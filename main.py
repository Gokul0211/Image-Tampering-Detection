# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import tempfile
import os
import time
import base64
import uuid
from io import BytesIO
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import uvicorn
import shutil

app = FastAPI(title="Image Tampering Detection API")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for serving files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variables
MODEL_PATH = os.path.join('model', 'model_casia_run1.h5')
IMAGE_SIZE = (128, 128)
CLASS_NAMES = ['fake', 'real']  # Note that 'fake' corresponds to 'tampered' in the frontend
ELA_SAVE_DIR = os.path.join('static', 'ela')

# Ensure the ELA directory exists
os.makedirs(ELA_SAVE_DIR, exist_ok=True)

# Load model at startup
model = None

@app.on_event("startup")
async def load_ml_model():
    global model
    try:
        model = load_model(MODEL_PATH)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        # Continue without crashing, will handle in the endpoint

def convert_to_ela_image(image_path, quality=91):
    """Convert image to Error Level Analysis (ELA) image and save it"""
    # Create a temporary filename for JPEG compression
    temp_filename = os.path.join(tempfile.gettempdir(), f"temp_ela_{uuid.uuid4().hex}.jpg")
    
    try:
        # Open the original image
        image = Image.open(image_path).convert('RGB')
        image.save(temp_filename, 'JPEG', quality=quality)
        temp_image = Image.open(temp_filename)
        
        # Calculate ELA
        ela_image = ImageChops.difference(image, temp_image)
        
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0:
            max_diff = 1
        scale = 255.0 / max_diff
        
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        
        # Generate a unique filename for saving the ELA image
        ela_filename = f"ela_{uuid.uuid4().hex}.jpg"
        ela_save_path = os.path.join(ELA_SAVE_DIR, ela_filename)
        
        # Save the ELA image
        ela_image.save(ela_save_path)
        
        return ela_image, f"/static/ela/{ela_filename}"
        
    finally:
        # Clean up the temporary compression file
        try:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        except Exception as e:
            print(f"Warning: Could not delete temporary file {temp_filename}: {e}")

def prepare_image(image_path):
    """Prepare image for model prediction"""
    ela_image, ela_path = convert_to_ela_image(image_path)
    ela_resized = ela_image.resize(IMAGE_SIZE)
    image_array = np.array(ela_resized) / 255.0
    return image_array, ela_image, ela_path

def encode_ela_image(ela_image):
    """Encode ELA image to base64 for frontend display"""
    buffered = BytesIO()
    ela_image.save(buffered, format="JPEG")
    return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global model
    
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Check if the model is loaded
    if model is None:
        try:
            model = load_model(MODEL_PATH)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model not loaded: {str(e)}")
    
    # Check file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create a temporary file for the uploaded image
    temp_path = os.path.join(tempfile.gettempdir(), f"upload_{uuid.uuid4().hex}.jpg")
    
    try:
        # Save the uploaded file temporarily
        with open(temp_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        
        # Process the image
        start_time = time.time()
        image_array, ela_image, ela_path = prepare_image(temp_path)
        
        # Reshape for prediction
        image_array = image_array.reshape(-1, IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
        
        # Make prediction
        prediction = model.predict(image_array)
        predicted_class_idx = np.argmax(prediction, axis=1)[0]
        predicted_class = CLASS_NAMES[predicted_class_idx]
        confidence = float(np.max(prediction))
        
        # For frontend compatibility, also include base64 encoding
        ela_base64 = encode_ela_image(ela_image)
        
        # Map 'fake'/'real' to 'tampered'/'authentic' for frontend
        frontend_prediction = "tampered" if predicted_class == "fake" else "authentic"
        
        # Prepare response
# In the /predict endpoint response, add milliseconds to processing_time
        response = {
            "prediction": frontend_prediction,
            "confidence": confidence,
            "ela_image": ela_base64,
            "ela_path": ela_path,
            "processing_time": (time.time() - start_time) * 1000  # Convert to milliseconds
        }
        return JSONResponse(content=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    finally:
        # Clean up the temporary uploaded file
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception as e:
            print(f"Warning: Could not delete temporary file {temp_path}: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "model_loaded": model is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)