from django.urls import path
from . import views


urlpatterns = [
    path('predict/', views.PredictView.as_view(), name='predict'),
    path('analysis/', views.AnalysisView.as_view(), name='analysis')
]
