# Generated by Django 4.0.4 on 2022-06-17 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_alter_project_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectimage',
            name='name',
            field=models.CharField(default='temp', max_length=100),
            preserve_default=False,
        ),
    ]
