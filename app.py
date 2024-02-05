from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)

# Load the pre-trained MobileNetV2 model
model = tf.keras.applications.MobileNetV2(weights='imagenet', input_shape=(224, 224, 3))

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

def predict_image_class(image_array):
    predictions = model.predict(image_array)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions.numpy())
    top_prediction = decoded_predictions[0][0]
    return top_prediction[1]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    image_path = 'static/uploads/uploaded_image.jpg'
    file.save(image_path)

    image_array = preprocess_image(image_path)
    predicted_class = predict_image_class(image_array)

    return jsonify({'result': predicted_class})

if __name__ == '__main__':
    app.run(debug=True)
