# Generated by Django 2.2.4 on 2019-08-22 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0008_auto_20190822_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='body',
            field=models.TextField(blank=True, null=True, verbose_name='博文'),
        ),
    ]
