# Generated by Django 4.0.4 on 2022-06-17 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_alter_projectimage_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectimage',
            old_name='image',
            new_name='image_path',
        ),
    ]