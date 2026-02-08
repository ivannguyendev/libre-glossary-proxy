import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from libretranslatepy import LibreTranslateAPI

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
        lt = LibreTranslateAPI(LIBRETRANSLATE_URL, api_key=request.api_key)
        result = lt.translate(
            request.q,
            request.source,
            request.target
        )
        return {"translatedText": result}
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
