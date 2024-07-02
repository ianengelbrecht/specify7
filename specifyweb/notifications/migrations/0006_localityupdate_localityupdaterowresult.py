# Generated by Django 3.2.15 on 2024-06-18 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('specify', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0005_auto_20240530_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalityUpdate',
            fields=[
                ('taskid', models.CharField(max_length=256)),
                ('status', models.CharField(max_length=256)),
                ('timestampcreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestampmodified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(db_column='LocalityUpdateID', primary_key=True, serialize=False, verbose_name='localityupdateid')),
                ('collection', models.ForeignKey(db_column='CollectionID', on_delete=django.db.models.deletion.CASCADE, to='specify.collection')),
                ('createdbyagent', models.ForeignKey(db_column='CreatedByAgentID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='specify.agent')),
                ('modifiedbyagent', models.ForeignKey(db_column='ModifiedByAgentID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='specify.agent')),
                ('recordset', models.ForeignKey(blank=True, db_column='RecordSetID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='specify.recordset')),
                ('specifyuser', models.ForeignKey(db_column='SpecifyUserID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'localityupdate',
            },
        ),
        migrations.CreateModel(
            name='LocalityUpdateRowResult',
            fields=[
                ('id', models.AutoField(db_column='LocalityUpdateRowResultID', primary_key=True, serialize=False, verbose_name='localityupdaterowresultid')),
                ('rownumber', models.IntegerField()),
                ('result', models.JSONField()),
                ('localityupdate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', db_column='LocalityUpdateID', to='notifications.localityupdate')),
            ],
            options={
                'db_table': 'localityupdaterowresult',
            },
        ),
    ]
