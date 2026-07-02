import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.cores.database import get_db
from app.cores.security import get_current_user
from app.models.thumbnail import Thumbnail
from app.models.user import User
from app.schemas.thumbnail import ThumbnailCreate, ThumbnailResponse
from app.services.image_service import fetch_base_image, overlay_title_text, save_thumbnail_locally
from app.services.prompt_service import build_thumbnail_prompt


router = APIRouter(prefix="/thumbnails", tags=["Thumbnails"])

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=ThumbnailResponse)
async def generate_thumnail(thumbnail_request: ThumbnailCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    generated_prompt = build_thumbnail_prompt(
        topic=thumbnail_request.topic,
        style=thumbnail_request.style,
        color_scheme=thumbnail_request.color_scheme,
    )
    try:
        base_image = await fetch_base_image(generated_prompt)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to generate base image from Pollinations.ai",
        )
    final_image = overlay_title_text(base_image, thumbnail_request.title)

    filepath = save_thumbnail_locally(final_image)

    new_thumbnail = Thumbnail(
        title=thumbnail_request.title,
        topic=thumbnail_request.topic,
        style=thumbnail_request.style,
        color_scheme=thumbnail_request.color_scheme,
        generated_prompt=generated_prompt,
        image_url=filepath,
        owner_id=current_user.id,
    )
    db.add(new_thumbnail)
    db.commit()
    db.refresh(new_thumbnail)
    return new_thumbnail

@router.get("/", response_model=list[ThumbnailResponse])
def get_my_thumbnails(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    thumbnails = (
        db.query(Thumbnail).filter(Thumbnail.owner_id == current_user.id).all()
    )
    return thumbnails

@router.get("/{thumbnail_id}")
def download_thumbnail(
    thumbnail_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    thumbnail = (
        db.query(Thumbnail)
        .filter(
            Thumbnail.id == thumbnail_id, Thumbnail.owner_id == current_user.id
        )
        .first()
    )

    if not thumbnail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thumbnail with id {thumbnail_id} not found",
        )

    if not os.path.exists(thumbnail.image_url):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thumbnail file no longer exists on disk",
        )

    return FileResponse(
        thumbnail.image_url, media_type="image/jpeg", filename=f"thumbnail_{thumbnail_id}.jpg"
    )