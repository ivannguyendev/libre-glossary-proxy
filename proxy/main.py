import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from LibreTranslateAPI import LibreTranslateAPI
from mask import mask_vi, mask_en, unmask_content


import logging

# Configure logging
# Uvicorn overrides logging config, so we hook into uvicorn's logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

app = FastAPI()

LIBRETRANSLATE_URL = os.getenv("LIBRETRANSLATE_URL", "http://libretranslate:5000")

@app.get("/")
def read_root():
    return {"message": "LibreTranslate Proxy is running"}

class TranslateRequest(BaseModel):
    q: str
    source: str = "auto"
    target: str
    format: Optional[str] = "text"
    api_key: Optional[str] = None

@app.post("/translate")
def translate(request: TranslateRequest):
    try:
        # 1. Mask content to skip translation for specific POS tags
        if request.source == "en":
            masked_q, mapping = mask_en(request.q)
        else:
            masked_q, mapping = mask_vi(request.q)

        lt = LibreTranslateAPI(LIBRETRANSLATE_URL, api_key=request.api_key)
        
        # We force text format since we are handling the masking ourselves now
        # and not relying on HTML tags
        translation_response = lt.translate(
            q=masked_q,
            source=request.source,
            target=request.target,
            format="text",
        )
        
        translated_text = translation_response.get("translatedText", "")

        # 4. Unmask content
        clean_text = unmask_content(translated_text, mapping)
        
        # Update response with clean text
        translation_response["translatedText"] = clean_text

        return translation_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class DetectRequest(BaseModel):
    q: str
    api_key: Optional[str] = None

@app.post("/detect")
def detect(request: DetectRequest):
    try:
        lt = LibreTranslateAPI(LIBRETRANSLATE_URL, api_key=request.api_key)
        result = lt.detect(request.q)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/languages")
def languages():
    try:
        lt = LibreTranslateAPI(LIBRETRANSLATE_URL)
        return lt.languages()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
