# Generated by Django 2.2.4 on 2019-08-22 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0007_auto_20190822_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='body',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_body', to='myblog.Content', verbose_name='博文'),
        ),
    ]
