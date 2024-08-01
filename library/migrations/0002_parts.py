# Generated by Django 5.0.7 on 2024-08-01 10:40

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument', models.CharField(max_length=100)),
                ('part_number', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('file', models.FileField(upload_to='parts/')),
                ('piece', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.piece')),
            ],
        ),
    ]
