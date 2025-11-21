# # app/api/ai_tagging.py
# from io import BytesIO
# from typing import List

# from fastapi import APIRouter, UploadFile, File, HTTPException
# from PIL import Image
# from transformers import pipeline

# router = APIRouter()

# # Load model once at process start
# classifier = pipeline(
#     "zero-shot-image-classification",
#     model="openai/clip-vit-base-patch32"
# )

# # Tune this to your world
# CANDIDATE_TAGS = [
#     "character",
#     "human",
#     "creature",
#     "prop",
#     "environment",
#     "architecture",
#     "city",
#     "nature",
#     "hdri",
#     "texture",
#     "fx",
#     "vfx",
#     "dust",
#     "smoke",
#     "explosion",
#     "sci-fi",
#     "fantasy",
#     "realistic",
#     "cartoon",
#     "cinematic",
#     "studio lighting",
#     "night",
#     "day",
#     "interior",
#     "exterior",
# ]

# @router.post("/ai/tags")
# async def ai_generate_tags(
#     file: UploadFile = File(...),
#     max_tags: int = 8,
#     min_score: float = 0.15,
# ):
#     if not file.content_type or not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="File must be an image")

#     # Read image
#     data = await file.read()
#     image = Image.open(BytesIO(data)).convert("RGB")

#     # Run CLIP zero-shot classification
#     result = classifier(
#         image,
#         candidate_labels=CANDIDATE_TAGS,
#         hypothesis_template="a render of {}"
#     )

#     tags: List[str] = []
#     for item in result:
#         label = item["label"]
#         score = float(item["score"])
#         if score < min_score:
#             continue
#         tag = label.lower().replace(" ", "_")  # normalize
#         tags.append(tag)
#         if len(tags) >= max_tags:
#             break

#     return {"tags": tags}
