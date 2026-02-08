# libre-glossary-proxy
Glossary proxy opensource for LibreTranslate

## Setup & Run

1.  Create environment configuration:
    ```bash
    cp .env.example .env
    ```

2.  Start the services:
    ```bash
    docker-compose up --build
    ```

## Example Usage

### Translate (POST /translate)

**English to Vietnamese:**
```bash
curl -X POST "https://proxy.libre-glossary-proxy.orb.local/translate" \
     -H "Content-Type: application/json" \
     -d '{
           "q": "Hello world",
           "source": "en",
           "target": "vi"
         }'
```

**Vietnamese to English:**
```bash
curl -X POST "https://proxy.libre-glossary-proxy.orb.local/translate" \
     -H "Content-Type: application/json" \
     -d '{
           "q": "Bình đang đi học",
           "source": "vi",
           "target": "en"
         }'
```

**English to Vietnamese:**
```bash
curl -X POST "https://proxy.libre-glossary-proxy.orb.local/translate" \
     -H "Content-Type: application/json" \
     -d '{
           "q": "Apple is looking at buying U.K. startup for $1 billion",
           "source": "en",
           "target": "vi"
         }'
```

### Detect Language (POST /detect)

```bash
curl -X POST "https://proxy.libre-glossary-proxy.orb.local/detect" \
     -H "Content-Type: application/json" \
     -d '{
           "q": "Xin chào"
         }'
```

### Supported Languages (GET /languages)

```bash
curl "https://proxy.libre-glossary-proxy.orb.local/languages"
```
