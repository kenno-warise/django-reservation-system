# Generated by Django 3.2.15 on 2022-10-05 04:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0027_auto_20221005_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='reservable_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reserve.reservabledate', verbose_name='予約可能日'),
        ),
    ]
