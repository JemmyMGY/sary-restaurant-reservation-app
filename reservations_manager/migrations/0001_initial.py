# Generated by Django 4.1.2 on 2023-03-26 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tables_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationModel',
            fields=[
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('reservation_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables_manager.tablemodel')),
            ],
        ),
    ]
