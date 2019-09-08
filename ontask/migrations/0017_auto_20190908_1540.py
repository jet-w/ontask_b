# Generated by Django 2.2.5 on 2019-09-08 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0016_scheduledaction_execute_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledaction',
            name='execute_until',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End of execution period (if executing multiple times)'),
        ),
    ]
