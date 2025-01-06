from django.urls import path
from . import views
from .views import VacancyListView

urlpatterns = [
    path('viewer_hh/', VacancyListView.as_view()),
]