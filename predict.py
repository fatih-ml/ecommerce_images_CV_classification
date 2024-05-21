import os
import random
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import logging

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)


# Function to randomly select an image from the SAMPLE_DATASET directory
def get_random_image(sample_dataset_dir):
    classes = os.listdir(sample_dataset_dir)
    selected_class = random.choice(classes)
    class_dir = os.path.join(sample_dataset_dir, selected_class)
    image_name = random.choice(os.listdir(class_dir))
    image_path = os.path.join(class_dir, image_name)
    return image_path, selected_class


# Function to preprocess the image
def preprocess_image(img_path):
    # Load the image (this itself is a printable image)
    loaded_img = image.load_img(img_path, target_size=(224, 224))
    # Convert the image to a numpy array
    img = image.img_to_array(loaded_img)
    # Reshape the image to add an extra dimension (batch size dimension)
    array_image = np.expand_dims(img, axis=0)
    # Normalize the image to the range [0, 1]
    array_image = array_image / 255.0
    return loaded_img, array_image


# Display The Image
def display_image(img, category, figsize=(5, 5)):
    "Give a loaded image and its category"
    plt.figure(figsize=figsize)
    plt.imshow(img)
    plt.title(f"Chosen Image Actual Category: {category}")
    plt.axis("off")
    plt.show()


def bring_predict_probas(predictions):
    class_labels = {
        "BABY_PRODUCTS": 0,
        "BEAUTY_HEALTH": 1,
        "CLOTHING_ACCESSORIES_JEWELLERY": 2,
        "ELECTRONICS": 3,
        "GROCERY": 4,
        "HOBBY_ARTS_STATIONERY": 5,
        "HOME_KITCHEN_TOOLS": 6,
        "PET_SUPPLIES": 7,
        "SPORTS_OUTDOOR": 8,
    }
    # Create a reverse mapping
    reverse_class_labels = {v: k for k, v in class_labels.items()}
    # Flatten the predictions array and sort the probabilities along with their indices
    predictions = predictions.flatten()
    sorted_indices = np.argsort(predictions)[::-1]  # Sort in descending order
    # Get sorted class labels and their corresponding probabilities
    sorted_class_labels = [reverse_class_labels[i] for i in sorted_indices]
    sorted_probabilities = np.round(predictions[sorted_indices], 2)
    return sorted_class_labels, sorted_probabilities


# Create a DataFrame
def create_dataframe(sorted_class_labels, sorted_probabilities):
    df = pd.DataFrame(
        {"Class": sorted_class_labels, "Probability": sorted_probabilities}
    )
    return df
