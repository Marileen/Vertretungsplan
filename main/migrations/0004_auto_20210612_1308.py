# Generated by Django 3.2.4 on 2021-06-12 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='telefon',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
