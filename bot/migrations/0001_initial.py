# Generated by Django 4.0.4 on 2022-05-23 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Telegram nickname', max_length=200)),
                ('tg_id', models.PositiveBigIntegerField(help_text='Telegram ID')),
                ('username', models.CharField(default=None, help_text='Telegram username', max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fish', models.CharField(help_text='Familiya Ism Sharif', max_length=200)),
                ('birth_date', models.CharField(help_text="Tug'ilgan kun: dd.mm.yyyy shaklda", max_length=50)),
                ('adress', models.CharField(help_text="To'liq manzil: viloyat, mahalla, ko'cha, xonadon", max_length=200)),
                ('tel', models.PositiveBigIntegerField(help_text='Telefon raqami: + siz', max_length=12)),
                ('files', models.TextField(help_text="JSON formatdagi telegram medialari ro'yxati")),
                ('tg_user', models.OneToOneField(help_text='Telegram user', on_delete=django.db.models.deletion.CASCADE, to='bot.tguser')),
            ],
        ),
    ]