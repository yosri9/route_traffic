# Generated by Django 3.2.2 on 2021-05-13 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AverageData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_node_altitude', models.FloatField(null=True)),
                ('first_node_longitude', models.FloatField(null=True)),
                ('end_node_altitude', models.FloatField(null=True)),
                ('end_node_longitude', models.FloatField(null=True)),
                ('distance_between_end_node_and_point', models.FloatField(null=True)),
                ('averageSpeed', models.CharField(max_length=100, null=True)),
            ],
            options={
                'unique_together': {('id',)},
            },
        ),
    ]
