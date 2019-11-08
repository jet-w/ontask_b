# Generated by Django 2.2.5 on 2019-10-16 12:58

from collections import Counter

from django.db import migrations, models

from ontask.dataops.sql import db_rename_column
from ontask.models import Workflow


def _make_unique_new_names(name_list):
    """Create a list if new names that are unique

    :param name_list: List of names to make unique
    :return: List of names that are unique
    """
    if len(name_list) == len(set(name_list)):
        return name_list

    cntr = Counter(name_list)
    max_rep = max(cntr.values())

    digits = {}
    for name, appears in cntr.items():
        if appears == 1:
            continue
        dig = 1
        while 10 ** dig < appears:
            dig += 1
        digits[name] = dig

    new_names = []
    for col in name_list:
        appears = cntr[col]
        if appears == 1:
            new_names.append(col)
            continue

        new_names.append(col[:-digits[col]] + str(appears).zfill(digits[col]))
        cntr[col] = cntr[col] - 1

    return new_names


def trim_column_names(apps, schema_editor):
    """
    Traverse all workshops and trim column names to 63 characters.

    :param apps:
    :param schema_editor:
    :return:
    """
    for wflow in Workflow.objects.all():
        rename_cols = []
        for column in wflow.columns.all():
            if len(column.name) <= 63:
                continue
            rename_cols.append(column)

        if not rename_cols:
            continue

        new_names = _make_unique_new_names(
            [col.name[:63] for col in rename_cols])

        for col, new_name in zip(rename_cols, new_names):
            if col.name[:63] == new_name:
                continue

            db_rename_column(
                wflow.get_data_frame_table_name(),
                col.name[:63],
                new_name)

            col.name = new_name
            col.save()


def reverse_migration(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0047_auto_20191007_2118'),
    ]

    operations = [
        migrations.RunPython(
            trim_column_names,
            reverse_code=reverse_migration),
        migrations.AlterField(
            model_name='column',
            name='name',
            field=models.CharField(max_length=63, verbose_name='column name'),
        ),
    ]
