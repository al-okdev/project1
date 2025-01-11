from tortoise.models import Model
from tortoise import fields

class Vacancy(Model):
    class Meta:
        table = "vacancies"

    uuid = fields.UUIDField(primary_key=True)
    experiece = fields.CharField(max_length=50)
    price = fields.IntField()
    competentions = fields.TextField(null=True)

    def __str__(self):
        return self.uuid