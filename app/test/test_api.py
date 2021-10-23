from fastapi.testclient import TestClient

from app.main.main import app

client = TestClient(app)


def test_post_json():
    response = client.post(
        "/redact_pdf",
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"}
    )
    assert response.status_code == 422


# not yet setup correctly
# def test_post_wrong_file_type():
#     with open("./app/test/sample_txt_file.txt", "rb") as file:
#         response = client.post(
#             "/redact_pdf",
#             data={"file": file}
#         )
#         assert response.status_code == 415
