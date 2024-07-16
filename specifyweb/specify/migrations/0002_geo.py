# Generated by Django 3.2.15 on 2024-06-21 21:56
# TODO: Finish editing this migration for the new app structure

from calendar import c
from django.db import migrations, models
import django.utils.timezone
from specifyweb.businessrules.rules.cogtype_rules import COG_TYPE_TYPES
from specifyweb.specify.models import (
    protect_with_blockers,
    Collectionobject,
    CollectionObjectType,
    CollectionObjectGroupType,
    Collection,
    Discipline,
    Institution,
    Division,
    Datatype,
    Geologictimeperiodtreedef,
    Geographytreedef,
)
from specifyweb.specify.update_schema_config import (
    update_table_schema_config_with_defaults,
    revert_table_schema_config,
)
from specifyweb.specify.utils import testing_guard_clause

# Migrations Operations Order:
# 1. Create CollectionObjectType
# 2. Add CollectionObjectType (coType) realtionship to CollectionObject
# 3. Add hasreferencecatalognumber field to CollectionObject
# 4. Create default collection object types based on each discipline
# 5. Create new default taxon trees and ranks
# 6. Create CollectionObjectGroup
# 7. Create CollectionObjectGroupJoin

SCHEMA_CONFIG_TABLES = [
        ('CollectionObjectType', None),
        ('CollectionObjectGroupType', None),
        ('CollectionObjectGroup', None),
        ('CollectionObjectGroupJoin', None),
        ('SpUserExternalId', 'Stores provider identifiers and tokens for users who sign in using Single Sign On (SSO).'),
        ('SpAttachmentDataSet', 'Holds attachment data sets.'),
        ('UniquenessRule', 'Stores table names in the data model that have uniqueness rules configured for each discipline.'),
        ('UniquenessRuleField', 'Stores field names in the data model that have uniqueness rules configured for each discipline, linked to UniquenessRule records.'),
        ('Message', 'Stores user notifications.'),
        ('SpMerging', 'Tracks record and task IDs of records being merged.'),
        ('UserPolicy', 'Records permissions for a user within a collection.'),
        ('UserRole', 'Records roles associated with ecify users.'),
        ('Role', 'Stores names, descriptions, and collection information for user-created roles.'),
        ('RolePolicy', 'Stores resource and action permissions for user-created roles within a collection.'),
        ('LibraryRole', 'Stores names and descriptions of default roles that can be added to any collection.'),
        ('LibraryRolePolicy', 'Stores resource and action permissions for library roles within a collection.'),
        ('SpDataSet', 'Stores Specify Data Sets created during bulk import using the WorkBench, typically through spreadsheet uploads.')
    ]

