from underthesea import pos_tag
import spacy

from typing import Tuple, Dict
import re
import logging


logger = logging.getLogger("uvicorn")

try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    logger.warning("Spacy model 'en_core_web_md' not found. English masking might fail.")
    nlp = None


def mask_en(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Masks specific parts of English text (Proper nouns, Numbers, Punctuation)
    with placeholders ZGL0, ZGL1, etc. using Spacy.
    """
    if nlp is None:
        logger.warning("Spacy model not loaded, skipping masking for English text.")
        return text, {}
    
    try:
        doc = nlp(text)
        processed_tokens = []
        mapping = {}
        mask_counter = 0

        for token in doc:
            # PROPN: Proper noun,  PUNCT: Punctuation, SYM: Symbol
            if token.pos_ in ["PUNCT"]:
                mask = f"ZGL{mask_counter}"
                mapping[mask] = token.text
                processed_tokens.append(mask)
                mask_counter += 1
            else:
                processed_tokens.append(token.text)
        
        return " ".join(processed_tokens), mapping
    except Exception as e:
        logger.error(f"Error in mask_en: {e}")
        return text, {}


def mask_vi(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Masks specific parts of Vietnamese text (Proper nouns, Numbers, Punctuation)
    with placeholders ZGL0, ZGL1, etc. using Underthesea.
    """
    try:
        # pos_tag returns list of (word, tag) tuples
        tags = pos_tag(text)
        processed_tokens = []
        mapping = {}
        mask_counter = 0

        for word, tag in tags:
            # Np: Proper noun, M: Number, CH: Punctuation
            if tag in ["Np", "M", "CH"]:
                mask = f"ZGL{mask_counter}"
                mapping[mask] = word
                processed_tokens.append(mask)
                mask_counter += 1
            else:
                processed_tokens.append(word)
        
        return " ".join(processed_tokens), mapping
    except Exception as e:
        logger.error(f"Error in mask_vi: {e}")
        return text, {}

def unmask_content(text: str, mapping: Dict[str, str]) -> str:
    """
    Restores valid placeholders ZGL<Number> with their original content.
    """
    try:
        # We look for ZGL followed by digits
        def replace_match(match):
            mask = match.group(0)
            return mapping.get(mask, mask) # Return original mask if not found in mapping
            
        return re.sub(r'ZGL\d+', replace_match, text)
    except Exception as e:
        logger.error(f"Error in unmask_content: {e}")
        return text
