# Generated by Django 3.1.5 on 2021-02-06 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_votings', '0005_complaint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='ans',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