def create_temp_discipline():
    if not testing_guard_clause():
        raise Exception("Discipline not found in database.")
    institution = Institution.objects.create(
        name="Temp Institution",
        isaccessionsglobal=True,
        issecurityon=False,
        isserverbased=False,
        issharinglocalities=True,
        issinglegeographytree=True,
    )
    division = Division.objects.create(
        institution=institution, name="Temp Division"
    )
    geologictimeperiodtreedef = Geologictimeperiodtreedef.objects.create(
        name="Temp gtptd"
    )
    geographytreedef = Geographytreedef.objects.create(name="Temp gtd")
    datatype = models.Datatype.objects.create(name='Temp datatype')
    return models.Discipline.objects.create(
        geologictimeperiodtreedef=geologictimeperiodtreedef,
        geographytreedef=geographytreedef,
        division=division,
        datatype=datatype,
    )

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
                taxontreedef_id=discipline.taxontreedef_id
            )
            # Update CollectionObjects' collectionobjecttype for the discipline
            Collectionobject.objects.filter(collection=collection).update(collectionobjecttype=cot)
            collection.collectionobjecttype = cot
            collection.save()

    def revert_default_collection_types(apps, schema_editor):
        # Reverse handeled by table deletion.
        pass

    def create_default_cog_types(apps, schema_editor):
        # Create default collection object group types for each collection, named after the discipline
        for collection in Collection.objects.all():
            for cog_type_type in COG_TYPE_TYPES:
                CollectionObjectGroupType.objects.get_or_create(
                    name=cog_type_type,
                    type=cog_type_type,
                    collection=collection
                )

    def revert_default_cog_types(apps, schema_editor):
        # Reverse handeled by table deletion
        pass

    def create_default_discipline_for_tree_defs(apps, schema_editor):
        for discipline in Discipline.objects.all():
            geography_tree_def = discipline.geographytreedef
            geography_tree_def.discipline = discipline
            geography_tree_def.save()

            geologic_time_period_tree_def = discipline.geologictimeperiodtreedef
            geologic_time_period_tree_def.discipline = discipline
            geologic_time_period_tree_def.save()

            lithostrat_tree_def = discipline.lithostrattreedef
            lithostrat_tree_def.discipline = discipline
            lithostrat_tree_def.save()

            # TODO: Fix BusinessRuleException 'Taxontreedef must have unique name in discipline'
            # taxon_tree_def = discipline.taxontreedef
            # taxon_tree_def.discipline = discipline
            # taxon_tree_def.save()

        for institution in Institution.objects.all():
            storage_tree_def = institution.storagetreedef
            storage_tree_def.institution = institution
            storage_tree_def.save()

    def revert_default_discipline_for_tree_defs(apps, schema_editor):
        # Reverse handeled by table deletion
        pass

    def initial_default_tree_def_discipline():
        try:
            return Discipline.objects.first().id
        except AttributeError: # Error handling for unit test building
            return create_temp_discipline().id

    def initial_default_tree_def_institution():
        try:
            return Institution.objects.first().id
        except AttributeError: # Error handling for unit test building
            if not testing_guard_clause():
                raise Exception("Institution not found in database.")
            return models.Institution.objects.create(
                name="Temp Institution",
                isaccessionsglobal=True,
                issecurityon=False,
                isserverbased=False,
                issharinglocalities=True,
                issinglegeographytree=True,
            ).id

    def create_table_schema_config_with_defaults(apps, schema_editor):
        for table, desc in SCHEMA_CONFIG_TABLES:
            try:
                discipline_id =  Discipline.objects.first().id
            except AttributeError: # Error handling for unit test building
                discipline_id = create_temp_discipline().id
            update_table_schema_config_with_defaults(table, discipline_id, desc)

    def revert_table_schema_config_with_defaults(apps, schema_editor):
        for table, _ in SCHEMA_CONFIG_TABLES:
            revert_table_schema_config(table)

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
                ('type', models.CharField(blank=True, db_column='Type', max_length=255, null=False)),
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
            field=models.ForeignKey(db_column='CollectionObjectTypeID', null=True, on_delete=models.SET_NULL, related_name='collections', to='specify.collectionobjecttype'),
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
        migrations.RunPython(create_default_cog_types, revert_default_cog_types),
        migrations.AddField(
            model_name='geographytreedef',
            name='discipline',
            field=models.ForeignKey(db_column='DisciplineID', default=initial_default_tree_def_discipline, null=True, on_delete=protect_with_blockers, related_name='geographytreedefs', to='specify.discipline'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='geologictimeperiodtreedef',
            name='discipline',
            field=models.ForeignKey(db_column='DisciplineID', default=initial_default_tree_def_discipline, null=True, on_delete=protect_with_blockers, related_name='geologictimeperiodtreedefs', to='specify.discipline'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lithostrattreedef',
            name='discipline',
            field=models.ForeignKey(db_column='DisciplineID', default=initial_default_tree_def_discipline, null=True, on_delete=protect_with_blockers, related_name='lithostratstreedefs', to='specify.discipline'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storagetreedef',
            name='institution',
            field=models.ForeignKey(db_column='InstitutionID', default=initial_default_tree_def_institution, on_delete=protect_with_blockers, related_name='storagetreedefs', to='specify.institution'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taxontreedef',
            name='discipline',
            field=models.ForeignKey(db_column='DisciplineID', default=initial_default_tree_def_discipline, null=True, on_delete=protect_with_blockers, related_name='taxontreedefs', to='specify.discipline'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='discipline',
            name='taxontreedef',
            field=models.OneToOneField(db_column='TaxonTreeDefID', null=True, on_delete=protect_with_blockers, related_name='defaultdiscipline', to='specify.taxontreedef'),
        ),
        migrations.RunPython(create_default_discipline_for_tree_defs, revert_default_discipline_for_tree_defs),
        migrations.RunPython(create_table_schema_config_with_defaults, revert_table_schema_config_with_defaults),
    ]
