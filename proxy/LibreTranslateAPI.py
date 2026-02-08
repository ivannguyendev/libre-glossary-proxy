import httpx
from typing import Optional, List, Dict, Union

class LibreTranslateAPI:
    """
    A client for the LibreTranslate API.
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the LibreTranslate API client.

        :param base_url: The base URL of the LibreTranslate instance (e.g., "http://localhost:5000").
        :param api_key: Optional API key.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _post(self, endpoint: str, data: Dict) -> Dict:
        """
        Helper method to perform POST requests.
        """
        url = f"{self.base_url}{endpoint}"
        if self.api_key:
            data["api_key"] = self.api_key
        
        # Using a context manager for each request since we are in a synchronous context
        # and not sharing a session across requests in this simple implementation.
        # If performance becomes an issue, we can use a shared Client.
        with httpx.Client() as client:
            response = client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Union[Dict, List]:
        """
        Helper method to perform GET requests.
        """
        url = f"{self.base_url}{endpoint}"
        if self.api_key:
            if params is None:
                params = {}
            params["api_key"] = self.api_key
            
        with httpx.Client() as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def translate(self, q: Union[str, List[str]], source: str, target: str, format: str = "text", **kwargs) -> Dict:
        """
        Translate text from source language to target language.

        :param q: The text to translate (string or list of strings).
        :param source: The source language code (e.g., "en", "auto").
        :param target: The target language code (e.g., "es").
        :param format: The format of the text ("text" or "html"). Default is "text".
        :param kwargs: Additional arguments to pass to the API.
        :return: The translated text (string or list of strings).
        """
        data = {
            "q": q,
            "source": source,
            "target": target,
            "format": format,
            **kwargs
        }
        result = self._post("/translate", data)
        return result

    def detect(self, q: str) -> List[Dict]:
        """
        Detect the language of the text.

        :param q: The text to detect.
        :return: A list of detection results, e.g., [{'confidence': 0.6, 'language': 'en'}].
        """
        data = {"q": q}
        return self._post("/detect", data)

    def languages(self) -> List[Dict]:
        """
        Retrieve the list of supported languages.

        :return: A list of supported languages.
        """
        return self._get("/languages")

    def suggest(self, q: str, s: str, t: str, correction: str) -> Dict:
        """
        Submit a suggestion for a translation.

        :param q: The original text.
        :param s: The source language code.
        :param t: The target language code.
        :param correction: The suggested translation.
        :return: The API response.
        """
        data = {
            "q": q,
            "s": s,
            "t": t,
            "correction": correction
        }
        return self._post("/suggest", data)

    def frontend_settings(self) -> Dict:
        """
        Retrieve frontend settings.

        :return: A dictionary of settings.
        """
        return self._get("/frontend/settings")
