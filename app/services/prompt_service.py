from app.schemas.thumbnail import ThumbnailStyle

STYLE_MODIFIERS = {
    ThumbnailStyle.dramatic: (
        "dramatic cinematic lighting, high contrast, intense atmosphere, "
        "bold rim lighting, epic composition, movie poster quality"
    ),
    ThumbnailStyle.minimal: (
        "minimalist design, clean composition, simple uncluttered background, "
        "plenty of negative space, modern flat design, elegant"
    ),
    ThumbnailStyle.gaming: (
        "gaming aesthetic, vibrant neon colors, action-packed dynamic pose, "
        "digital art, high energy, esports poster style"
    ),
    ThumbnailStyle.tutorial: (
        "clean professional photography, clear focal subject, bright even studio lighting, "
        "approachable, modern tech aesthetic"
    ),
    ThumbnailStyle.vlog: (
        "candid lifestyle photography, warm natural lighting, personal and relatable, "
        "authentic, shallow depth of field"
    ),
    ThumbnailStyle.educational: (
        "clear and informative, professional studio lighting, organized composition, "
        "trustworthy, polished editorial photography"
    ),
}

QUALITY_BOOSTERS = (
    "highly detailed, sharp focus, professional photography, 8k, "
    "trending on artstation, masterpiece quality"
)

NEGATIVE_GUIDANCE = (
    "no fake text, no illegible signage, no garbled UI, no watermark, "
    "no logos, no blurry background elements"
)


def build_thumbnail_prompt(topic: str, style: ThumbnailStyle, color_scheme: str) -> str:
    style_modifier = STYLE_MODIFIERS[style]

    prompt = (
        f"A professional YouTube thumbnail photo depicting {topic}, "
        f"{style_modifier}, dominant color palette of {color_scheme}, "
        f"{QUALITY_BOOSTERS}, {NEGATIVE_GUIDANCE}, 16:9 aspect ratio"
    )

    return prompt