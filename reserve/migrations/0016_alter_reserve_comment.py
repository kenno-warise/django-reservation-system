# Generated by Django 3.2.15 on 2022-09-29 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0015_auto_20220929_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='comment',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='備考欄'),
        ),
    ]
