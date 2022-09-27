# Generated by Django 3.2.15 on 2022-09-27 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0003_alter_reserve_reserve_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='reserve_num',
            field=models.CharField(choices=[('', '人数'), (1, '1'), (2, '2'), (3, '3')], max_length=10, verbose_name='予約人数'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='reserve_time',
            field=models.CharField(choices=[('', '予約時間'), (1, '14:00'), (2, '15:00'), (3, '16:00')], max_length=10, verbose_name='予約時間'),
        ),
    ]
