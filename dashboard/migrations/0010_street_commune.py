# Generated by Django 2.2 on 2019-12-20 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20191220_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='street',
            name='commune',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='streets', to='dashboard.Commune'),
            preserve_default=False,
        ),
    ]
