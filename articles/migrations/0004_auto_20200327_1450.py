# Generated by Django 3.0.4 on 2020-03-27 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20200327_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(error_messages={'required': '!!!!!!'}, max_length=140),
        ),
    ]
