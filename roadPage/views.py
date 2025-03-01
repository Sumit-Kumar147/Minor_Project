# roadPage/views.py
from django.shortcuts import render
from django.http import JsonResponse
import cloudinary
import cloudinary.uploader
from .utils import analyze_image,MODEL
import logging

logger = logging.getLogger(__name__)

# Cloudinary configuration
cloudinary.config( 
    cloud_name = "duzqgybdn", 
    api_key = "998255766485536", 
    api_secret = "0T9BkogE-cM1KZaKKlr3ktJ3QXA", 
    secure=True
)

def upload_page(request):
    """Render the upload page"""
    return render(request, 'upload.html')

def upload_image(request):
    """Handle image upload and analysis"""
    try:
        print("Starting upload_image view")
        
        if request.method != 'POST':
            return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file found'}, status=400)

        if MODEL is None:
            print("Model is not loaded")
            return JsonResponse({'error': 'Model not loaded'}, status=500)
        
        image_file = request.FILES['image']
        print(f"Received image: {image_file.name}")

        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if image_file.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid file type'}, status=400)

        # Upload to Cloudinary first
        print("Uploading to Cloudinary...")
        upload_result = cloudinary.uploader.upload(image_file)
        image_url = upload_result.get('secure_url')
        print(f"Cloudinary URL: {image_url}")

        # Analyze image
        print("Analyzing image...")
        analysis_result = analyze_image(image_file)
        if not analysis_result:
            print("Analysis failed")
            return JsonResponse({'error': 'Failed to analyze image'}, status=500)

        # Combine results
        response_data = {
            'image_url': image_url,
            'class_label': analysis_result['class_label'],
            'confidence': analysis_result['confidence'],
            'analyzed_image': analysis_result['image_base64'],
            'email_sent': analysis_result['email_sent']
        }
        print("Analysis complete")

        return JsonResponse(response_data)

    except Exception as e:
        print(f"Error in upload_image: {str(e)}")
        logger.error(f"Error processing upload: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)