from django.shortcuts import render
from django.http import HttpResponse
from .forms import PredictionForm
from .utils import predict_diabetes, generate_pdf
from django.contrib.auth.decorators import login_required

@login_required
def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            prediction = predict_diabetes(data)
            response = generate_pdf(data, prediction)
            return response
    else:
        form = PredictionForm()

    return render(request, 'predictor/predict.html', {'form': form})
