from django.urls import path
from .views import VacancyListView

urlpatterns = [
    path('viewer_hh/', VacancyListView.as_view()),
]