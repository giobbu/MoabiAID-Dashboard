# Generated by Django 2.2 on 2020-04-24 16:12

from django.db import migrations
from django.db.models import Count, Max


def remove_dup_streets(apps, schema_editor):
    Street = apps.get_model('dashboard', 'Street')

    duplicates = (
    Street.objects.values('name')
    .order_by()
    .annotate(max_id=Max('id'), count_id=Count('id'))
    .filter(count_id__gt=1))

    for duplicate in duplicates:
        (
            Street.objects
            .filter(name=duplicate['name'])
            .exclude(id=duplicate['max_id'])
            .delete()
        )

class Migration(migrations.Migration):

    dependencies=[
        ('dashboard', '0012_auto_20191220_1617'),
    ]

    operations=[
        migrations.RemoveField(
            model_name='streetsegment',
            name='parent_segment',
        ),
        migrations.RemoveField(
            model_name='streetsegment',
            name='street',
        ),
        migrations.RunPython(remove_dup_streets),
        migrations.AlterUniqueTogether(
            name='street',
            unique_together={('name', 'commune')},
        ),
        migrations.DeleteModel(
            name='RoadWorks',
        ),
        migrations.DeleteModel(
            name='StreetSegment',
        ),
    ]
