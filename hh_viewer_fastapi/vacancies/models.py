from tortoise.models import Model
from tortoise import fields

from uuid import UUID
import bcrypt
from fastadmin import TortoiseModelAdmin, register

class Vacancy(Model):
    class Meta:
        table = "vacancies"

    id = fields.UUIDField(primary_key=True)
    experiece = fields.CharField(max_length=50)
    price = fields.IntField()
    competentions = fields.TextField(null=True)

    def __str__(self):
        return self.id
    
@register(Vacancy)
class VacancyAdmin(TortoiseModelAdmin):
    list_display = ("id", "experiece", "price", "competentions")

class User(Model):
    username = fields.CharField(max_length=255, unique=True)
    hash_password = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=False)

    def __str__(self):
        return self.username


@register(User)
class UserAdmin(TortoiseModelAdmin):
    exclude = ("hash_password",)
    list_display = ("id", "username", "is_superuser", "is_active")
    list_display_links = ("id", "username")
    list_filter = ("id", "username", "is_superuser", "is_active")
    search_fields = ("username",)

    async def authenticate(self, username: str, password: str) -> UUID | int | None:
        user = await User.filter(username=username, is_superuser=True).first()
        if not user:
            return None
        if not bcrypt.checkpw(password.encode(), user.hash_password.encode()):
            return None
        return user.id