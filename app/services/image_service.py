import io
import os
import uuid
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import httpx
from app.cores.config import settings

THUMBNAIL_WIDTH = 1280
THUMBNAIL_HEIGHT = 720

GENERATED_DIR = "generated_thumbnails"


async def fetch_base_image(prompt: str) -> Image.Image:
    encoded_prompt = quote(prompt)
    url = (
        f"{settings.POLLINATIONS_BASE_URL}/{encoded_prompt}"
        f"?width={THUMBNAIL_WIDTH}&height={THUMBNAIL_HEIGHT}"
        f"&model=flux&nologo=true&enhance=true"
    )

    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    image_bytes = response.content
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    return image


def boost_image_quality(image: Image.Image) -> Image.Image:
    image = ImageEnhance.Color(image).enhance(1.35)
    image = ImageEnhance.Contrast(image).enhance(1.15)
    image = ImageEnhance.Sharpness(image).enhance(1.3)
    return image


def overlay_title_text(image: Image.Image, title: str) -> Image.Image:
    image = boost_image_quality(image)
    image = image.resize((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
    draw = ImageDraw.Draw(image, "RGBA")

    font_size = 95
    font = ImageFont.load_default(size=font_size)

    max_width = THUMBNAIL_WIDTH - 80
    lines = _wrap_text(title, font, max_width, draw)

    line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total_text_height = sum(line_heights) + (len(lines) - 1) * 10

    overlay_height = total_text_height + 60
    overlay = Image.new(
        "RGBA", (THUMBNAIL_WIDTH, overlay_height), (0, 0, 0, 190)
    )
    image.paste(
        overlay, (0, THUMBNAIL_HEIGHT - overlay_height), overlay
    )

    y = THUMBNAIL_HEIGHT - overlay_height + 30
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (THUMBNAIL_WIDTH - line_width) // 2
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        y += bbox[3] + 10

    return image.convert("RGB")


def _wrap_text(text: str, font, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        test_width = bbox[2] - bbox[0]

        if test_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def save_thumbnail_locally(image: Image.Image) -> str:
    os.makedirs(GENERATED_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(GENERATED_DIR, filename)
    image.save(filepath, "JPEG", quality=90)
    return filepath