# Generated by Django 4.1 on 2022-09-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_group_alter_group_slug_alter_group_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(max_length=25),
        ),
    ]
