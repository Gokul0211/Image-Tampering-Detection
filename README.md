# Image-Tampering-Detection

This project focuses on detecting image tampering using Enhanced Local Binary Patterns (ELBP) and Convolutional Neural Networks (CNNs). It aims to identify and localize manipulated regions in digital images, ensuring authenticity and integrity.

---

## Project Structure

* `image-forgery-detection-using-ela-and-cnn.ipynb`: A Jupyter Notebook implementing the ELBP and CNN-based tampering detection model.
* `main.py`: The main script to run the tampering detection process.
* `pyhton.py`: An auxiliary Python script.
* `requirements.txt`: Lists the necessary Python libraries and dependencies.
* `Main final.pdf`: A PDF detailing the project's methodology and results.
* `images/`: Directory containing sample images used for testing.
* `static/`: Directory for static files.
* `__pycache__/`: Compiled Python files.

---

## Requirements

Install the required Python libraries using:

```bash
pip install -r requirements.txt
```

Key libraries include:

* `opencv-python`
* `numpy`
* `tensorflow`
* `matplotlib`
* `scikit-learn`
* `pillow`

---

## Usage

### 1. Run the Jupyter Notebook

```bash
jupyter notebook image-forgery-detection-using-ela-and-cnn.ipynb
```

Follow the notebook to load images, apply ELBP, and train the CNN model.

### 2. Run the Main Script

```bash
python main.py
```

Ensure necessary input images are available before running the script.

---

## How It Works

1. **Enhanced Local Binary Patterns (ELBP)**: Extracts texture features from images to highlight potential tampered regions.
2. **Convolutional Neural Network (CNN)**: Trains on extracted features to classify regions as tampered or authentic.
3. **Detection & Localization**: Identifies and marks manipulated areas within images.

---

## Documentation

Refer to `Main final.pdf` for detailed methodology, objectives, and results.

---

## Sample Images

The `images/` directory contains sample images used for testing the tampering detection model.

---

## Contact

* **GitHub**: [Gokul0211](https://github.com/Gokul0211)
* **Email**: [gokuliyer111@gmail.com](mailto:gokuliyer111@gmail.com)
