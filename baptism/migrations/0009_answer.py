# Generated by Django 5.1.3 on 2024-12-17 09:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baptism', '0008_alter_fieldtable_choice_alter_fieldtable_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.AutoField(primary_key=True, serialize=False)),
                ('q_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('field_id', models.IntegerField()),
                ('text_answer', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=10)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
