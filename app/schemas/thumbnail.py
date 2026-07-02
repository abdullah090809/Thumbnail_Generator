from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


class ThumbnailStyle(str, Enum):
    dramatic = "dramatic"
    minimal = "minimal"
    gaming = "gaming"
    tutorial = "tutorial"
    vlog = "vlog"
    educational = "educational"


class ThumbnailCreate(BaseModel):
    title: str
    topic: str
    style: ThumbnailStyle
    color_scheme: str


class ThumbnailResponse(BaseModel):
    id: int
    title: str
    topic: str
    style: ThumbnailStyle
    color_scheme: str
    generated_prompt: str
    image_url: str
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)