# Generated by Django 4.0.4 on 2022-05-23 20:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='work_or_study',
            field=models.CharField(default=django.utils.timezone.now, help_text="(Ish joyi va lavozimi) yoki (O'qish joyi va bosqichi)", max_length=200),
            preserve_default=False,
        ),
    ]
