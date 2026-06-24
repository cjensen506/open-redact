import fitz
from fastapi.testclient import TestClient

from app.main.main import app

client = TestClient(app)


def _sample_pdf():
    """Build a small in-memory PDF containing a name and an email."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Resume of Lindsey Horan")
    page.insert_text((72, 100), "Email: fake_email@fake.com")
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_post_json():
    response = client.post(
        "/redact_pdf",
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"}
    )
    assert response.status_code == 422


def test_list_entities():
    response = client.get("/entities")
    assert response.status_code == 200
    entities = response.json()["entities"]
    assert "PERSON" in entities
    assert "EMAIL_ADDRESS" in entities


def test_redact_requires_entities():
    response = client.post(
        "/redact_pdf",
        files={"file": ("sample.pdf", _sample_pdf(), "application/pdf")},
    )
    assert response.status_code == 400


def test_redact_rejects_unsupported_entity():
    response = client.post(
        "/redact_pdf",
        files={"file": ("sample.pdf", _sample_pdf(), "application/pdf")},
        data={"entities": "NOT_A_REAL_ENTITY"},
    )
    assert response.status_code == 400


def test_redact_with_entities():
    response = client.post(
        "/redact_pdf",
        files={"file": ("sample.pdf", _sample_pdf(), "application/pdf")},
        data={"entities": ["PERSON", "EMAIL_ADDRESS"]},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

    # the requested entities should be gone from the redacted output
    redacted = fitz.open(stream=response.content, filetype="pdf")
    text = "".join(page.get_text() for page in redacted)
    redacted.close()
    assert "Lindsey Horan" not in text
    assert "fake_email@fake.com" not in text


def test_redact_only_requested_entity():
    # only redact emails; the name should remain in the output
    response = client.post(
        "/redact_pdf",
        files={"file": ("sample.pdf", _sample_pdf(), "application/pdf")},
        data={"entities": "EMAIL_ADDRESS"},
    )
    assert response.status_code == 200

    redacted = fitz.open(stream=response.content, filetype="pdf")
    text = "".join(page.get_text() for page in redacted)
    redacted.close()
    assert "fake_email@fake.com" not in text
    assert "Lindsey Horan" in text


# not yet setup correctly
# def test_post_wrong_file_type():
#     with open("./app/test/sample_txt_file.txt", "rb") as file:
#         response = client.post(
#             "/redact_pdf",
#             data={"file": file}
#         )
#         assert response.status_code == 415
