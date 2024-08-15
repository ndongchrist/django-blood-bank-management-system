# Generated by Django 4.2.11 on 2024-08-15 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_appointment_center_remove_appointment_donor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('cancelled', 'Cancelled'), ('pending', 'pending')], default='pending', max_length=50, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('cancelled', 'Cancelled'), ('pending', 'pending')], default='pending', max_length=50, verbose_name='Status'),
        ),
    ]