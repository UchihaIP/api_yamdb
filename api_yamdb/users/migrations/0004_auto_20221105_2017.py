# Generated by Django 2.2.16 on 2022-11-05 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20221105_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=5714, max_length=5, null=True),
        ),
    ]
