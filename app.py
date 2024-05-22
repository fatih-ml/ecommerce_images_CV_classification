from flask import Flask, request, jsonify, render_template, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import pandas as pd
import os
import random
import gdown
import gc
from predict import (
    get_random_image,
    preprocess_image,
    bring_predict_probas,
    create_dataframe,
)


app = Flask(__name__)

# some constants
STATIC_DIR = "static"
MODEL_PATH = "mobilenetv2_18K_model.h5"
DRIVE_URL = "https://drive.google.com/uc?id=1S55B7V3WhETRw3NSjRci65GGDbPVw-bE"

model = None


def download_model(drive_url, output_path):
    gdown.download(drive_url, output_path, quiet=False)


# Lazy load the model for low RAM usage
def load_model_if_not_loaded():
    global model
    if model is None:
        print("Loading model...")
        model = load_model(MODEL_PATH)
    return model


if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    download_model(DRIVE_URL, MODEL_PATH)
else:
    print("Model already exists. Skipping download.")

# Load our model (model***.h5 file needs to be in the same directory as app.py)
# model = load_model(MODEL_PATH)


# Define a route for the default URL, which loads the index page
# This is HOME PAGE route
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate_image", methods=["GET"])
def generate_image():
    image_path, image_class = get_random_image(STATIC_DIR)
    image_url = f"/static/{image_class}/{os.path.basename(image_path)}"
    return jsonify({"image_url": image_url, "image_class": image_class})


@app.route("/predict", methods=["POST"])
def predict():
    global model
    image_url = request.form["image_path"]
    image_path = os.path.join(STATIC_DIR, *image_url.split("/static/")[1:])
    _, img_array = preprocess_image(image_path)
    model = load_model_if_not_loaded()
    predictions = model.predict(img_array)
    sorted_class_labels, sorted_probabilities = bring_predict_probas(predictions)
    df = create_dataframe(sorted_class_labels, sorted_probabilities)
    prediction = sorted_class_labels[0]
    return jsonify(
        {
            "prediction": prediction,
            "dataframe": df.to_html(classes="data", header="true"),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
