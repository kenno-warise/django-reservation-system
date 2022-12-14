# Generated by Django 3.2.15 on 2022-09-27 04:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='comment',
            field=models.TextField(verbose_name='備考欄'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='メールアドレス'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='name',
            field=models.CharField(max_length=100, verbose_name='氏名'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='reserve_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reserve.shop', verbose_name='予約日'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='reserve_num',
            field=models.IntegerField(default=1, verbose_name='予約人数'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='reserve_time',
            field=models.TimeField(verbose_name='予約時間'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='tel',
            field=models.CharField(max_length=20, verbose_name='電話番号'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='end_time',
            field=models.TimeField(verbose_name='閉店時間'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='max_reserve_num',
            field=models.IntegerField(verbose_name='１時間当たりの予約上限人数'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='reservable_date',
            field=models.IntegerField(verbose_name='予約可能日'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='start_time',
            field=models.TimeField(verbose_name='開店時間'),
        ),
    ]
