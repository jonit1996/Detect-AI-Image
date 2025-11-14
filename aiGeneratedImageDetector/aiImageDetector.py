# -*- coding: utf-8 -*-
import torch
from PIL import Image as PILImage
from transformers import AutoImageProcessor, Swinv2ForImageClassification

# -------- GLOBAL MODEL LOADING (runs only once) -------- #

MODEL_PATH = r"E:\AICS\aiGeneratedImageDetector_API\aiGeneratedImageDetectorAPI\Ai-images-detectorModel"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

try:
    processor = AutoImageProcessor.from_pretrained(
        MODEL_PATH,
        local_files_only=True
    )
    model = Swinv2ForImageClassification.from_pretrained(
        MODEL_PATH,
        local_files_only=True
    )
    model.to(device)
    model.eval()
except Exception as e:
    print("❌ ERROR LOADING MODEL:", e)
    processor = None
    model = None


# ---------------- DETECTION FUNCTION ---------------- #

def detect_ai_image(image_path):
    try:
        if model is None or processor is None:
            return {"success": False, "error": "Model loading failed"}

        # Load and preprocess image
        image = PILImage.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt").to(device)

        # Inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        predicted_class_idx = logits.argmax(-1).item()
        predicted_label = model.config.id2label[predicted_class_idx]
        probabilities = torch.softmax(logits, dim=-1)

        return {
            "success": True,
            "predicted_label": predicted_label,
            "confidence": f"{round(probabilities[0, predicted_class_idx].item() * 100)}%"
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
