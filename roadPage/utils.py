# roadPage/utils.py
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import smtplib
import os
from dotenv import load_dotenv
import base64
import io
from django.conf import settings

# Load environment variables
load_dotenv()

# Email Configuration
FROM_EMAIL = os.getenv("FROM_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
STREET_NAME = os.getenv("STREET_NAME", "Unknown Location")

BASE_DIR = settings.BASE_DIR

# Model path configuration
MODEL_LOCATIONS = [
    os.path.join(BASE_DIR, 'model_deep.keras'),
    os.path.join(BASE_DIR, 'mysite', 'roadPage', 'model_deep.keras'),
    os.path.join(BASE_DIR, 'roadPage', 'model_deep.keras')
]

def find_model():
    for path in MODEL_LOCATIONS:
        if os.path.exists(path):
            print(f"Found model at: {path}")
            return path
    return None

# Load the model
try:
    model_path = find_model()
    if model_path is None:
        raise FileNotFoundError("Model file not found in any of the expected locations")
    print(f"Loading model from: {model_path}")
    MODEL = tf.keras.models.load_model(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    MODEL = None
 

def load_image(image_file):
    """
    Load and preprocess an image for prediction.
    Args:
        image_file: File object or path to the image.
    Returns:
        tuple: (original_image, preprocessed_image_array)
    """
    try:
        if isinstance(image_file, str):
            # If input is a file path
            img = Image.open(image_file)
        else:
            # If input is a file object
            img = Image.open(image_file)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Store original image for visualization
        original_img = img.copy()
        
        # Preprocess for model
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        
        return original_img, np.expand_dims(img_array, axis=0)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None

def send_email(subject, body):
    """Send email notification"""
    try:
        # Print debug information
        print(f"Attempting to send email from: {FROM_EMAIL}")
        print(f"Sending to: {TO_EMAIL}")
        print(f"Subject: {subject}")
        
        if not all([FROM_EMAIL, EMAIL_PASSWORD, TO_EMAIL]):
            print("Missing email configuration")
            return False

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            
            # Login attempt
            print("Attempting to login to SMTP server...")
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            print("Login successful")

            # Prepare message
            msg = f"Subject: {subject}\n\n{body}"
            
            # Send email
            print("Sending email...")
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg)
            print("Email sent successfully")
            
            return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def analyze_image(image_file):
    """
    Analyze image and return prediction results
    Args:
        image_file: File object from request.FILES
    Returns:
        dict: Analysis results including class label, confidence, and visualization
    """
    try:
        # Load and preprocess image
        original_img, processed_img = load_image(image_file)
        if processed_img is None:
            return None

        # Make prediction
        prediction = MODEL.predict(processed_img)
        class_idx = np.argmax(prediction)
        class_label = "Garbage" if class_idx == 1 else "Clean"
        confidence = float(prediction[0][class_idx])

        # Create visualization
        img_array = np.array(original_img)
        img_display = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Add prediction text to image
        text = f"{class_label} ({confidence:.2f})"
        cv2.putText(img_display, text,
                    (10, 30),  # position
                    cv2.FONT_HERSHEY_SIMPLEX,  # font
                    1,  # font scale
                    (0, 255, 0),  # color (BGR)
                    2)  # thickness

        # Convert result image to base64
        _, buffer = cv2.imencode('.jpg', img_display)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        # Send email if garbage is detected
        email_sent = None
        if class_label == "Garbage":
            subject = "Garbage Detected!"
            body = f"Street - {STREET_NAME} is found to be unclean with confidence {confidence:.2f}."
            email_sent = send_email(subject, body)

        return {
            'class_label': class_label,
            'confidence': confidence,
            'image_base64': img_base64,
            'email_sent': email_sent
        }

    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None

def predict_and_print(image_path, model=MODEL):
    """
    Predict and print results, sending email if garbage is detected.
    Args:
        image_path (str): Path to the image file
        model: The loaded model (defaults to global MODEL)
    """
    try:
        # Load and preprocess image
        original_img, processed_img = load_image(image_path)
        if processed_img is None:
            return

        # Make prediction
        prediction = model.predict(processed_img)
        class_idx = np.argmax(prediction)
        class_label = "Garbage" if class_idx == 1 else "Clean"
        confidence = float(prediction[0][class_idx])

        print(f"Prediction: {class_label} ({confidence:.2f})")

        # Send email if garbage is detected
        if class_label == "Garbage":
            subject = "Garbage Detected!"
            body = f"Street - {STREET_NAME} is found to be unclean with confidence {confidence:.2f}."
            send_email(subject, body)

        return {
            'class_label': class_label,
            'confidence': confidence
        }

    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def predict_and_visualize(image_path, model=MODEL):
    """
    Predict the class of an image and visualize the result.
    Args:
        image_path (str): Path to the image file.
        model: The loaded model (defaults to global MODEL)
    Returns:
        dict: Prediction results and visualization
    """
    try:
        # Load and preprocess the image
        original_img, processed_img = load_image(image_path)
        if processed_img is None:
            return None

        # Predict the class
        prediction = model.predict(processed_img)
        class_idx = np.argmax(prediction)
        class_label = "Garbage" if class_idx == 1 else "Clean"
        confidence = float(prediction[0][class_idx])

        # Create visualization
        img_array = np.array(original_img)
        img_display = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Add prediction text
        cv2.putText(img_display, 
                    f"{class_label} ({confidence:.2f})", 
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1, 
                    (0, 255, 0), 
                    2)

        # Display the image
        cv2.imshow("Prediction", img_display)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return {
            'class_label': class_label,
            'confidence': confidence,
            'image': img_display
        }

    except Exception as e:
        print(f"Error processing image: {e}")
        return None