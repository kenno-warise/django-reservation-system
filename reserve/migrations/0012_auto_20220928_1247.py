# Generated by Django 3.2.15 on 2022-09-28 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0011_auto_20220928_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='reserve_date',
            field=models.CharField(choices=[('1', '6/1'), ('2', '6/2'), ('3', '6/3')], max_length=20, verbose_name='予約日'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='reserve_num',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=10, verbose_name='予約人数'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='reserve_time',
            field=models.CharField(choices=[('1', '14:00'), ('2', '15:00'), ('3', '16:00')], max_length=10, verbose_name='予約時間'),
        ),
    ]
