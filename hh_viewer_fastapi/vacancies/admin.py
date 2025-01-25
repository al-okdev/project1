from fastadmin import TortoiseModelAdmin, register
from vacancies.models import Vacancy 

@register(Vacancy)
class VacancyAdmin(TortoiseModelAdmin):
    list_display = ("id", "experiece", "price", "competentions")