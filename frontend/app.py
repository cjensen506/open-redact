"""Gradio demo frontend for the open-redact API.

This app runs as its own Hugging Face Space. It calls the open-redact API
server-side (so no CORS configuration is required on the API), letting anyone
upload a PDF, choose which PII entity types to redact, preview the redacted
result, and download it.

The API location is configured via the ``API_BASE_URL`` environment variable
(set it as a Space secret). It defaults to the public open-redact API Space.
"""

import os
import tempfile

import fitz  # PyMuPDF, used to render the redacted PDF to preview images
import gradio as gr
import requests

API_BASE_URL = os.environ.get(
    "API_BASE_URL", "https://cjensen506-open-redact.hf.space"
).rstrip("/")

# Generous timeout: the free API tier loads a large spaCy model and may
# cold-start on the first request.
REQUEST_TIMEOUT = 120

# Entity types pre-checked on load, when the API reports them as supported.
DEFAULT_ENTITIES = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"]


def fetch_entities():
    """Return the entity types the API supports, for the checkbox group.

    Called once at startup. On any failure we fall back to an empty list so the
    app still loads and can show a clear error when the user tries to redact.
    """
    try:
        resp = requests.get(f"{API_BASE_URL}/entities", timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json().get("entities", [])
    except requests.RequestException:
        return []


def _pdf_to_images(pdf_path):
    """Render each page of a PDF to a PNG for the preview gallery."""
    images = []
    doc = fitz.open(pdf_path)
    try:
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=130)
            out = os.path.join(tempfile.gettempdir(), f"preview_{os.getpid()}_{i}.png")
            pix.save(out)
            images.append(out)
    finally:
        doc.close()
    return images


def redact(pdf_path, selected_entities):
    """Send the PDF + chosen entities to the API; return (download, preview)."""
    if not pdf_path:
        raise gr.Error("Please upload a PDF file first.")
    if not selected_entities:
        raise gr.Error("Select at least one entity type to redact.")

    with open(pdf_path, "rb") as f:
        files = {"file": ("input.pdf", f, "application/pdf")}
        # Repeated form field, matching the API's `_parse_entities`.
        data = [("entities", entity) for entity in selected_entities]
        try:
            resp = requests.post(
                f"{API_BASE_URL}/redact_pdf",
                files=files,
                data=data,
                timeout=REQUEST_TIMEOUT,
            )
        except requests.RequestException as exc:
            raise gr.Error(f"Could not reach the API at {API_BASE_URL}: {exc}")

    if resp.status_code != 200:
        raise gr.Error(f"API error {resp.status_code}: {resp.text}")

    out_path = os.path.join(tempfile.gettempdir(), "redacted.pdf")
    with open(out_path, "wb") as f:
        f.write(resp.content)

    return out_path, _pdf_to_images(out_path)


ALL_ENTITIES = fetch_entities()

CSS = """
.gradio-container { max-width: 1080px !important; margin: auto !important; }
#header { text-align: center; margin-bottom: 0.5rem; }
#header h1 { margin-bottom: 0.25rem; }
#redact-btn { margin-top: 0.5rem; }
footer { display: none !important; }
"""

theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
    neutral_hue="slate",
)

with gr.Blocks(title="Open Redact") as demo:
    gr.Markdown(
        "# 🔒 Open Redact\n"
        "Upload a PDF, choose which personally identifiable information (PII) to "
        "redact, then preview and download the anonymized result — for example, "
        "to redact names from resumes before review for a more equitable hiring "
        "process.",
        elem_id="header",
    )

    with gr.Row(equal_height=False):
        with gr.Column(scale=4):
            pdf_input = gr.File(
                label="1. Upload a PDF",
                file_types=[".pdf"],
                file_count="single",
            )
            entity_choices = gr.CheckboxGroup(
                choices=ALL_ENTITIES,
                value=[e for e in DEFAULT_ENTITIES if e in ALL_ENTITIES],
                label="2. PII to redact",
            )
            redact_button = gr.Button(
                "🔒 Redact PDF", variant="primary", size="lg", elem_id="redact-btn"
            )

        with gr.Column(scale=6):
            preview_gallery = gr.Gallery(
                label="Redacted preview",
                columns=1,
                height=560,
                object_fit="contain",
            )
            pdf_output = gr.File(label="Download redacted PDF")

    gr.Markdown(
        f"<div style='text-align:center;opacity:0.6'>Powered by the "
        f"<a href='{API_BASE_URL}/docs'>open-redact API</a> &middot; "
        f"<a href='https://github.com/cjensen506/open-redact'>GitHub</a></div>"
    )

    redact_button.click(
        fn=redact,
        inputs=[pdf_input, entity_choices],
        outputs=[pdf_output, preview_gallery],
    )


if __name__ == "__main__":
    demo.launch(theme=theme, css=CSS)
