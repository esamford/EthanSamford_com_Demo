# Generated by Django 4.0.4 on 2022-06-23 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_rename_save_path_projectimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimage',
            name='display_order',
            field=models.PositiveIntegerField(default=0, help_text='Lower values will be shown before higher values.'),
        ),
    ]
