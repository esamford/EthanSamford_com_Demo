# Generated by Django 4.0.4 on 2022-06-17 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_alter_projectimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimage',
            name='image',
            field=models.ImageField(upload_to='static/uploaded_files/project_images/None_%Y_%m_%d_%H_%M_%S'),
        ),
    ]
