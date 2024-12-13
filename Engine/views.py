from django.shortcuts import render,redirect
import os
import numpy as np
from PIL import Image
from skimage.io import imread
from keras.models import load_model
from django.http import JsonResponse
from keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

# Create your views here.
def homepage(request):
    return render(request,'Engine/Homepage.html')



# Load the model once when the server starts
MODEL_PATH = os.path.join("Assets", "catdog.h5")
model = load_model(MODEL_PATH)

def predict_image(request):
    # Default value for predicted_class to avoid uninitialized variable errors
    predicted_class = "No prediction made"

    if request.method == "POST" and request.FILES.get("image"):
        uploaded_image = request.FILES["image"]

        # Save uploaded image temporarily
        temp_image_path = "Assets/Detection/Input/temp_image.jpg"
        with open(temp_image_path, "wb") as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        try:
            # Preprocess the image
            img = image.load_img(temp_image_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # Make prediction
            preds = model.predict(x)
            out = decode_predictions(preds, top=1)
            predicted_class = out[0][0][1]  # Get the predicted class

            # Replace underscores with spaces for better readability
            predicted_class = predicted_class.replace("_", " ").title()

        except Exception as e:
            predicted_class = f"Error during prediction: {str(e)}"

        finally:
            # Clean up the temporary file
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

        return render(request, "Engine/Prediction.html", {"prediction": predicted_class})
    else:
        return render(request, "Engine/Prediction.html")

