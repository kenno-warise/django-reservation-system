# Generated by Django 3.2.15 on 2022-10-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0032_alter_reserve_reserve_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='email',
            field=models.EmailField(max_length=100, verbose_name='メールアドレス'),
        ),
    ]