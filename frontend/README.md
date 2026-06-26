---
title: Open Redact Demo
emoji: 🔒
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
---

# Open Redact Demo

A small [Gradio](https://www.gradio.app/) frontend that lets anyone try the
[open-redact](https://github.com/cjensen506/open-redact) API in the browser:
upload a PDF, pick which PII entity types to redact, and download the
anonymized result.

This app calls the open-redact API **server-side**, so the API needs no CORS
configuration. The frontend is intentionally kept separate from the API code so
the main repo stays cloneable as just the API.

## Configuration

The API location is read from the `API_BASE_URL` environment variable and
defaults to the public open-redact API Space. To point at a different
deployment (e.g. a local instance), set `API_BASE_URL`.

## Run locally

```bash
pip install -r requirements.txt
# Optionally point at a local API instead of the public Space:
# export API_BASE_URL=http://127.0.0.1:8000
python app.py
```

Then open the local URL Gradio prints (usually http://127.0.0.1:7860).

## Deploy as a Hugging Face Space

1. Create a new Space → SDK **Gradio**.
2. Push the contents of this `frontend/` folder to the Space's git remote. From
   the root of the open-redact repo you can use a subtree push:

   ```bash
   git subtree push --prefix frontend <space-git-url> main
   ```

   (Or clone the Space repo separately and copy `app.py`, `requirements.txt`,
   and this `README.md` into it.)
3. In the Space **Settings → Variables and secrets**, set `API_BASE_URL` to the
   API Space's direct URL, e.g. `https://<hf-user>-open-redact.hf.space` (find
   it via the API Space page's "Embed this Space" / `*.hf.space` link).
