# test_model.py
import os
import tensorflow as tf
from dotenv import load_dotenv

load_dotenv()

def test_model_loading():
    try:
        # Print current directory and available files
        print(f"Current directory: {os.getcwd()}")
        print(f"Files in current directory: {os.listdir('.')}")
        
        # Try to load model
        model_path = os.getenv('MODEL_PATH', 'model_deep.keras')
        print(f"Attempting to load model from: {model_path}")
        
        if not os.path.exists(model_path):
            print(f"Model file not found at: {model_path}")
            return False
            
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully")
        print(f"Model summary:")
        model.summary()
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

if __name__ == "__main__":
    test_model_loading()