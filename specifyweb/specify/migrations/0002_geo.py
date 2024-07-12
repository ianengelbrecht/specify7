# Generated by Django 3.2.15 on 2024-06-21 21:56
# TODO: Finish editing this migration for the new app structure

from django.db import migrations, models
from django.db.models import Subquery, OuterRef
import django.db.models.deletion
import django.utils.timezone
import specifyweb.specify.models
from specifyweb.specify.models import (
    protect_with_blockers,
    Discipline,
    Collectionobject,
    CollectionObjectType,
    Collection,
)

# Migrations Operations Order:
# 1. Create CollectionObjectType
# 2. Add CollectionObjectType (coType) realtionship to CollectionObject
# 3. Add hasreferencecatalognumber field to CollectionObject
# 4. Create default collection object types based on each discipline
# 5. Create new default taxon trees and ranks
# 6. Create CollectionObjectGroup
# 7. Create CollectionObjectGroupJoin

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('specify', '0001_initial'),
    ]

    def create_default_collection_types(apps, schema_editor):
        # Create default collection types for each collection, named after the discipline
        for collection in Collection.objects.all():
            discipline = collection.discipline
            discipline_name = discipline.name
            cot, created = CollectionObjectType.objects.get_or_create(
                name=discipline_name,
                collection=collection,
                taxontreedef=discipline.taxontreedef
            )
            # Update CollectionObjects' collectionobjecttype for the discipline
            Collectionobject.objects.filter(collection=collection).update(collectionobjecttype=cot)
            collection.collectionobjecttype = cot
            collection.save()

    def revert_default_collection_types(apps, schema_editor):
        # Reverse handeled by table deletion.
        pass

    operations = [
        migrations.CreateModel(
            name='CollectionObjectType',
            fields=[
                ('id', models.AutoField(db_column='CollectionObjectTypeID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=255)),
                ('version', models.IntegerField(blank=True, db_column='Version', default=0, null=True)),
                ('timestampcreated', models.DateTimeField(db_column='TimestampCreated', default=django.utils.timezone.now)),
                ('timestampmodified', models.DateTimeField(blank=True, db_column='TimestampModified', default=django.utils.timezone.now, null=True)),
                ('text1', models.TextField(blank=True, db_column='Text1', null=True)),
                ('text2', models.TextField(blank=True, db_column='Text2', null=True)),
                ('text3', models.TextField(blank=True, db_column='Text3', null=True)),
                ('collection', models.ForeignKey(db_column='CollectionID', on_delete=protect_with_blockers, related_name='cotypes', to='specify.collection')),
                ('createdbyagent', models.ForeignKey(db_column='CreatedByAgentID', null=True, on_delete=protect_with_blockers, related_name='+', to='specify.agent')),
                ('modifiedbyagent', models.ForeignKey(db_column='ModifiedByAgentID', null=True, on_delete=protect_with_blockers, related_name='+', to='specify.agent')),
                ('taxontreedef', models.ForeignKey(db_column='TaxonTreeDefID', on_delete=protect_with_blockers, related_name='cotypes', to='specify.taxontreedef')),
            ],
            options={
                'db_table': 'collectionobjecttype',
                'ordering': (),
            },
        ),
        migrations.CreateModel(
            name='CollectionObjectGroupType',
            fields=[
                ('id', models.AutoField(db_column='COGTypeID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=255, null=False)),
                ('cogtype', models.CharField(blank=True, db_column='COGType', max_length=255, null=False)),
                ('version', models.IntegerField(blank=True, db_column='Version', default=0, null=True)),
                ('timestampcreated', models.DateTimeField(db_column='TimestampCreated', default=django.utils.timezone.now)),
                ('timestampmodified', models.DateTimeField(blank=True, db_column='TimestampModified', default=django.utils.timezone.now, null=True)),
                ('collection', models.ForeignKey(db_column='CollectionID', on_delete=protect_with_blockers, related_name='cogtypes', to='specify.collection')),
                ('createdbyagent', models.ForeignKey(db_column='CreatedByAgentID', null=True, on_delete=protect_with_blockers, related_name='+', to='specify.agent')),
                ('modifiedbyagent', models.ForeignKey(db_column='ModifiedByAgentID', null=True, on_delete=protect_with_blockers, related_name='+', to='specify.agent')),
            ],
            options={
                'db_table': 'collectionobjectgrouptype',
                'ordering': (),
            },
        ),
        migrations.AddField(
            model_name='collectionobject',
            name='collectionobjecttype',
            field=models.ForeignKey(db_column='CollectionObjectTypeID', null=True, on_delete=models.SET_NULL, related_name='collectionobjects', to='specify.collectionobjecttype'),
        ),
        migrations.AddField(
            model_name='collection',
            name='collectionobjecttype',
            field=models.ForeignKey(db_column='CollectionObjectTypeID', null=True, on_delete=protect_with_blockers, related_name='collections', to='specify.collectionobjecttype'),
        ),
        migrations.RunPython(create_default_collection_types, revert_default_collection_types),
        migrations.CreateModel(
            name='CollectionObjectGroup',
            fields=[
                ('id', models.AutoField(db_column='collectionobjectgroupid', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('description', models.TextField(blank=True, db_column='Description', null=True)),
                ('igsn', models.CharField(blank=True, db_column='IGSN', max_length=255, null=True)),
                ('guid', models.CharField(blank=True, db_column='GUID', max_length=255, null=True)),
                ('integer1', models.IntegerField(blank=True, db_column='Integer1', null=True)),
                ('integer2', models.IntegerField(blank=True, db_column='Integer2', null=True)),
                ('integer3', models.IntegerField(blank=True, db_column='Integer3', null=True)),
                ('decimal1', models.DecimalField(blank=True, db_column='Decimal1', decimal_places=10, max_digits=22, null=True)),
                ('decimal2', models.DecimalField(blank=True, db_column='Decimal2', decimal_places=10, max_digits=22, null=True)),
                ('decimal3', models.DecimalField(blank=True, db_column='Decimal3', decimal_places=10, max_digits=22, null=True)),
                ('text1', models.TextField(blank=True, db_column='Text1', null=True)),
                ('text2', models.TextField(blank=True, db_column='Text2', null=True)),
                ('text3', models.TextField(blank=True, db_column='Text3', null=True)),
                ('yesno1', models.BooleanField(blank=True, db_column='YesNo1', null=True)),
                ('yesno2', models.BooleanField(blank=True, db_column='YesNo2', null=True)),
                ('yesno3', models.BooleanField(blank=True, db_column='YesNo3', null=True)),
                ('version', models.IntegerField(blank=True, db_column='Version', default=0, null=True)),
                ('timestampcreated', models.DateTimeField(db_column='TimestampCreated', default=django.utils.timezone.now)),
                ('timestampmodified', models.DateTimeField(blank=True, db_column='TimestampModified', default=django.utils.timezone.now, null=True)),
                ('collection', models.ForeignKey(db_column='CollectionID', on_delete=protect_with_blockers, related_name='collectionobjectgroups', to='specify.collection')),
                ('cogtype', models.ForeignKey(db_column='COGTypeID', on_delete=protect_with_blockers, related_name='collectionobjectgroups', to='specify.collectionobjectgrouptype')),
                ('createdbyagent', models.ForeignKey(db_column='CreatedByAgentID', null=True, on_delete=protect_with_blockers, related_name='+', to='specify.agent')),
                ('modifiedbyagent', models.ForeignKey(db_column='ModifiedByAgentID', null=True, on_delete=protect_with_blockers, related_name='+', to='specify.agent')),
            ],
            options={
                'db_table': 'collectionobjectgroup',
                'ordering': (),
            },
        ),
        migrations.CreateModel(
            name='CollectionObjectGroupJoin', # add as dependant to collection object group
            fields=[
                ('id', models.AutoField(db_column='collectionobjectgroupjoinid', primary_key=True, serialize=False)),
                ('isprimary', models.BooleanField(blank=True, db_column='IsPrimary', null=True)),
                ('issubstrate', models.BooleanField(blank=True, db_column='IsSubstrate', null=True)),
                ('precedence', models.SmallIntegerField(blank=True, db_column='Precedence', null=True)),
                ('version', models.IntegerField(blank=True, db_column='Version', default=0, null=True)),
                ('timestampcreated', models.DateTimeField(db_column='TimestampCreated', default=django.utils.timezone.now)),
                ('timestampmodified', models.DateTimeField(blank=True, db_column='TimestampModified', default=django.utils.timezone.now, null=True)),
                ('text1', models.TextField(blank=True, db_column='Text1', null=True)),
                ('text2', models.TextField(blank=True, db_column='Text2', null=True)),
                ('text3', models.TextField(blank=True, db_column='Text3', null=True)),
                ('integer1', models.IntegerField(blank=True, db_column='Integer1', null=True)),
                ('integer2', models.IntegerField(blank=True, db_column='Integer2', null=True)),
                ('integer3', models.IntegerField(blank=True, db_column='Integer3', null=True)),
                ('yesno1', models.BooleanField(blank=True, db_column='YesNo1', null=True)),
                ('yesno2', models.BooleanField(blank=True, db_column='YesNo2', null=True)),
                ('yesno3', models.BooleanField(blank=True, db_column='YesNo3', null=True)),
                ('parentcog', models.ForeignKey(db_column='ParentCOGID', on_delete=django.db.models.deletion.CASCADE, related_name='parentcojos', to='specify.collectionobjectgroup')),
                ('childcog', models.OneToOneField(db_column='ChildCOGID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cojo', to='specify.collectionobjectgroup')),
                ('childco', models.OneToOneField(db_column='ChildCOID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cojo', to='specify.collectionobject')),
            ],
            options={
                'db_table': 'collectionobjectgroupjoin',
                'ordering': (),
                'unique_together': (('parentcog', 'childco'),),
            },
        ),
    ]
