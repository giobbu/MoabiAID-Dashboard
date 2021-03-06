# Generated by Django 2.2 on 2019-12-20 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20190930_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='street',
            name='commune',
        ),
        migrations.AddField(
            model_name='street',
            name='bridge',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='street',
            name='category',
            field=models.CharField(default='street', max_length=28),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='street',
            name='one_way',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='street',
            name='tunnel',
            field=models.BooleanField(default=False),
        ),
    ]
