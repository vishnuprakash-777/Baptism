# Generated by Django 5.1.3 on 2024-12-23 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baptism', '0021_alter_question_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='order_id',
            field=models.IntegerField(unique=True),
        ),
    ]
