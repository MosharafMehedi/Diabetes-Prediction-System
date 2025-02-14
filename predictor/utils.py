# predictor/utils.py
import pickle
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import numpy as np

# Load the model, scaler, and feature names from the files
MODEL_PATH = './best_model.pkl'
SCALER_PATH = './scaler.pkl'
FEATURES_PATH = './features.pkl'

with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

with open(SCALER_PATH, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

with open(FEATURES_PATH, 'rb') as features_file:
    feature_names = pickle.load(features_file)

def preprocess(data):
    # Implement the preprocessing steps you used in your training pipeline
    gender = 1 if data['gender'] == 'male' else 0
    smoking_history = {
        'never': 0,
        'former': 1,
        'current': 2,
        'ever': 3,
        'not current': 4
    }[data['smoking_history']]

    input_data = {
        'gender_Male': gender,
        'age': data['age'],
        'hypertension': data['hypertension'],
        'heart_disease': data['heart_disease'],
        'smoking_history_ever': 0,
        'smoking_history_former': 0,
        'smoking_history_never': 0,
        'smoking_history_not current': 0,
        'smoking_history_current': 0,
        'bmi': data['bmi'],
        'HbA1c_level': data['HbA1c_level'],
        'blood_glucose_level': data['blood_glucose_level']
    }

    smoking_key = f"smoking_history_{data['smoking_history']}"
    if smoking_key in input_data:
        input_data[smoking_key] = 1

    # Ensure the order of features matches training
    input_data_ordered = [input_data[feature] for feature in feature_names if feature != 'diabetes']

    # Apply MinMax scaling
    columns_to_scale = [feature_names.index(col) for col in ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']]
    input_data_np = np.array([input_data_ordered])
    input_data_np[:, columns_to_scale] = scaler.transform(input_data_np[:, columns_to_scale])

    return input_data_np

def predict_diabetes(data):
    input_data = preprocess(data)
    prediction = model.predict(input_data)
    return 'Positive' if prediction[0] == 1 else 'Negative'

def generate_pdf(data, prediction):
    template = get_template('predictor/report_template.html')
    context = {'data': data, 'prediction': prediction}
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors <pre>' + html + '</pre>')
