# Generated by Django 4.2.3 on 2023-10-01 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_alter_laptop_options_alter_laptop_release_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='amount_hdd',
            field=models.PositiveSmallIntegerField(help_text='Capacity in GB'),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='amount_ram',
            field=models.PositiveSmallIntegerField(help_text='Capacity in GB'),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='release_year',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
