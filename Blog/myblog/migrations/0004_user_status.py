# Generated by Django 2.2.4 on 2019-08-21 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0003_auto_20190820_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '离线'), (1, '在线')], default=0, verbose_name='用户状态'),
        ),
    ]
