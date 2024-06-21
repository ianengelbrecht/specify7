# Generated by Django 3.2.15 on 2024-06-21 21:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import specifyweb.specify.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('specify', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionObjectGroup',
            fields=[
                ('id', models.AutoField(db_column='collectionobjectgroupid', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('description', models.TextField(blank=True, db_column='Description', null=True)),
                ('igsn', models.CharField(blank=True, db_column='IGSN', max_length=255, null=True)),
                ('guid', models.CharField(blank=True, db_column='GUID', max_length=255, null=True)),
                ('number', models.SmallIntegerField(blank=True, db_column='Number', null=True)),
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
            name='CollectionObjectType',
            fields=[
                ('id', models.AutoField(db_column='CollectionObjectTypeID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=255)),
                ('isloanable', models.BooleanField(blank=True, db_column='IsLoanable', null=True)),
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
            },
        ),
        migrations.CreateModel(
            name='CollectionObjectGroupJoin',
            fields=[
                ('id', models.AutoField(db_column='collectionobjectgroupjoinid', primary_key=True, serialize=False)),
                ('isprimary', models.BooleanField(blank=True, db_column='IsPrimary', null=True)),
                ('issubstrate', models.BooleanField(blank=True, db_column='IsSubstrate', null=True)),
                ('precedence', models.SmallIntegerField(blank=True, db_column='Precedence', null=True)),
                ('order', models.SmallIntegerField(blank=True, db_column='Order', null=True)),
                ('version', models.IntegerField(blank=True, db_column='Version', default=0, null=True)),
                ('timestampcreated', models.DateTimeField(db_column='TimestampCreated', default=django.utils.timezone.now)),
                ('timestampmodified', models.DateTimeField(blank=True, db_column='TimestampModified', default=django.utils.timezone.now, null=True)),
                ('text1', models.TextField(blank=True, db_column='Text1', null=True)),
                ('text2', models.TextField(blank=True, db_column='Text2', null=True)),
                ('text3', models.TextField(blank=True, db_column='Text3', null=True)),
                ('collectionobjectchild', models.ForeignKey(db_column='CollectionObjectChildID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collectionobjectchildren', to='specify.collectionobject')),
                ('collectionobjectgroupchild', models.ForeignKey(db_column='CollectionObjectGroupChildID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collectionobjectgroupchildren', to='sp7_models.collectionobjectgroup')),
                ('collectionobjectgroupparent', models.ForeignKey(db_column='CollectionObjectGroupParentID', on_delete=django.db.models.deletion.CASCADE, related_name='collectionobjectgroupparents', to='sp7_models.collectionobjectgroup')),
            ],
            options={
                'db_table': 'collectionobjectgroupjoin',
                'ordering': (),
            },
        ),
        migrations.RunSQL(
            # Add ismemberofcog and hasreferencecatalognumber fields to CollectionObject
            """
            ALTER TABLE collectionobject
            ADD COLUMN IsMemberOfCog bit(1) DEFAULT 0 NOT NULL;
            ALTER TABLE collectionobject
            ADD COLUMN HasReferenceCatalogNumber bit(1) DEFAULT 0 NOT NULL;
            """,
            # Remove ismemberofcog and hasreferencecatalognumber fields from CollectionObject when unapplying migration
            """
            ALTER TABLE collectionobject
            DROP COLUMN IsMemberOfCog;
            ALTER TABLE collectionobject
            DROP COLUMN HasReferenceCatalogNumber;
            """
        ),
        # migrations.AddField( # This doesn't work right now because CollectionObject is in the specify django app
        #     model_name='ColllectionObject',
        #     name='ismemberofcog',
        #     field=models.BooleanField(blank=True, null=True, unique=False, db_column='IsMemberOfCog', db_index=False),
        #     preserve_default=False,
        # ),
        # migrations.RunPython(
        #     # Add ismemberofcog field to CollectionObject
        #     lambda apps, schema_editor: apps.get_model(
        #         "specify", "CollectionObject"
        #     ).add_to_class(
        #         "ismemberofcog",
        #         models.BooleanField(
        #             blank=True,
        #             null=True,
        #             unique=False,
        #             db_column="IsMemberOfCog",
        #             default=False,
        #             db_index=False,
        #         ),
        #     ),
        #     # Remove ismemberofcog field from CollectionObject when unapplying migration
        #     lambda apps, schema_editor: apps.get_model(
        #         "specify", "CollectionObject"
        #     ).remove_from_class("ismemberofcog"),
        # ),
    ]
