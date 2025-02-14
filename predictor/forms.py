# predictor/forms.py
from django import forms

class PredictionForm(forms.Form):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    SMOKING_CHOICES = [('never', 'Never'), ('former', 'Former'), ('current', 'Current')]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    age = forms.IntegerField()
    hypertension = forms.BooleanField(required=False)
    heart_disease = forms.BooleanField(required=False)
    smoking_history = forms.ChoiceField(choices=SMOKING_CHOICES)
    bmi = forms.FloatField()
    HbA1c_level = forms.FloatField()
    blood_glucose_level = forms.FloatField()
