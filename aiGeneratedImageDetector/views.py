from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime

from .aiImageDetector import detect_ai_image


@api_view(['POST'])
def detectAIgeneratedImage(request):

    if 'image' not in request.FILES:
        return Response({"success": False, "error": "No image file provided"}, status=400)

    image_file = request.FILES['image']

    # Validate file type
    valid_extensions = ('.jpg', '.jpeg', '.png')
    if not image_file.name.lower().endswith(valid_extensions):
        return Response({"success": False, "error": "Invalid file type"}, status=400)

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"temp_{timestamp}_{image_file.name}"

        temp_path = default_storage.save(temp_filename, ContentFile(image_file.read()))
        full_temp_path = default_storage.path(temp_path)

        # Run detector
        result = detect_ai_image(full_temp_path)

        # Remove temp file
        default_storage.delete(temp_path)

        # Response
        return Response(result, status=200 if result["success"] else 500)

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
