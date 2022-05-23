from django.db import models

# Create your models here.
class TgUser(models.Model):
    full_name = models.CharField(max_length=200, null=False, help_text="Telegram nickname")
    tg_id = models.PositiveBigIntegerField(null=False, help_text="Telegram ID")
    username = models.CharField(max_length=100, unique=True, null=True, default=None, help_text="Telegram username")

class Contestant(models.Model):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE, help_text="Telegram user", unique=True)
    fish = models.CharField(max_length=200, help_text="Familiya Ism Sharif")
    birth_date = models.CharField(max_length=50. help_text="Tug'ilgan kun: dd.mm.yyyy shaklda")
    adress = models.CharField(max_length=200, help_text="To'liq manzil: viloyat, mahalla, ko'cha, xonadon")
    tel = models.PositiveBigIntegerField(max_length=12, help_text="Telefon raqami: + siz")
    files = models.TextField(null=False, help_text="JSON formatdagi telegram medialari ro'yxati")
