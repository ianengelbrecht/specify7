# Generated by Django 3.2.15 on 2024-06-21 21:56
# TODO: Finish editing this migration for the new app structure

from django.db import migrations, models
from django.db.models import Subquery, OuterRef
import django.db.models.deletion
import django.utils.timezone
import specifyweb.specify.models
from specifyweb.specify.models import (
    Taxontreedef,
    Taxontreedefitem,
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
        # Create default collection types for each discipline
        for discipline in Discipline.objects.all():
            discipline_name = discipline.name
            if CollectionObjectType.objects.filter(name=discipline_name).exists():
                continue
            cot = CollectionObjectType.objects.create(
                name=discipline_name,
                isdefault=True,
                collection = Collection.objects.filter(discipline=discipline).first(),
                taxontreedef=discipline.taxontreedef,
            )
            cot.save()

        # Iteratively update CollectionObjects' collectionobjecttype for each discipline in a bulk operation
        for discipline in Discipline.objects.all():
            discipline_name = discipline.name
            cot = CollectionObjectType.objects.get(name=discipline_name)
            (Collectionobject.objects
                .filter(collection__discipline=discipline)
                .update(cotype=cot))

    operations = [
        migrations.CreateModel(
            name='CollectionObjectType',
            fields=[
                ('id', models.AutoField(db_column='CollectionObjectTypeID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=255)),
                ('isloanable', models.BooleanField(blank=True, db_column='IsLoanable', null=True)),
                ('isdefault', models.BooleanField(blank=True, db_column='IsDefault', null=False, default=False)),
                ('version', models.IntegerField(blank=True, db_column='Version', default=0, null=True)),
                ('timestampcreated', models.DateTimeField(db_column='TimestampCreated', default=django.utils.timezone.now)),
                ('timestampmodified', models.DateTimeField(blank=True, db_column='TimestampModified', default=django.utils.timezone.now, null=True)),
                ('text1', models.TextField(blank=True, db_column='Text1', null=True)),
                ('text2', models.TextField(blank=True, db_column='Text2', null=True)),
                ('text3', models.TextField(blank=True, db_column='Text3', null=True)),
                ('collection', models.ForeignKey(db_column='CollectionID', on_delete=specifyweb.specify.models.protect_with_blockers, related_name='collectionobjecttypes', to='specify.collection')),
                ('createdbyagent', models.ForeignKey(db_column='CreatedByAgentID', null=True, on_delete=specifyweb.specify.models.protect_with_blockers, related_name='+', to='specify.agent')),
                ('modifiedbyagent', models.ForeignKey(db_column='ModifiedByAgentID', null=True, on_delete=specifyweb.specify.models.protect_with_blockers, related_name='+', to='specify.agent')),
                ('taxontreedef', models.ForeignKey(db_column='TaxonTreeDefID', on_delete=specifyweb.specify.models.protect_with_blockers, related_name='collectionobjecttypes', to='specify.taxontreedef')),
            ],
            options={
                'db_table': 'collectionobjecttype',
                'ordering': (),
                'unique_together': (('collection', 'isdefault'),),
            },
        ),
        migrations.AddField(
            model_name='collectionobject',
            name='cotype',
            field=models.ForeignKey(db_column='COTypeID', null=True, on_delete=models.SET_NULL, related_name='collectionobjects', to='specify.collectionobjecttype'),
        ),
        migrations.AddField(
            model_name='collectionobject',
            name='hasreferencecatalognumber',
            field=models.BooleanField(blank=True, db_column='HasReferenceCatalogNumber', default=False, null=True),
        ),
        migrations.RunPython(create_default_collection_types), # reverse handeled by table deletion
        migrations.CreateModel(
            name='CollectionObjectGroup',
            fields=[
                ('id', models.AutoField(db_column='collectionobjectgroupid', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('description', models.TextField(blank=True, db_column='Description', null=True)),
                ('igsn', models.CharField(blank=True, db_column='IGSN', max_length=255, null=True)),
                ('guid', models.CharField(blank=True, db_column='GUID', max_length=255, null=True)),
                ('number1', models.SmallIntegerField(blank=True, db_column='Number1', null=True)),
                ('version', models.IntegerField(blank=True, db_column='Version', default=0, null=True)),
                ('timestampcreated', models.DateTimeField(db_column='TimestampCreated', default=django.utils.timezone.now)),
                ('timestampmodified', models.DateTimeField(blank=True, db_column='TimestampModified', default=django.utils.timezone.now, null=True)),
                ('text1', models.TextField(blank=True, db_column='Text1', null=True)),
                ('text2', models.TextField(blank=True, db_column='Text2', null=True)),
                ('text3', models.TextField(blank=True, db_column='Text3', null=True)),
                ('collection', models.ForeignKey(db_column='CollectionID', on_delete=specifyweb.specify.models.protect_with_blockers, related_name='collectionobjectgroups', to='specify.collection')),
                ('createdbyagent', models.ForeignKey(db_column='CreatedByAgentID', null=True, on_delete=specifyweb.specify.models.protect_with_blockers, related_name='+', to='specify.agent')),
                ('modifiedbyagent', models.ForeignKey(db_column='ModifiedByAgentID', null=True, on_delete=specifyweb.specify.models.protect_with_blockers, related_name='+', to='specify.agent')),
            ],
            options={
                'db_table': 'collectionobjectgroup',
                'ordering': (),
            },
        ),
        migrations.CreateModel(
            name='CollectionObjectGroupJoin',
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
                ('parent', models.ForeignKey(db_column='ParentID', on_delete=django.db.models.deletion.CASCADE, related_name='parentcojos', to='specify.collectionobjectgroup')),
                ('cog', models.ForeignKey(db_column='COGID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cojo', to='specify.collectionobjectgroup')),
                ('co', models.ForeignKey(db_column='COID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cojo', to='specify.collectionobject')),
            ],
            options={
                'db_table': 'collectionobjectgroupjoin',
                'ordering': (),
            },
        ),
        migrations.AlterUniqueTogether(
            name='collectionobjectgroupjoin',
            unique_together={('parent', 'cog'), ('parent', 'co')},
        ),
    ]
