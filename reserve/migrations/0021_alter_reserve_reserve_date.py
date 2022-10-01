# Generated by Django 3.2.15 on 2022-09-30 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0020_auto_20220930_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='reserve_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reserve.shop', verbose_name='予約日'),
        ),
    ]