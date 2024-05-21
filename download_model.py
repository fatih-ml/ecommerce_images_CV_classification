import gdown
import os


def download_model(drive_url, output_path):
    gdown.download(drive_url, output_path, quiet=False)


if __name__ == "__main__":
    # Google Drive shareable link (file ID extracted and formatted)
    drive_url = "https://drive.google.com/uc?id=1S55B7V3WhETRw3NSjRci65GGDbPVw-bE"

    # Local path where the model will be saved
    output_path = "mobilenetv2_18K_model.h5"

    if not os.path.exists(output_path):
        print("Downloading model...")
        download_model(drive_url, output_path)
    else:
        print("Model already exists. Skipping download.")
