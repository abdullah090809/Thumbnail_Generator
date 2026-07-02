from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from app.cores.database import Base


class Thumbnail(Base):
    __tablename__ = "thumbnails"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    style = Column(String, nullable=False)
    color_scheme = Column(String, nullable=False)
    generated_prompt = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    owner = relationship("User")