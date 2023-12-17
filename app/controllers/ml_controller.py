from flask import request, jsonify
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
from io import BytesIO
from app.config.config import db

# Load model
# Mendapatkan path ke direktori 'controllers'
controllers_dir = os.path.dirname(os.path.abspath(__file__))

# Mendapatkan path ke direktori 'app'
app_dir = os.path.dirname(controllers_dir)

# Mendapatkan path ke direktori 'models/1'
model_path = os.path.join(app_dir, 'models', '1')

model = load_model(model_path)


def predict():
    # Get the uploaded image file
    file = request.files['image']

    # Load and preprocess the image
    file_data = BytesIO(file.read())
    img = load_img(file_data, target_size=(299, 299))
    x = img_to_array(img)
    x /= 255. # Normalize image
    x = np.expand_dims(x, axis=0)

    # Make predictions
    predictions = model.predict(x)

    # Get the class with the highest probability
    predicted_class = np.argmax(predictions[0])

    # Define class labels based on your model
    classes_outputs = ['2', '1', '0']
    predicted_label = classes_outputs[predicted_class]
    label_response = str(predicted_label)

    print("Predicted Label:", label_response)

    # Mengambil koleksi ml_response dari Firestore
    ml_ref = db.collection("ml_response").document(label_response)

    # mendapatkan snapshot
    ml_snapshot = ml_ref.get()

    if ml_snapshot.exists:
        output_data = ml_snapshot.to_dict()
        response = {
            'title': output_data.get('title', ''),
            'paragraf_1': output_data.get('paragraf_1', ''),
            'paragraf_2': output_data.get('paragraf_2', ''),
            'paragraf_3': output_data.get('paragraf_3', ''),
            'paragraf_4': output_data.get('paragraf_4', ''),
            'paragraf_5': output_data.get('paragraf_5', ''),
            'paragraf_6': output_data.get('paragraf_6', '')
        }
        return jsonify(response), 200
    else:
        # Handle the case when the document does not exist
        return jsonify({'error': 'Document not found'}), 404
