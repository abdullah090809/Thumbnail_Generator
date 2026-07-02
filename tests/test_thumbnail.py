from fastapi import status
from unittest.mock import patch


def test_get_my_thumbnails(
    authorized_client
):

    response = authorized_client.get(
        "/thumbnails/"
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_my_thumbnails_unauthorized(
    client
):

    response = client.get(
        "/thumbnails/"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@patch(
    "app.routers.thumbnail.save_thumbnail_locally"
)
@patch(
    "app.routers.thumbnail.overlay_title_text"
)
@patch(
    "app.routers.thumbnail.fetch_base_image"
)
def test_generate_thumbnail(
    mock_fetch,
    mock_overlay,
    mock_save,
    authorized_client
):

    mock_fetch.return_value = "image"
    mock_overlay.return_value = "edited_image"
    mock_save.return_value = "thumbnail.jpg"

    response = authorized_client.post(
    "/thumbnails/",
    json={
        "title": "Python Tutorial",
        "topic": "Programming",
        "style": "tutorial",
        "color_scheme": "Blue"
    }
)

    assert response.status_code == \
        status.HTTP_201_CREATED

    data = response.json()

    assert data["title"] == "Python Tutorial"
    assert data["topic"] == "Programming"


@patch(
    "app.routers.thumbnail.fetch_base_image"
)
def test_generate_thumbnail_api_failure(
    mock_fetch,
    authorized_client
):

    mock_fetch.side_effect = Exception(
        "Pollinations Error"
    )

    response = authorized_client.post(
        "/thumbnails/",
        json={
            "title": "Python Tutorial",
            "topic": "Programming",
            "style": "tutorial",
            "color_scheme": "Blue"
        }
    )

    assert response.status_code == \
        status.HTTP_502_BAD_GATEWAY

    assert response.json()["detail"] == \
        "Failed to generate base image from Pollinations.ai"


def test_download_thumbnail_not_found(
    authorized_client
):

    response = authorized_client.get(
        "/thumbnails/999"
    )

    assert response.status_code == \
        status.HTTP_404_NOT_FOUND