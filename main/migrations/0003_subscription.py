# Generated by Django 3.2.4 on 2021-06-12 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_subscriber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.school')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subscriber')),
            ],
        ),
    ]