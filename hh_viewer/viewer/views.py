from django.views.generic import ListView
from viewer.models import Vacancy

class VacancyListView(ListView):
    model = Vacancy
