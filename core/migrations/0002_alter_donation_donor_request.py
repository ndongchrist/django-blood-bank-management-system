# Generated by Django 5.1 on 2024-08-12 07:02

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(choices=[('DONOR', 'Donor'), ('PATIENT', 'Patient')], on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, default=dict, null=True, verbose_name='meta data')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Deleted')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Time Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Time Modified')),
                ('date', models.DateField()),
                ('volume', models.PositiveIntegerField()),
                ('blood_group', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=50, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('user_requesting', models.ForeignKey(limit_choices_to={'user_type': 'donor'}, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
