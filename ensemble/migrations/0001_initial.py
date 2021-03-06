# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-29 17:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('simulation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ensemble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_id', models.CharField(default=None, max_length=256, unique=True)),
                ('iteration', models.IntegerField(default=0, verbose_name='Iteration')),
                ('name', models.CharField(max_length=256)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(default=None, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Realisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iens', models.IntegerField(verbose_name='Realisation')),
                ('ensemble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ensemble.Ensemble')),
                ('simulation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='simulation.Simulation')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='realisation',
            unique_together=set([('iens', 'ensemble')]),
        ),
    ]
