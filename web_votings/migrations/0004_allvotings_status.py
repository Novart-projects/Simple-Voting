# Generated by Django 3.1.5 on 2021-02-05 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_votings', '0003_usersanswers'),
    ]

    operations = [
        migrations.AddField(
            model_name='allvotings',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
