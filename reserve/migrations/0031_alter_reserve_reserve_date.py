# Generated by Django 3.2.15 on 2022-10-08 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0030_alter_reserve_reserve_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='reserve_date',
            field=models.DateField(choices=[('1', '1'), ('2', '2')], max_length=20, verbose_name='予約日'),
        ),
    ]
