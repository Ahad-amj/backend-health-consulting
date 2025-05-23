# Generated by Django 5.2 on 2025-05-04 07:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_doctor_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='doctor',
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('prescription', models.TextField(blank=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='main_app.doctor')),
                ('medicines', models.ManyToManyField(blank=True, related_name='patients', to='main_app.medicine')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
