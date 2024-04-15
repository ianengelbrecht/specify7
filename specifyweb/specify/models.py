from functools import partialmethod
from django.db import models
from specifyweb.businessrules.exceptions import AbortSave
from . import model_extras
from .datamodel import datamodel
import logging

logger = logging.getLogger(__name__)

def protect_with_blockers(collector, field, sub_objs, using):
    if hasattr(collector, 'delete_blockers'):
        collector.delete_blockers.append((field, sub_objs))
    else:
        return models.PROTECT(collector, field, sub_objs, using)

def custom_save(self, *args, **kwargs):
    try:
        # Custom save logic here, if necessary
        super(self.__class__, self).save(*args, **kwargs)
    except AbortSave as e:
        # Handle AbortSave exception as needed
        logger.error("Save operation aborted: %s", e)
        return
class Accession(models.Model):
    specify_model = datamodel.get_table('accession')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='accessionid')

    # Fields
    accessioncondition = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='AccessionCondition', db_index=False)
    accessionnumber = models.CharField(blank=False, max_length=60, null=False, unique=False, db_column='AccessionNumber', db_index=False)
    dateaccessioned = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateAccessioned', db_index=False)
    dateacknowledged = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateAcknowledged', db_index=False)
    datereceived = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateReceived', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    status = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Status', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    totalvalue = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='TotalValue', db_index=False)
    type = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Type', db_index=False)
    verbatimdate = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='VerbatimDate', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    addressofrecord = models.ForeignKey('AddressOfRecord', db_column='AddressOfRecordID', related_name='accessions', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    repositoryagreement = models.ForeignKey('RepositoryAgreement', db_column='RepositoryAgreementID', related_name='accessions', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'accession'
        ordering = ()
        indexes = [
            # models.Index(fields=['AccessionNumber'], name='AccessionNumberIDX'),
            # models.Index(fields=['DateAccessioned'], name='AccessionDateIDX')
        ]

    save = partialmethod(custom_save)

class Accessionagent(models.Model):
    specify_model = datamodel.get_table('accessionagent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='accessionagentid')

    # Fields
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    role = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='Role', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    accession = models.ForeignKey('Accession', db_column='AccessionID', related_name='accessionagents', null=True, on_delete=models.CASCADE)
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    repositoryagreement = models.ForeignKey('RepositoryAgreement', db_column='RepositoryAgreementID', related_name='repositoryagreementagents', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'accessionagent'
        ordering = ()

    save = partialmethod(custom_save)

class Accessionattachment(models.Model):
    specify_model = datamodel.get_table('accessionattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='accessionattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    accession = models.ForeignKey('Accession', db_column='AccessionID', related_name='accessionattachments', null=False, on_delete=models.CASCADE)
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='accessionattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'accessionattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Accessionauthorization(models.Model):
    specify_model = datamodel.get_table('accessionauthorization')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='accessionauthorizationid')

    # Fields
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    accession = models.ForeignKey('Accession', db_column='AccessionID', related_name='accessionauthorizations', null=True, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    permit = models.ForeignKey('Permit', db_column='PermitID', related_name='accessionauthorizations', null=False, on_delete=protect_with_blockers)
    repositoryagreement = models.ForeignKey('RepositoryAgreement', db_column='RepositoryAgreementID', related_name='repositoryagreementauthorizations', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'accessionauthorization'
        ordering = ()

    save = partialmethod(custom_save)

class Accessioncitation(models.Model):
    specify_model = datamodel.get_table('accessioncitation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='accessioncitationid')

    # Fields
    figurenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FigureNumber', db_index=False)
    isfigured = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFigured', db_index=False)
    pagenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PageNumber', db_index=False)
    platenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PlateNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    accession = models.ForeignKey('Accession', db_column='AccessionID', related_name='accessioncitations', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='+', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'accessioncitation'
        ordering = ()

    save = partialmethod(custom_save)

class Address(models.Model):
    specify_model = datamodel.get_table('address')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='addressid')

    # Fields
    address = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Address', db_index=False)
    address2 = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Address2', db_index=False)
    address3 = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Address3', db_index=False)
    address4 = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Address4', db_index=False)
    address5 = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Address5', db_index=False)
    city = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='City', db_index=False)
    country = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Country', db_index=False)
    enddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EndDate', db_index=False)
    fax = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Fax', db_index=False)
    iscurrent = models.BooleanField(blank=True, null=True, unique=False, db_column='IsCurrent', db_index=False)
    isprimary = models.BooleanField(blank=True, null=True, unique=False, db_column='IsPrimary', db_index=False)
    isshipping = models.BooleanField(blank=True, null=True, unique=False, db_column='IsShipping', db_index=False)
    ordinal = models.IntegerField(blank=True, null=True, unique=False, db_column='Ordinal', db_index=False)
    phone1 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Phone1', db_index=False)
    phone2 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Phone2', db_index=False)
    positionheld = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PositionHeld', db_index=False)
    postalcode = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PostalCode', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    roomorbuilding = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='RoomOrBuilding', db_index=False)
    startdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='StartDate', db_index=False)
    state = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='State', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    typeofaddr = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='TypeOfAddr', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='addresses', null=True, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'address'
        ordering = ()

    save = partialmethod(custom_save)

class Addressofrecord(models.Model):
    specify_model = datamodel.get_table('addressofrecord')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='addressofrecordid')

    # Fields
    address = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Address', db_index=False)
    address2 = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Address2', db_index=False)
    city = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='City', db_index=False)
    country = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Country', db_index=False)
    postalcode = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PostalCode', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    state = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='State', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'addressofrecord'
        ordering = ()

    save = partialmethod(custom_save)

class Agent(models.Model):
    specify_model = datamodel.get_table('agent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='agentid')

    # Fields
    abbreviation = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Abbreviation', db_index=False)
    agenttype = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='AgentType', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    date2 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date2', db_index=False)
    date2precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date2Precision', db_index=False)
    dateofbirth = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateOfBirth', db_index=False)
    dateofbirthprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='DateOfBirthPrecision', db_index=False)
    dateofdeath = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateOfDeath', db_index=False)
    dateofdeathprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='DateOfDeathPrecision', db_index=False)
    datetype = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='DateType', db_index=False)
    email = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Email', db_index=False)
    firstname = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FirstName', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    initials = models.CharField(blank=True, max_length=8, null=True, unique=False, db_column='Initials', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    interests = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Interests', db_index=False)
    jobtitle = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='JobTitle', db_index=False)
    lastname = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='LastName', db_index=False)
    middleinitial = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='MiddleInitial', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    suffix = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Suffix', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Title', db_index=False)
    url = models.CharField(blank=True, max_length=1024, null=True, unique=False, db_column='URL', db_index=False)
    verbatimdate1 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='VerbatimDate1', db_index=False)
    verbatimdate2 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='VerbatimDate2', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collcontentcontact = models.ForeignKey('Collection', db_column='CollectionCCID', related_name='contentcontacts', null=True, on_delete=protect_with_blockers)
    colltechcontact = models.ForeignKey('Collection', db_column='CollectionTCID', related_name='technicalcontacts', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='members', null=True, on_delete=protect_with_blockers)
    instcontentcontact = models.ForeignKey('Institution', db_column='InstitutionCCID', related_name='contentcontacts', null=True, on_delete=protect_with_blockers)
    insttechcontact = models.ForeignKey('Institution', db_column='InstitutionTCID', related_name='technicalcontacts', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    organization = models.ForeignKey('Agent', db_column='ParentOrganizationID', related_name='orgmembers', null=True, on_delete=protect_with_blockers)
    specifyuser = models.ForeignKey('SpecifyUser', db_column='SpecifyUserID', related_name='agents', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'agent'
        ordering = ()
        indexes = [
            # models.Index(fields=['LastName'], name='AgentLastNameIDX'),
            # models.Index(fields=['FirstName'], name='AgentFirstNameIDX'),
            # models.Index(fields=['GUID'], name='AgentGuidIDX'),
            # models.Index(fields=['AgentType'], name='AgentTypeIDX'),
            # models.Index(fields=['Abbreviation'], name='AbbreviationIDX')
        ]

    save = partialmethod(custom_save)

class Agentattachment(models.Model):
    specify_model = datamodel.get_table('agentattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='agentattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='agentattachments', null=False, on_delete=models.CASCADE)
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='agentattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'agentattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Agentgeography(models.Model):
    specify_model = datamodel.get_table('agentgeography')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='agentgeographyid')

    # Fields
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    role = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Role', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='agentgeographies', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    geography = models.ForeignKey('Geography', db_column='GeographyID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'agentgeography'
        ordering = ()

    save = partialmethod(custom_save)

class Agentidentifier(models.Model):
    specify_model = datamodel.get_table('agentidentifier')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='agentidentifierid')

    # Fields
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    date2 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date2', db_index=False)
    date2precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date2Precision', db_index=False)
    identifier = models.CharField(blank=False, max_length=2048, null=False, unique=False, db_column='Identifier', db_index=False)
    identifiertype = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='IdentifierType', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='identifiers', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'agentidentifier'
        ordering = ()

    save = partialmethod(custom_save)

class Agentspecialty(models.Model):
    specify_model = datamodel.get_table('agentspecialty')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='agentspecialtyid')

    # Fields
    ordernumber = models.IntegerField(blank=False, null=False, unique=False, db_column='OrderNumber', db_index=False)
    specialtyname = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='SpecialtyName', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='agentspecialties', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'agentspecialty'
        ordering = ()

    save = partialmethod(custom_save)

class Agentvariant(models.Model):
    specify_model = datamodel.get_table('agentvariant')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='agentvariantid')

    # Fields
    country = models.CharField(blank=True, max_length=2, null=True, unique=False, db_column='Country', db_index=False)
    language = models.CharField(blank=True, max_length=2, null=True, unique=False, db_column='Language', db_index=False)
    name = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Name', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    vartype = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='VarType', db_index=False)
    variant = models.CharField(blank=True, max_length=2, null=True, unique=False, db_column='Variant', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='variants', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'agentvariant'
        ordering = ()

    save = partialmethod(custom_save)

class Appraisal(models.Model):
    specify_model = datamodel.get_table('appraisal')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='appraisalid')

    # Fields
    appraisaldate = models.DateTimeField(blank=False, null=False, unique=False, db_column='AppraisalDate', db_index=False)
    appraisalnumber = models.CharField(blank=False, max_length=64, null=False, unique=True, db_column='AppraisalNumber', db_index=False)
    appraisalvalue = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='AppraisalValue', db_index=False)
    monetaryunittype = models.CharField(blank=True, max_length=8, null=True, unique=False, db_column='MonetaryUnitType', db_index=False)
    notes = models.TextField(blank=True, null=True, unique=False, db_column='Notes', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    accession = models.ForeignKey('Accession', db_column='AccessionID', related_name='appraisals', null=True, on_delete=protect_with_blockers)
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'appraisal'
        ordering = ()
        indexes = [
            # models.Index(fields=['AppraisalNumber'], name='AppraisalNumberIDX'),
            # models.Index(fields=['AppraisalDate'], name='AppraisalDateIDX')
        ]

    save = partialmethod(custom_save)

class Attachment(models.Model):
    specify_model = datamodel.get_table('attachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='attachmentid')

    # Fields
    attachmentlocation = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='AttachmentLocation', db_index=False)
    attachmentstorageconfig = models.TextField(blank=True, null=True, unique=False, db_column='AttachmentStorageConfig', db_index=False)
    capturedevice = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='CaptureDevice', db_index=False)
    copyrightdate = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='CopyrightDate', db_index=False)
    copyrightholder = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='CopyrightHolder', db_index=False)
    credit = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Credit', db_index=False)
    dateimaged = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='DateImaged', db_index=False)
    filecreateddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='FileCreatedDate', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    ispublic = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsPublic', db_index=False)
    license = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='License', db_index=False)
    licenselogourl = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='LicenseLogoUrl', db_index=False)
    metadatatext = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='MetadataText', db_index=False)
    mimetype = models.CharField(blank=True, max_length=1024, null=True, unique=False, db_column='MimeType', db_index=False)
    origfilename = models.TextField(blank=False, null=False, unique=False, db_column='OrigFilename', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    scopeid = models.IntegerField(blank=True, null=True, unique=False, db_column='ScopeID', db_index=False)
    scopetype = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='ScopeType', db_index=False)
    subjectorientation = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SubjectOrientation', db_index=False)
    subtype = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Subtype', db_index=False)
    tableid = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='TableID', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Title', db_index=False)
    type = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    visibility = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Visibility', db_index=False)

    # Relationships: Many-to-One
    attachmentimageattribute = models.ForeignKey('AttachmentImageAttribute', db_column='AttachmentImageAttributeID', related_name='attachments', null=True, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    creator = models.ForeignKey('Agent', db_column='CreatorID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    visibilitysetby = models.ForeignKey('SpecifyUser', db_column='VisibilitySetByID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'attachment'
        ordering = ()
        indexes = [
            # models.Index(fields=['Title'], name='TitleIDX'),
            # models.Index(fields=['DateImaged'], name='DateImagedIDX'),
            # models.Index(fields=['ScopeID'], name='AttchScopeIDIDX'),
            # models.Index(fields=['ScopeType'], name='AttchScopeTypeIDX'),
            # models.Index(fields=['GUID'], name='AttchmentGuidIDX')
        ]

    save = partialmethod(custom_save)

class Attachmentimageattribute(models.Model):
    specify_model = datamodel.get_table('attachmentimageattribute')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='attachmentimageattributeid')

    # Fields
    creativecommons = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='CreativeCommons', db_index=False)
    height = models.IntegerField(blank=True, null=True, unique=False, db_column='Height', db_index=False)
    imagetype = models.CharField(blank=True, max_length=80, null=True, unique=False, db_column='ImageType', db_index=False)
    magnification = models.FloatField(blank=True, null=True, unique=False, db_column='Magnification', db_index=False)
    mbimageid = models.IntegerField(blank=True, null=True, unique=False, db_column='MBImageID', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    resolution = models.FloatField(blank=True, null=True, unique=False, db_column='Resolution', db_index=False)
    text1 = models.CharField(blank=True, max_length=200, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=200, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestamplastsend = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampLastSend', db_index=False)
    timestamplastupdatecheck = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampLastUpdateCheck', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    viewdescription = models.CharField(blank=True, max_length=80, null=True, unique=False, db_column='ViewDescription', db_index=False)
    width = models.IntegerField(blank=True, null=True, unique=False, db_column='Width', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    morphbankview = models.ForeignKey('MorphBankView', db_column='MorphBankViewID', related_name='attachmentimageattributes', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'attachmentimageattribute'
        ordering = ()

    save = partialmethod(custom_save)

class Attachmentmetadata(models.Model):
    specify_model = datamodel.get_table('attachmentmetadata')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='attachmentmetadataid')

    # Fields
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    value = models.CharField(blank=False, max_length=128, null=False, unique=False, db_column='Value', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='metadata', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'attachmentmetadata'
        ordering = ()

    save = partialmethod(custom_save)

class Attachmenttag(models.Model):
    specify_model = datamodel.get_table('attachmenttag')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='attachmenttagid')

    # Fields
    tag = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Tag', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='tags', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'attachmenttag'
        ordering = ()

    save = partialmethod(custom_save)

class Attributedef(models.Model):
    specify_model = datamodel.get_table('attributedef')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='attributedefid')

    # Fields
    datatype = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='DataType', db_index=False)
    fieldname = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FieldName', db_index=False)
    tabletype = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='TableType', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='attributedefs', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preptype = models.ForeignKey('PrepType', db_column='PrepTypeID', related_name='attributedefs', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'attributedef'
        ordering = ()

    save = partialmethod(custom_save)

class Author(models.Model):
    specify_model = datamodel.get_table('author')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='authorid')

    # Fields
    ordernumber = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='OrderNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='authors', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'author'
        ordering = ('ordernumber',)

    save = partialmethod(custom_save)

class Autonumberingscheme(models.Model):
    specify_model = datamodel.get_table('autonumberingscheme')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='autonumberingschemeid')

    # Fields
    formatname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='FormatName', db_index=False)
    isnumericonly = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsNumericOnly', db_index=False)
    schemeclassname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SchemeClassName', db_index=False)
    schemename = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SchemeName', db_index=False)
    tablenumber = models.IntegerField(blank=False, null=False, unique=False, db_column='TableNumber', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'autonumberingscheme'
        ordering = ()
        indexes = [
            # models.Index(fields=['SchemeName'], name='SchemeNameIDX')
        ]

    save = partialmethod(custom_save)

class Borrow(models.Model):
    specify_model = datamodel.get_table('borrow')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='borrowid')

    # Fields
    borrowdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='BorrowDate', db_index=False)
    borrowdateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='BorrowDatePrecision', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    currentduedate = models.DateTimeField(blank=True, null=True, unique=False, db_column='CurrentDueDate', db_index=False)
    dateclosed = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateClosed', db_index=False)
    invoicenumber = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='InvoiceNumber', db_index=False)
    isclosed = models.BooleanField(blank=True, null=True, unique=False, db_column='IsClosed', db_index=False)
    isfinancialresponsibility = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFinancialResponsibility', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    numberofitemsborrowed = models.IntegerField(blank=True, null=True, unique=False, db_column='NumberOfItemsBorrowed', db_index=False)
    originalduedate = models.DateTimeField(blank=True, null=True, unique=False, db_column='OriginalDueDate', db_index=False)
    receiveddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ReceivedDate', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    status = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Status', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    addressofrecord = models.ForeignKey('AddressOfRecord', db_column='AddressOfRecordID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'borrow'
        ordering = ()
        indexes = [
            # models.Index(fields=['InvoiceNumber'], name='BorInvoiceNumberIDX'),
            # models.Index(fields=['ReceivedDate'], name='BorReceivedDateIDX'),
            # models.Index(fields=['CollectionMemberID'], name='BorColMemIDX')
        ]

    save = partialmethod(custom_save)

class Borrowagent(models.Model):
    specify_model = datamodel.get_table('borrowagent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='borrowagentid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    role = models.CharField(blank=False, max_length=32, null=False, unique=False, db_column='Role', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    borrow = models.ForeignKey('Borrow', db_column='BorrowID', related_name='borrowagents', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'borrowagent'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='BorColMemIDX2')
        ]

    save = partialmethod(custom_save)

class Borrowattachment(models.Model):
    specify_model = datamodel.get_table('borrowattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='borrowattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='borrowattachments', null=False, on_delete=protect_with_blockers)
    borrow = models.ForeignKey('Borrow', db_column='BorrowID', related_name='borrowattachments', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'borrowattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Borrowmaterial(models.Model):
    specify_model = datamodel.get_table('borrowmaterial')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='borrowmaterialid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    description = models.CharField(blank=True, max_length=250, null=True, unique=False, db_column='Description', db_index=False)
    incomments = models.TextField(blank=True, null=True, unique=False, db_column='InComments', db_index=False)
    materialnumber = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='MaterialNumber', db_index=False)
    outcomments = models.TextField(blank=True, null=True, unique=False, db_column='OutComments', db_index=False)
    quantity = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Quantity', db_index=False)
    quantityresolved = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='QuantityResolved', db_index=False)
    quantityreturned = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='QuantityReturned', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    borrow = models.ForeignKey('Borrow', db_column='BorrowID', related_name='borrowmaterials', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'borrowmaterial'
        ordering = ()
        indexes = [
            # models.Index(fields=['MaterialNumber'], name='BorMaterialNumberIDX'),
            # models.Index(fields=['CollectionMemberID'], name='BorMaterialColMemIDX'),
            # models.Index(fields=['Description'], name='DescriptionIDX')
        ]

    save = partialmethod(custom_save)

class Borrowreturnmaterial(models.Model):
    specify_model = datamodel.get_table('borrowreturnmaterial')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='borrowreturnmaterialid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    quantity = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Quantity', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    returneddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ReturnedDate', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='ReturnedByID', related_name='+', null=True, on_delete=protect_with_blockers)
    borrowmaterial = models.ForeignKey('BorrowMaterial', db_column='BorrowMaterialID', related_name='borrowreturnmaterials', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'borrowreturnmaterial'
        ordering = ()
        indexes = [
            # models.Index(fields=['ReturnedDate'], name='BorrowReturnedDateIDX'),
            # models.Index(fields=['CollectionMemberID'], name='BorrowReturnedColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectingevent(models.Model):
    specify_model = datamodel.get_table('collectingevent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectingeventid')

    # Fields
    enddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EndDate', db_index=False)
    enddateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='EndDatePrecision', db_index=False)
    enddateverbatim = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='EndDateVerbatim', db_index=False)
    endtime = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='EndTime', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    method = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Method', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    reservedinteger3 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger3', db_index=False)
    reservedinteger4 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger4', db_index=False)
    reservedtext1 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ReservedText1', db_index=False)
    reservedtext2 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ReservedText2', db_index=False)
    sgrstatus = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='SGRStatus', db_index=False)
    startdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='StartDate', db_index=False)
    startdateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='StartDatePrecision', db_index=False)
    startdateverbatim = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='StartDateVerbatim', db_index=False)
    starttime = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='StartTime', db_index=False)
    stationfieldnumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='StationFieldNumber', db_index=False)
    stationfieldnumbermodifier1 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='StationFieldNumberModifier1', db_index=False)
    stationfieldnumbermodifier2 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='StationFieldNumberModifier2', db_index=False)
    stationfieldnumbermodifier3 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='StationFieldNumberModifier3', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.TextField(blank=True, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.TextField(blank=True, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.TextField(blank=True, null=True, unique=False, db_column='Text8', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    uniqueidentifier = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='UniqueIdentifier', db_index=False)
    verbatimdate = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='VerbatimDate', db_index=False)
    verbatimlocality = models.TextField(blank=True, null=True, unique=False, db_column='VerbatimLocality', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    visibility = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Visibility', db_index=False)

    # Relationships: Many-to-One
    collectingeventattribute = models.ForeignKey('CollectingEventAttribute', db_column='CollectingEventAttributeID', related_name='collectingevents', null=True, on_delete=protect_with_blockers)
    collectingtrip = models.ForeignKey('CollectingTrip', db_column='CollectingTripID', related_name='collectingevents', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    locality = models.ForeignKey('Locality', db_column='LocalityID', related_name='collectingevents', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    paleocontext = models.ForeignKey('PaleoContext', db_column='PaleoContextID', related_name='collectingevents', null=True, on_delete=protect_with_blockers)
    visibilitysetby = models.ForeignKey('SpecifyUser', db_column='VisibilitySetByID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectingevent'
        ordering = ()
        indexes = [
            # models.Index(fields=['StationFieldNumber'], name='CEStationFieldNumberIDX'),
            # models.Index(fields=['StartDate'], name='CEStartDateIDX'),
            # models.Index(fields=['EndDate'], name='CEEndDateIDX'),
            # models.Index(fields=['UniqueIdentifier'], name='CEUniqueIdentifierIDX'),
            # models.Index(fields=['GUID'], name='CEGuidIDX')
        ]

    save = partialmethod(custom_save)

class Collectingeventattachment(models.Model):
    specify_model = datamodel.get_table('collectingeventattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectingeventattachmentid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='collectingeventattachments', null=False, on_delete=protect_with_blockers)
    collectingevent = models.ForeignKey('CollectingEvent', db_column='CollectingEventID', related_name='collectingeventattachments', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectingeventattachment'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='CEAColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectingeventattr(models.Model):
    specify_model = datamodel.get_table('collectingeventattr')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='attrid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    dblvalue = models.FloatField(blank=True, null=True, unique=False, db_column='DoubleValue', db_index=False)
    strvalue = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='StrValue', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collectingevent = models.ForeignKey('CollectingEvent', db_column='CollectingEventID', related_name='collectingeventattrs', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    definition = models.ForeignKey('AttributeDef', db_column='AttributeDefID', related_name='collectingeventattrs', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectingeventattr'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='COLEVATColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectingeventattribute(models.Model):
    specify_model = datamodel.get_table('collectingeventattribute')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectingeventattributeid')

    # Fields
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer10 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer10', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer4 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    integer6 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer6', db_index=False)
    integer7 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer7', db_index=False)
    integer8 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer8', db_index=False)
    integer9 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer9', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number10 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number10', db_index=False)
    number11 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number11', db_index=False)
    number12 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number12', db_index=False)
    number13 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number13', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    number6 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number6', db_index=False)
    number7 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number7', db_index=False)
    number8 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number8', db_index=False)
    number9 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number9', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text10 = models.TextField(blank=True, null=True, unique=False, db_column='Text10', db_index=False)
    text11 = models.TextField(blank=True, null=True, unique=False, db_column='Text11', db_index=False)
    text12 = models.TextField(blank=True, null=True, unique=False, db_column='Text12', db_index=False)
    text13 = models.TextField(blank=True, null=True, unique=False, db_column='Text13', db_index=False)
    text14 = models.TextField(blank=True, null=True, unique=False, db_column='Text14', db_index=False)
    text15 = models.TextField(blank=True, null=True, unique=False, db_column='Text15', db_index=False)
    text16 = models.TextField(blank=True, null=True, unique=False, db_column='Text16', db_index=False)
    text17 = models.TextField(blank=True, null=True, unique=False, db_column='Text17', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.TextField(blank=True, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.TextField(blank=True, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.TextField(blank=True, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.TextField(blank=True, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    hosttaxon = models.ForeignKey('Taxon', db_column='HostTaxonID', related_name='collectingeventattributes', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectingeventattribute'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineID'], name='COLEVATSDispIDX')
        ]

    save = partialmethod(custom_save)

class Collectingeventauthorization(models.Model):
    specify_model = datamodel.get_table('collectingeventauthorization')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectingeventauthorizationid')

    # Fields
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collectingevent = models.ForeignKey('CollectingEvent', db_column='CollectingEventID', related_name='collectingeventauthorizations', null=True, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    permit = models.ForeignKey('Permit', db_column='PermitID', related_name='collectingeventauthorizations', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectingeventauthorization'
        ordering = ()

    save = partialmethod(custom_save)

class Collectingtrip(models.Model):
    specify_model = datamodel.get_table('collectingtrip')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectingtripid')

    # Fields
    collectingtripname = models.CharField(blank=True, max_length=400, null=True, unique=False, db_column='CollectingTripName', db_index=False)
    cruise = models.CharField(blank=True, max_length=250, null=True, unique=False, db_column='Cruise', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    date2 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date2', db_index=False)
    date2precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date2Precision', db_index=False)
    enddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EndDate', db_index=False)
    enddateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='EndDatePrecision', db_index=False)
    enddateverbatim = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='EndDateVerbatim', db_index=False)
    endtime = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='EndTime', db_index=False)
    expedition = models.CharField(blank=True, max_length=250, null=True, unique=False, db_column='Expedition', db_index=False)
    number1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number2', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    sponsor = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Sponsor', db_index=False)
    startdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='StartDate', db_index=False)
    startdateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='StartDatePrecision', db_index=False)
    startdateverbatim = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='StartDateVerbatim', db_index=False)
    starttime = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='StartTime', db_index=False)
    text1 = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.TextField(blank=True, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.TextField(blank=True, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.TextField(blank=True, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.TextField(blank=True, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    vessel = models.CharField(blank=True, max_length=250, null=True, unique=False, db_column='Vessel', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    agent1 = models.ForeignKey('Agent', db_column='Agent1ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent2 = models.ForeignKey('Agent', db_column='Agent2ID', related_name='+', null=True, on_delete=protect_with_blockers)
    collectingtripattribute = models.ForeignKey('CollectingTripAttribute', db_column='CollectingTripAttributeID', related_name='collectingtrips', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectingtrip'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectingTripName'], name='COLTRPNameIDX'),
            # models.Index(fields=['StartDate'], name='COLTRPStartDateIDX')
        ]

    save = partialmethod(custom_save)

class Collectingtripattachment(models.Model):
    specify_model = datamodel.get_table('collectingtripattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectingtripattachmentid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='collectingtripattachments', null=False, on_delete=protect_with_blockers)
    collectingtrip = models.ForeignKey('CollectingTrip', db_column='CollectingTripID', related_name='collectingtripattachments', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectingtripattachment'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='CTAColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectingtripattribute(models.Model):
    specify_model = datamodel.get_table('collectingtripattribute')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectingtripattributeid')

    # Fields
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer10 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer10', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer4 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    integer6 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer6', db_index=False)
    integer7 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer7', db_index=False)
    integer8 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer8', db_index=False)
    integer9 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer9', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number10 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number10', db_index=False)
    number11 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number11', db_index=False)
    number12 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number12', db_index=False)
    number13 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number13', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    number6 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number6', db_index=False)
    number7 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number7', db_index=False)
    number8 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number8', db_index=False)
    number9 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number9', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text10 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text10', db_index=False)
    text11 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text11', db_index=False)
    text12 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text12', db_index=False)
    text13 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text13', db_index=False)
    text14 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text14', db_index=False)
    text15 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text15', db_index=False)
    text16 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text16', db_index=False)
    text17 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text17', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectingtripattribute'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineID'], name='COLTRPSDispIDX')
        ]

    save = partialmethod(custom_save)

class Collectingtripauthorization(models.Model):
    specify_model = datamodel.get_table('collectingtripauthorization')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectingtripauthorizationid')

    # Fields
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collectingtrip = models.ForeignKey('CollectingTrip', db_column='CollectingTripID', related_name='collectingtripauthorizations', null=True, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    permit = models.ForeignKey('Permit', db_column='PermitID', related_name='collectingtripauthorizations', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectingtripauthorization'
        ordering = ()

    save = partialmethod(custom_save)

class Collection(models.Model):
    specify_model = datamodel.get_table('collection')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='usergroupscopeid')

    # Fields
    catalognumformatname = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='CatalogFormatNumName', db_index=False)
    code = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Code', db_index=False)
    collectionname = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='CollectionName', db_index=False)
    collectiontype = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='CollectionType', db_index=False)
    dbcontentversion = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='DbContentVersion', db_index=False)
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    developmentstatus = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='DevelopmentStatus', db_index=False)
    estimatedsize = models.IntegerField(blank=True, null=True, unique=False, db_column='EstimatedSize', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    institutiontype = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='InstitutionType', db_index=False)
    isembeddedcollectingevent = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsEmbeddedCollectingEvent', db_index=False)
    isanumber = models.CharField(blank=True, max_length=24, null=True, unique=False, db_column='IsaNumber', db_index=False)
    kingdomcoverage = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='KingdomCoverage', db_index=False)
    preservationmethodtype = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PreservationMethodType', db_index=False)
    primaryfocus = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PrimaryFocus', db_index=False)
    primarypurpose = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PrimaryPurpose', db_index=False)
    regnumber = models.CharField(blank=True, max_length=24, null=True, unique=False, db_column='RegNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    scope = models.TextField(blank=True, null=True, unique=False, db_column='Scope', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    webportaluri = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='WebPortalURI', db_index=False)
    websiteuri = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='WebSiteURI', db_index=False)

    # Relationships: Many-to-One
    admincontact = models.ForeignKey('Agent', db_column='AdminContactID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='collections', null=False, on_delete=protect_with_blockers)
    institutionnetwork = models.ForeignKey('Institution', db_column='InstitutionNetworkID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collection'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionName'], name='CollectionNameIDX'),
            # models.Index(fields=['GUID'], name='CollectionGuidIDX')
        ]

    save = partialmethod(custom_save)

class Collectionobject(models.Model):
    specify_model = datamodel.get_table('collectionobject')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectionobjectid')

    # Fields
    altcatalognumber = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='AltCatalogNumber', db_index=False)
    availability = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Availability', db_index=False)
    catalognumber = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='CatalogNumber', db_index=False)
    catalogeddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='CatalogedDate', db_index=False)
    catalogeddateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='CatalogedDatePrecision', db_index=False)
    catalogeddateverbatim = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='CatalogedDateVerbatim', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    countamt = models.IntegerField(blank=True, null=True, unique=False, db_column='CountAmt', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    deaccessioned = models.BooleanField(blank=True, null=True, unique=False, db_column='Deaccessioned', db_index=False)
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    embargoreason = models.TextField(blank=True, null=True, unique=False, db_column='EmbargoReason', db_index=False)
    embargoreleasedate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EmbargoReleaseDate', db_index=False)
    embargoreleasedateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='EmbargoReleaseDatePrecision', db_index=False)
    embargostartdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EmbargoStartDate', db_index=False)
    embargostartdateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='EmbargoStartDatePrecision', db_index=False)
    fieldnumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FieldNumber', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    inventorydate = models.DateTimeField(blank=True, null=True, unique=False, db_column='InventoryDate', db_index=False)
    inventorydateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='InventoryDatePrecision', db_index=False)
    modifier = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Modifier', db_index=False)
    name = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Name', db_index=False)
    notifications = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Notifications', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    numberofduplicates = models.IntegerField(blank=True, null=True, unique=False, db_column='NumberOfDuplicates', db_index=False)
    objectcondition = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='ObjectCondition', db_index=False)
    ocr = models.TextField(blank=True, null=True, unique=False, db_column='OCR', db_index=False)
    projectnumber = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='ProjectNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    reservedinteger3 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger3', db_index=False)
    reservedinteger4 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger4', db_index=False)
    reservedtext = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ReservedText', db_index=False)
    reservedtext2 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ReservedText2', db_index=False)
    reservedtext3 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ReservedText3', db_index=False)
    restrictions = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Restrictions', db_index=False)
    sgrstatus = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='SGRStatus', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.TextField(blank=True, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.TextField(blank=True, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.TextField(blank=True, null=True, unique=False, db_column='Text8', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    totalvalue = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='TotalValue', db_index=False)
    uniqueidentifier = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='UniqueIdentifier', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    visibility = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Visibility', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)
    yesno6 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo6', db_index=False)

    # Relationships: Many-to-One
    accession = models.ForeignKey('Accession', db_column='AccessionID', related_name='collectionobjects', null=True, on_delete=protect_with_blockers)
    agent1 = models.ForeignKey('Agent', db_column='Agent1ID', related_name='+', null=True, on_delete=protect_with_blockers)
    appraisal = models.ForeignKey('Appraisal', db_column='AppraisalID', related_name='collectionobjects', null=True, on_delete=protect_with_blockers)
    cataloger = models.ForeignKey('Agent', db_column='CatalogerID', related_name='+', null=True, on_delete=protect_with_blockers)
    collectingevent = models.ForeignKey('CollectingEvent', db_column='CollectingEventID', related_name='collectionobjects', null=True, on_delete=protect_with_blockers)
    collection = models.ForeignKey('Collection', db_column='CollectionID', related_name='+', null=False, on_delete=protect_with_blockers)
    collectionobjectattribute = models.ForeignKey('CollectionObjectAttribute', db_column='CollectionObjectAttributeID', related_name='collectionobjects', null=True, on_delete=protect_with_blockers)
    container = models.ForeignKey('Container', db_column='ContainerID', related_name='collectionobjects', null=True, on_delete=protect_with_blockers)
    containerowner = models.ForeignKey('Container', db_column='ContainerOwnerID', related_name='collectionobjectkids', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    embargoauthority = models.ForeignKey('Agent', db_column='EmbargoAuthorityID', related_name='+', null=True, on_delete=protect_with_blockers)
    fieldnotebookpage = models.ForeignKey('FieldNotebookPage', db_column='FieldNotebookPageID', related_name='collectionobjects', null=True, on_delete=protect_with_blockers)
    inventorizedby = models.ForeignKey('Agent', db_column='InventorizedByID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    paleocontext = models.ForeignKey('PaleoContext', db_column='PaleoContextID', related_name='collectionobjects', null=True, on_delete=protect_with_blockers)
    visibilitysetby = models.ForeignKey('SpecifyUser', db_column='VisibilitySetByID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectionobject'
        ordering = ()
        indexes = [
            # models.Index(fields=['FieldNumber'], name='FieldNumberIDX'),
            # models.Index(fields=['CatalogedDate'], name='CatalogedDateIDX'),
            # models.Index(fields=['CatalogNumber'], name='CatalogNumberIDX'),
            # models.Index(fields=['UniqueIdentifier'], name='COUniqueIdentifierIDX'),
            # models.Index(fields=['AltCatalogNumber'], name='AltCatalogNumberIDX'),
            # models.Index(fields=['GUID'], name='ColObjGuidIDX'),
            # models.Index(fields=['CollectionmemberID'], name='COColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectionobjectattachment(models.Model):
    specify_model = datamodel.get_table('collectionobjectattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectionobjectattachmentid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='collectionobjectattachments', null=False, on_delete=protect_with_blockers)
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='collectionobjectattachments', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectionobjectattachment'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='COLOBJATTColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectionobjectattr(models.Model):
    specify_model = datamodel.get_table('collectionobjectattr')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='attrid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    dblvalue = models.FloatField(blank=True, null=True, unique=False, db_column='DoubleValue', db_index=False)
    strvalue = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='StrValue', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='collectionobjectattrs', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    definition = models.ForeignKey('AttributeDef', db_column='AttributeDefID', related_name='collectionobjectattrs', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectionobjectattr'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='COLOBJATRSColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectionobjectattribute(models.Model):
    specify_model = datamodel.get_table('collectionobjectattribute')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectionobjectattributeid')

    # Fields
    bottomdistance = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='BottomDistance', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    direction = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Direction', db_index=False)
    distanceunits = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='DistanceUnits', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer10 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer10', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer4 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    integer6 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer6', db_index=False)
    integer7 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer7', db_index=False)
    integer8 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer8', db_index=False)
    integer9 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer9', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number10 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number10', db_index=False)
    number11 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number11', db_index=False)
    number12 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number12', db_index=False)
    number13 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number13', db_index=False)
    number14 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number14', db_index=False)
    number15 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number15', db_index=False)
    number16 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number16', db_index=False)
    number17 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number17', db_index=False)
    number18 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number18', db_index=False)
    number19 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number19', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number20 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number20', db_index=False)
    number21 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number21', db_index=False)
    number22 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number22', db_index=False)
    number23 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number23', db_index=False)
    number24 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number24', db_index=False)
    number25 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number25', db_index=False)
    number26 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number26', db_index=False)
    number27 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number27', db_index=False)
    number28 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number28', db_index=False)
    number29 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number29', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number30 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number30', db_index=False)
    number31 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number31', db_index=False)
    number32 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number32', db_index=False)
    number33 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number33', db_index=False)
    number34 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number34', db_index=False)
    number35 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number35', db_index=False)
    number36 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number36', db_index=False)
    number37 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number37', db_index=False)
    number38 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number38', db_index=False)
    number39 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number39', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number40 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number40', db_index=False)
    number41 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number41', db_index=False)
    number42 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number42', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    number6 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number6', db_index=False)
    number7 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number7', db_index=False)
    number8 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number8', db_index=False)
    number9 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number9', db_index=False)
    positionstate = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PositionState', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text10 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text10', db_index=False)
    text11 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text11', db_index=False)
    text12 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text12', db_index=False)
    text13 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text13', db_index=False)
    text14 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text14', db_index=False)
    text15 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Text15', db_index=False)
    text16 = models.TextField(blank=True, null=True, unique=False, db_column='Text16', db_index=False)
    text17 = models.TextField(blank=True, null=True, unique=False, db_column='Text17', db_index=False)
    text18 = models.TextField(blank=True, null=True, unique=False, db_column='Text18', db_index=False)
    text19 = models.TextField(blank=True, null=True, unique=False, db_column='Text19', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text20 = models.TextField(blank=True, null=True, unique=False, db_column='Text20', db_index=False)
    text21 = models.TextField(blank=True, null=True, unique=False, db_column='Text21', db_index=False)
    text22 = models.TextField(blank=True, null=True, unique=False, db_column='Text22', db_index=False)
    text23 = models.TextField(blank=True, null=True, unique=False, db_column='Text23', db_index=False)
    text24 = models.TextField(blank=True, null=True, unique=False, db_column='Text24', db_index=False)
    text25 = models.TextField(blank=True, null=True, unique=False, db_column='Text25', db_index=False)
    text26 = models.TextField(blank=True, null=True, unique=False, db_column='Text26', db_index=False)
    text27 = models.TextField(blank=True, null=True, unique=False, db_column='Text27', db_index=False)
    text28 = models.TextField(blank=True, null=True, unique=False, db_column='Text28', db_index=False)
    text29 = models.TextField(blank=True, null=True, unique=False, db_column='Text29', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text30 = models.TextField(blank=True, null=True, unique=False, db_column='Text30', db_index=False)
    text31 = models.TextField(blank=True, null=True, unique=False, db_column='Text31', db_index=False)
    text32 = models.TextField(blank=True, null=True, unique=False, db_column='Text32', db_index=False)
    text33 = models.TextField(blank=True, null=True, unique=False, db_column='Text33', db_index=False)
    text34 = models.TextField(blank=True, null=True, unique=False, db_column='Text34', db_index=False)
    text35 = models.TextField(blank=True, null=True, unique=False, db_column='Text35', db_index=False)
    text36 = models.TextField(blank=True, null=True, unique=False, db_column='Text36', db_index=False)
    text37 = models.TextField(blank=True, null=True, unique=False, db_column='Text37', db_index=False)
    text38 = models.TextField(blank=True, null=True, unique=False, db_column='Text38', db_index=False)
    text39 = models.TextField(blank=True, null=True, unique=False, db_column='Text39', db_index=False)
    text4 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text4', db_index=False)
    text40 = models.TextField(blank=True, null=True, unique=False, db_column='Text40', db_index=False)
    text5 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    topdistance = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='TopDistance', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno10 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo10', db_index=False)
    yesno11 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo11', db_index=False)
    yesno12 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo12', db_index=False)
    yesno13 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo13', db_index=False)
    yesno14 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo14', db_index=False)
    yesno15 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo15', db_index=False)
    yesno16 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo16', db_index=False)
    yesno17 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo17', db_index=False)
    yesno18 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo18', db_index=False)
    yesno19 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo19', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno20 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo20', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)
    yesno6 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo6', db_index=False)
    yesno7 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo7', db_index=False)
    yesno8 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo8', db_index=False)
    yesno9 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo9', db_index=False)

    # Relationships: Many-to-One
    agent1 = models.ForeignKey('Agent', db_column='Agent1ID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectionobjectattribute'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='COLOBJATTRSColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectionobjectcitation(models.Model):
    specify_model = datamodel.get_table('collectionobjectcitation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectionobjectcitationid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    figurenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FigureNumber', db_index=False)
    isfigured = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFigured', db_index=False)
    pagenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PageNumber', db_index=False)
    platenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PlateNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='collectionobjectcitations', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='collectionobjectcitations', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectionobjectcitation'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='COCITColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectionobjectproperty(models.Model):
    specify_model = datamodel.get_table('collectionobjectproperty')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectionobjectpropertyid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date10 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date10', db_index=False)
    date11 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date11', db_index=False)
    date12 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date12', db_index=False)
    date13 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date13', db_index=False)
    date14 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date14', db_index=False)
    date15 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date15', db_index=False)
    date16 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date16', db_index=False)
    date17 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date17', db_index=False)
    date18 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date18', db_index=False)
    date19 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date19', db_index=False)
    date2 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date2', db_index=False)
    date20 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date20', db_index=False)
    date3 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date3', db_index=False)
    date4 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date4', db_index=False)
    date5 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date5', db_index=False)
    date6 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date6', db_index=False)
    date7 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date7', db_index=False)
    date8 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date8', db_index=False)
    date9 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date9', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    integer1 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer10 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer10', db_index=False)
    integer11 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer11', db_index=False)
    integer12 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer12', db_index=False)
    integer13 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer13', db_index=False)
    integer14 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer14', db_index=False)
    integer15 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer15', db_index=False)
    integer16 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer16', db_index=False)
    integer17 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer17', db_index=False)
    integer18 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer18', db_index=False)
    integer19 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer19', db_index=False)
    integer2 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer20 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer20', db_index=False)
    integer21 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer21', db_index=False)
    integer22 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer22', db_index=False)
    integer23 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer23', db_index=False)
    integer24 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer24', db_index=False)
    integer25 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer25', db_index=False)
    integer26 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer26', db_index=False)
    integer27 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer27', db_index=False)
    integer28 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer28', db_index=False)
    integer29 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer29', db_index=False)
    integer3 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer30 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer30', db_index=False)
    integer4 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    integer6 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer6', db_index=False)
    integer7 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer7', db_index=False)
    integer8 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer8', db_index=False)
    integer9 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer9', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number10 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number10', db_index=False)
    number11 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number11', db_index=False)
    number12 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number12', db_index=False)
    number13 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number13', db_index=False)
    number14 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number14', db_index=False)
    number15 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number15', db_index=False)
    number16 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number16', db_index=False)
    number17 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number17', db_index=False)
    number18 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number18', db_index=False)
    number19 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number19', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number20 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number20', db_index=False)
    number21 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number21', db_index=False)
    number22 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number22', db_index=False)
    number23 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number23', db_index=False)
    number24 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number24', db_index=False)
    number25 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number25', db_index=False)
    number26 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number26', db_index=False)
    number27 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number27', db_index=False)
    number28 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number28', db_index=False)
    number29 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number29', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number30 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number30', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    number6 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number6', db_index=False)
    number7 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number7', db_index=False)
    number8 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number8', db_index=False)
    number9 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number9', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text1', db_index=False)
    text10 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text10', db_index=False)
    text11 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text11', db_index=False)
    text12 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text12', db_index=False)
    text13 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text13', db_index=False)
    text14 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text14', db_index=False)
    text15 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text15', db_index=False)
    text16 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text16', db_index=False)
    text17 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text17', db_index=False)
    text18 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text18', db_index=False)
    text19 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text19', db_index=False)
    text2 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text2', db_index=False)
    text20 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text20', db_index=False)
    text21 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text21', db_index=False)
    text22 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text22', db_index=False)
    text23 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text23', db_index=False)
    text24 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text24', db_index=False)
    text25 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text25', db_index=False)
    text26 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text26', db_index=False)
    text27 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text27', db_index=False)
    text28 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text28', db_index=False)
    text29 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text29', db_index=False)
    text3 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text3', db_index=False)
    text30 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text30', db_index=False)
    text31 = models.TextField(blank=True, null=True, unique=False, db_column='Text31', db_index=False)
    text32 = models.TextField(blank=True, null=True, unique=False, db_column='Text32', db_index=False)
    text33 = models.TextField(blank=True, null=True, unique=False, db_column='Text33', db_index=False)
    text34 = models.TextField(blank=True, null=True, unique=False, db_column='Text34', db_index=False)
    text35 = models.TextField(blank=True, null=True, unique=False, db_column='Text35', db_index=False)
    text36 = models.TextField(blank=True, null=True, unique=False, db_column='Text36', db_index=False)
    text37 = models.TextField(blank=True, null=True, unique=False, db_column='Text37', db_index=False)
    text38 = models.TextField(blank=True, null=True, unique=False, db_column='Text38', db_index=False)
    text39 = models.TextField(blank=True, null=True, unique=False, db_column='Text39', db_index=False)
    text4 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text4', db_index=False)
    text40 = models.TextField(blank=True, null=True, unique=False, db_column='Text40', db_index=False)
    text5 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno10 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo10', db_index=False)
    yesno11 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo11', db_index=False)
    yesno12 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo12', db_index=False)
    yesno13 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo13', db_index=False)
    yesno14 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo14', db_index=False)
    yesno15 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo15', db_index=False)
    yesno16 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo16', db_index=False)
    yesno17 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo17', db_index=False)
    yesno18 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo18', db_index=False)
    yesno19 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo19', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno20 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo20', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)
    yesno6 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo6', db_index=False)
    yesno7 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo7', db_index=False)
    yesno8 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo8', db_index=False)
    yesno9 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo9', db_index=False)

    # Relationships: Many-to-One
    agent1 = models.ForeignKey('Agent', db_column='Agent1ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent10 = models.ForeignKey('Agent', db_column='Agent10ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent11 = models.ForeignKey('Agent', db_column='Agent11ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent12 = models.ForeignKey('Agent', db_column='Agent12ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent13 = models.ForeignKey('Agent', db_column='Agent13ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent14 = models.ForeignKey('Agent', db_column='Agent14ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent15 = models.ForeignKey('Agent', db_column='Agent15ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent16 = models.ForeignKey('Agent', db_column='Agent16ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent17 = models.ForeignKey('Agent', db_column='Agent17ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent18 = models.ForeignKey('Agent', db_column='Agent18ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent19 = models.ForeignKey('Agent', db_column='Agent19ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent2 = models.ForeignKey('Agent', db_column='Agent2ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent20 = models.ForeignKey('Agent', db_column='Agent20ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent3 = models.ForeignKey('Agent', db_column='Agent3ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent4 = models.ForeignKey('Agent', db_column='Agent4ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent5 = models.ForeignKey('Agent', db_column='Agent5ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent6 = models.ForeignKey('Agent', db_column='Agent6ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent7 = models.ForeignKey('Agent', db_column='Agent7ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent8 = models.ForeignKey('Agent', db_column='Agent8D', related_name='+', null=True, on_delete=protect_with_blockers)
    agent9 = models.ForeignKey('Agent', db_column='Agent9ID', related_name='+', null=True, on_delete=protect_with_blockers)
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='collectionobjectproperties', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectionobjectproperty'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='COLOBJPROPColMemIDX')
        ]

    save = partialmethod(custom_save)

class Collectionreltype(models.Model):
    specify_model = datamodel.get_table('collectionreltype')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectionreltypeid')

    # Fields
    name = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Name', db_index=False)
    remarks = models.CharField(blank=True, max_length=4096, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    leftsidecollection = models.ForeignKey('Collection', db_column='LeftSideCollectionID', related_name='leftsidereltypes', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    rightsidecollection = models.ForeignKey('Collection', db_column='RightSideCollectionID', related_name='rightsidereltypes', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collectionreltype'
        ordering = ()

    save = partialmethod(custom_save)

class Collectionrelationship(models.Model):
    specify_model = datamodel.get_table('collectionrelationship')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectionrelationshipid')

    # Fields
    text1 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collectionreltype = models.ForeignKey('CollectionRelType', db_column='CollectionRelTypeID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    leftside = models.ForeignKey('CollectionObject', db_column='LeftSideCollectionID', related_name='leftsiderels', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    rightside = models.ForeignKey('CollectionObject', db_column='RightSideCollectionID', related_name='rightsiderels', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'collectionrelationship'
        ordering = ()

    save = partialmethod(custom_save)

class Collector(models.Model):
    specify_model = datamodel.get_table('collector')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='collectorid')

    # Fields
    isprimary = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsPrimary', db_index=False)
    ordernumber = models.IntegerField(blank=False, null=False, unique=False, db_column='OrderNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='collectors', null=False, on_delete=protect_with_blockers)
    collectingevent = models.ForeignKey('CollectingEvent', db_column='CollectingEventID', related_name='collectors', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'collector'
        ordering = ('ordernumber',)
        indexes = [
            # models.Index(fields=['DivisionID'], name='COLTRDivIDX')
        ]

    save = partialmethod(custom_save)

class Commonnametx(models.Model):
    specify_model = datamodel.get_table('commonnametx')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='commonnametxid')

    # Fields
    author = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Author', db_index=False)
    country = models.CharField(blank=True, max_length=2, null=True, unique=False, db_column='Country', db_index=False)
    language = models.CharField(blank=True, max_length=2, null=True, unique=False, db_column='Language', db_index=False)
    name = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Name', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    variant = models.CharField(blank=True, max_length=2, null=True, unique=False, db_column='Variant', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    taxon = models.ForeignKey('Taxon', db_column='TaxonID', related_name='commonnames', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'commonnametx'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='CommonNameTxNameIDX'),
            # models.Index(fields=['Country'], name='CommonNameTxCountryIDX')
        ]

    save = partialmethod(custom_save)

class Commonnametxcitation(models.Model):
    specify_model = datamodel.get_table('commonnametxcitation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='commonnametxcitationid')

    # Fields
    figurenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FigureNumber', db_index=False)
    isfigured = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFigured', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    pagenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PageNumber', db_index=False)
    platenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PlateNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    commonnametx = models.ForeignKey('CommonNameTx', db_column='CommonNameTxID', related_name='citations', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='+', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'commonnametxcitation'
        ordering = ()

    save = partialmethod(custom_save)

class Conservdescription(models.Model):
    specify_model = datamodel.get_table('conservdescription')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='conservdescriptionid')

    # Fields
    backgroundinfo = models.TextField(blank=True, null=True, unique=False, db_column='BackgroundInfo', db_index=False)
    composition = models.TextField(blank=True, null=True, unique=False, db_column='Composition', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    date2 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date2', db_index=False)
    date2precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date2Precision', db_index=False)
    date3 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date3', db_index=False)
    date3precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date3Precision', db_index=False)
    date4 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date4', db_index=False)
    date4precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date4Precision', db_index=False)
    date5 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date5', db_index=False)
    date5precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date5Precision', db_index=False)
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    determineddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='CatalogedDate', db_index=False)
    displayrecommendations = models.TextField(blank=True, null=True, unique=False, db_column='DisplayRecommendations', db_index=False)
    height = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Height', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer4 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    lightrecommendations = models.TextField(blank=True, null=True, unique=False, db_column='LightRecommendations', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    objlength = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='ObjLength', db_index=False)
    otherrecommendations = models.TextField(blank=True, null=True, unique=False, db_column='OtherRecommendations', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    shortdesc = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ShortDesc', db_index=False)
    source = models.TextField(blank=True, null=True, unique=False, db_column='Source', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    units = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='Units', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    width = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Width', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='conservdescriptions', null=True, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationID', related_name='conservdescriptions', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'conservdescription'
        ordering = ()
        indexes = [
            # models.Index(fields=['ShortDesc'], name='ConservDescShortDescIDX')
        ]

    save = partialmethod(custom_save)

class Conservdescriptionattachment(models.Model):
    specify_model = datamodel.get_table('conservdescriptionattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='conservdescriptionattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='conservdescriptionattachments', null=False, on_delete=protect_with_blockers)
    conservdescription = models.ForeignKey('ConservDescription', db_column='ConservDescriptionID', related_name='conservdescriptionattachments', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'conservdescriptionattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Conservevent(models.Model):
    specify_model = datamodel.get_table('conservevent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='conserveventid')

    # Fields
    advtestingexam = models.TextField(blank=True, null=True, unique=False, db_column='AdvTestingExam', db_index=False)
    advtestingexamresults = models.TextField(blank=True, null=True, unique=False, db_column='AdvTestingExamResults', db_index=False)
    completedcomments = models.TextField(blank=True, null=True, unique=False, db_column='CompletedComments', db_index=False)
    completeddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='CompletedDate', db_index=False)
    completeddateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='CompletedDatePrecision', db_index=False)
    conditionreport = models.TextField(blank=True, null=True, unique=False, db_column='ConditionReport', db_index=False)
    curatorapprovaldate = models.DateTimeField(blank=True, null=True, unique=False, db_column='CuratorApprovalDate', db_index=False)
    curatorapprovaldateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='CuratorApprovalDatePrecision', db_index=False)
    examdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ExamDate', db_index=False)
    examdateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='ExamDatePrecision', db_index=False)
    number1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number2', db_index=False)
    photodocs = models.TextField(blank=True, null=True, unique=False, db_column='PhotoDocs', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    treatmentcompdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='TreatmentCompDate', db_index=False)
    treatmentcompdateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='TreatmentCompDatePrecision', db_index=False)
    treatmentreport = models.TextField(blank=True, null=True, unique=False, db_column='TreatmentReport', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    conservdescription = models.ForeignKey('ConservDescription', db_column='ConservDescriptionID', related_name='events', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    curator = models.ForeignKey('Agent', db_column='CuratorID', related_name='+', null=True, on_delete=protect_with_blockers)
    examinedbyagent = models.ForeignKey('Agent', db_column='ExaminedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    treatedbyagent = models.ForeignKey('Agent', db_column='TreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'conservevent'
        ordering = ()
        indexes = [
            # models.Index(fields=['ExamDate'], name='ConservExamDateIDX'),
            # models.Index(fields=['completedDate'], name='ConservCompletedDateIDX')
        ]

    save = partialmethod(custom_save)

class Conserveventattachment(models.Model):
    specify_model = datamodel.get_table('conserveventattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='conserveventattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='conserveventattachments', null=False, on_delete=protect_with_blockers)
    conservevent = models.ForeignKey('ConservEvent', db_column='ConservEventID', related_name='conserveventattachments', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'conserveventattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Container(models.Model):
    specify_model = datamodel.get_table('container')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='containerid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    name = models.CharField(blank=True, max_length=1024, null=True, unique=False, db_column='Name', db_index=False)
    number = models.IntegerField(blank=True, null=True, unique=False, db_column='Number', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('Container', db_column='ParentID', related_name='children', null=True, on_delete=protect_with_blockers)
    storage = models.ForeignKey('Storage', db_column='StorageID', related_name='containers', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'container'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='ContainerNameIDX'),
            # models.Index(fields=['CollectionMemberID'], name='ContainerMemIDX')
        ]

    save = partialmethod(custom_save)

class Dnaprimer(models.Model):
    specify_model = datamodel.get_table('dnaprimer')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='dnaprimerid')

    # Fields
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    primerdesignator = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='PrimerDesignator', db_index=False)
    primernameforward = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='PrimerNameForward', db_index=False)
    primernamereverse = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='PrimerNameReverse', db_index=False)
    primerreferencecitationforward = models.CharField(blank=True, max_length=300, null=True, unique=False, db_column='PrimerReferenceCitationForward', db_index=False)
    primerreferencecitationreverse = models.CharField(blank=True, max_length=300, null=True, unique=False, db_column='PrimerReferenceCitationReverse', db_index=False)
    primerreferencelinkforward = models.CharField(blank=True, max_length=300, null=True, unique=False, db_column='PrimerReferenceLinkForward', db_index=False)
    primerreferencelinkreverse = models.CharField(blank=True, max_length=300, null=True, unique=False, db_column='PrimerReferenceLinkReverse', db_index=False)
    primersequenceforward = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='PrimerSequenceForward', db_index=False)
    primersequencereverse = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='PrimerSequenceReverse', db_index=False)
    purificationmethod = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='purificationMethod', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    reservedinteger3 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger3', db_index=False)
    reservedinteger4 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger4', db_index=False)
    reservednumber3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='ReservedNumber3', db_index=False)
    reservednumber4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='ReservedNumber4', db_index=False)
    reservedtext3 = models.TextField(blank=True, null=True, unique=False, db_column='ReservedText3', db_index=False)
    reservedtext4 = models.TextField(blank=True, null=True, unique=False, db_column='ReservedText4', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'dnaprimer'
        ordering = ()
        indexes = [
            # models.Index(fields=['PrimerDesignator'], name='DesignatorIDX')
        ]

    save = partialmethod(custom_save)

class Dnasequence(models.Model):
    specify_model = datamodel.get_table('dnasequence')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='dnasequenceid')

    # Fields
    ambiguousresidues = models.IntegerField(blank=True, null=True, unique=False, db_column='AmbiguousResidues', db_index=False)
    boldbarcodeid = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='BOLDBarcodeID', db_index=False)
    boldlastupdatedate = models.DateTimeField(blank=True, null=True, unique=False, db_column='BOLDLastUpdateDate', db_index=False)
    boldsampleid = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='BOLDSampleID', db_index=False)
    boldtranslationmatrix = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='BOLDTranslationMatrix', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    compa = models.IntegerField(blank=True, null=True, unique=False, db_column='CompA', db_index=False)
    compc = models.IntegerField(blank=True, null=True, unique=False, db_column='CompC', db_index=False)
    compg = models.IntegerField(blank=True, null=True, unique=False, db_column='CompG', db_index=False)
    compt = models.IntegerField(blank=True, null=True, unique=False, db_column='compT', db_index=False)
    extractiondate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ExtractionDate', db_index=False)
    extractiondateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='ExtractionDatePrecision', db_index=False)
    genbankaccessionnumber = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='GenBankAccessionNumber', db_index=False)
    genesequence = models.TextField(blank=True, null=True, unique=False, db_column='GeneSequence', db_index=False)
    moleculetype = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='MoleculeType', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    sequencedate = models.DateTimeField(blank=True, null=True, unique=False, db_column='SequenceDate', db_index=False)
    sequencedateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='SequenceDatePrecision', db_index=False)
    targetmarker = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='TargetMarker', db_index=False)
    text1 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Text3', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    totalresidues = models.IntegerField(blank=True, null=True, unique=False, db_column='TotalResidues', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)

    # Relationships: Many-to-One
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='dnasequences', null=True, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    extractor = models.ForeignKey('Agent', db_column='ExtractorID', related_name='+', null=True, on_delete=protect_with_blockers)
    materialsample = models.ForeignKey('MaterialSample', db_column='MaterialSampleID', related_name='dnasequences', null=True, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    sequencer = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'dnasequence'
        ordering = ()
        indexes = [
            # models.Index(fields=['GenBankAccessionNumber'], name='GenBankAccIDX'),
            # models.Index(fields=['BOLDBarcodeID'], name='BOLDBarcodeIDX'),
            # models.Index(fields=['BOLDSampleID'], name='BOLDSampleIDX')
        ]

    save = partialmethod(custom_save)

class Dnasequenceattachment(models.Model):
    specify_model = datamodel.get_table('dnasequenceattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='dnasequenceattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='dnasequenceattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    dnasequence = models.ForeignKey('DNASequence', db_column='DnaSequenceID', related_name='attachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'dnasequenceattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Dnasequencingrun(models.Model):
    specify_model = datamodel.get_table('dnasequencingrun')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='dnasequencingrunid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    dryaddoi = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='DryadDOI', db_index=False)
    genesequence = models.TextField(blank=True, null=True, unique=False, db_column='GeneSequence', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    ordinal = models.IntegerField(blank=True, null=True, unique=False, db_column='Ordinal', db_index=False)
    pcrcocktailprimer = models.BooleanField(blank=True, null=True, unique=False, db_column='PCRCocktailPrimer', db_index=False)
    pcrforwardprimercode = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PCRForwardPrimerCode', db_index=False)
    pcrprimername = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PCRPrimerName', db_index=False)
    pcrprimersequence5_3 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='PCRPrimerSequence5_3', db_index=False)
    pcrreverseprimercode = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PCRReversePrimerCode', db_index=False)
    readdirection = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='ReadDirection', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    rundate = models.DateTimeField(blank=True, null=True, unique=False, db_column='RunDate', db_index=False)
    scorefilename = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='ScoreFileName', db_index=False)
    sequencecocktailprimer = models.BooleanField(blank=True, null=True, unique=False, db_column='SequenceCocktailPrimer', db_index=False)
    sequenceprimercode = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='SequencePrimerCode', db_index=False)
    sequenceprimername = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='SequencePrimerName', db_index=False)
    sequenceprimersequence5_3 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SequencePrimerSequence5_3', db_index=False)
    sraexperimentid = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SRAExperimentID', db_index=False)
    srarunid = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SRARunID', db_index=False)
    srasubmissionid = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SRASubmissionID', db_index=False)
    text1 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Text3', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    tracefilename = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='TraceFileName', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    dnaprimer = models.ForeignKey('DNAPrimer', db_column='DNAPrimerID', related_name='dnasequencingruns', null=True, on_delete=protect_with_blockers)
    dnasequence = models.ForeignKey('DNASequence', db_column='DNASequenceID', related_name='dnasequencingruns', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparedbyagent = models.ForeignKey('Agent', db_column='PreparedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    runbyagent = models.ForeignKey('Agent', db_column='RunByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'dnasequencingrun'
        ordering = ()

    save = partialmethod(custom_save)

class Dnasequencingrunattachment(models.Model):
    specify_model = datamodel.get_table('dnasequencingrunattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='dnasequencingrunattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='dnasequencingrunattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    dnasequencingrun = models.ForeignKey('DNASequencingRun', db_column='DnaSequencingRunID', related_name='attachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'dnasequencerunattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Dnasequencingruncitation(models.Model):
    specify_model = datamodel.get_table('dnasequencingruncitation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='dnasequencingruncitationid')

    # Fields
    figurenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FigureNumber', db_index=False)
    isfigured = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFigured', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    pagenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PageNumber', db_index=False)
    platenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PlateNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='+', null=False, on_delete=protect_with_blockers)
    sequencingrun = models.ForeignKey('DNASequencingRun', db_column='DNASequencingRunID', related_name='citations', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'dnasequencingruncitation'
        ordering = ()

    save = partialmethod(custom_save)

class Datatype(models.Model):
    specify_model = datamodel.get_table('datatype')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='datatypeid')

    # Fields
    name = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Name', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'datatype'
        ordering = ()

    save = partialmethod(custom_save)

class Deaccession(models.Model):
    specify_model = datamodel.get_table('deaccession')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='deaccessionid')

    # Fields
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date2 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date2', db_index=False)
    deaccessiondate = models.DateTimeField(blank=True, null=True, unique=False, db_column='DeaccessionDate', db_index=False)
    deaccessionnumber = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='DeaccessionNumber', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer4 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    status = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Status', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    agent1 = models.ForeignKey('Agent', db_column='Agent1ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent2 = models.ForeignKey('Agent', db_column='Agent2ID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'deaccession'
        ordering = ()
        indexes = [
            # models.Index(fields=['DeaccessionNumber'], name='DeaccessionNumberIDX'),
            # models.Index(fields=['DeaccessionDate'], name='DeaccessionDateIDX')
        ]

    save = partialmethod(custom_save)

class Deaccessionagent(models.Model):
    specify_model = datamodel.get_table('deaccessionagent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='deaccessionagentid')

    # Fields
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    role = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='Role', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    deaccession = models.ForeignKey('Deaccession', db_column='DeaccessionID', related_name='deaccessionagents', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'deaccessionagent'
        ordering = ()

    save = partialmethod(custom_save)

class Deaccessionattachment(models.Model):
    specify_model = datamodel.get_table('deaccessionattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='deaccessionattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='deaccessionattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    deaccession = models.ForeignKey('Deaccession', db_column='DeaccessionID', related_name='deaccessionattachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'deaccessionattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Determination(models.Model):
    specify_model = datamodel.get_table('determination')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='determinationid')

    # Fields
    addendum = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='Addendum', db_index=False)
    alternatename = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='AlternateName', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    confidence = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Confidence', db_index=False)
    determineddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='DeterminedDate', db_index=False)
    determineddateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='DeterminedDatePrecision', db_index=False)
    featureorbasis = models.CharField(blank=True, max_length=250, null=True, unique=False, db_column='FeatureOrBasis', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer4 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    iscurrent = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsCurrent', db_index=False)
    method = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Method', db_index=False)
    nameusage = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='NameUsage', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    qualifier = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='Qualifier', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    subspqualifier = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='SubSpQualifier', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text8', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    typestatusname = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='TypeStatusName', db_index=False)
    varqualifier = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='VarQualifier', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='determinations', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    determiner = models.ForeignKey('Agent', db_column='DeterminerID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preferredtaxon = models.ForeignKey('Taxon', db_column='PreferredTaxonID', related_name='+', null=True, on_delete=protect_with_blockers)
    taxon = models.ForeignKey('Taxon', db_column='TaxonID', related_name='determinations', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'determination'
        ordering = ('-iscurrent',)
        indexes = [
            # models.Index(fields=['DeterminedDate'], name='DeterminedDateIDX'),
            # models.Index(fields=['CollectionMemberID'], name='DetMemIDX'),
            # models.Index(fields=['AlternateName'], name='AlterNameIDX'),
            # models.Index(fields=['GUID'], name='DeterminationGuidIDX'),
            # models.Index(fields=['TypeStatusName'], name='TypeStatusNameIDX')
        ]

    save = partialmethod(custom_save)

class Determinationcitation(models.Model):
    specify_model = datamodel.get_table('determinationcitation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='determinationcitationid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    figurenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FigureNumber', db_index=False)
    isfigured = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFigured', db_index=False)
    pagenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PageNumber', db_index=False)
    platenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PlateNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    determination = models.ForeignKey('Determination', db_column='DeterminationID', related_name='determinationcitations', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='determinationcitations', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'determinationcitation'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='DetCitColMemIDX')
        ]

    save = partialmethod(custom_save)

class Determiner(models.Model):
    specify_model = datamodel.get_table('determiner')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='determinerid')

    # Fields
    isprimary = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsPrimary', db_index=False)
    ordernumber = models.IntegerField(blank=False, null=False, unique=False, db_column='OrderNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    determination = models.ForeignKey('Determination', db_column='DeterminationID', related_name='determiners', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'determiner'
        ordering = ('ordernumber',)

    save = partialmethod(custom_save)

class Discipline(models.Model):
    specify_model = datamodel.get_table('discipline')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='usergroupscopeid')

    # Fields
    ispaleocontextembedded = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsPaleoContextEmbedded', db_index=False)
    name = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Name', db_index=False)
    paleocontextchildtable = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PaleoContextChildTable', db_index=False)
    regnumber = models.CharField(blank=True, max_length=24, null=True, unique=False, db_column='RegNumber', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: One-to-One
    taxonTreeDef = models.OneToOneField('TaxonTreeDef', db_column='TaxonTreeDefID', related_name='discipline', null=True, on_delete=protect_with_blockers)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    datatype = models.ForeignKey('DataType', db_column='DataTypeID', related_name='+', null=False, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='disciplines', null=False, on_delete=protect_with_blockers)
    geographytreedef = models.ForeignKey('GeographyTreeDef', db_column='GeographyTreeDefID', related_name='disciplines', null=False, on_delete=protect_with_blockers)
    geologictimeperiodtreedef = models.ForeignKey('GeologicTimePeriodTreeDef', db_column='GeologicTimePeriodTreeDefID', related_name='disciplines', null=False, on_delete=protect_with_blockers)
    lithostrattreedef = models.ForeignKey('LithoStratTreeDef', db_column='LithoStratTreeDefID', related_name='disciplines', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'discipline'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='DisciplineNameIDX')
        ]

    save = partialmethod(custom_save)

class Disposal(models.Model):
    specify_model = datamodel.get_table('disposal')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='disposalid')

    # Fields
    disposaldate = models.DateTimeField(blank=True, null=True, unique=False, db_column='DisposalDate', db_index=False)
    disposalnumber = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='DisposalNumber', db_index=False)
    donotexport = models.BooleanField(blank=True, null=True, unique=False, db_column='doNotExport', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    deaccession = models.ForeignKey('Deaccession', db_column='DeaccessionID', related_name='disposals', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'disposal'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisposalNumber'], name='DisposalNumberIDX'),
            # models.Index(fields=['DisposalDate'], name='DisposalDateIDX')
        ]

    save = partialmethod(custom_save)

class Disposalagent(models.Model):
    specify_model = datamodel.get_table('disposalagent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='disposalagentid')

    # Fields
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    role = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='Role', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    disposal = models.ForeignKey('Disposal', db_column='DisposalID', related_name='disposalagents', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'disposalagent'
        ordering = ()

    save = partialmethod(custom_save)

class Disposalattachment(models.Model):
    specify_model = datamodel.get_table('disposalattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='disposalattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='disposalattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    disposal = models.ForeignKey('Disposal', db_column='DisposalID', related_name='disposalattachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'disposalattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Disposalpreparation(models.Model):
    specify_model = datamodel.get_table('disposalpreparation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='disposalpreparationid')

    # Fields
    quantity = models.IntegerField(blank=True, null=True, unique=False, db_column='Quantity', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    disposal = models.ForeignKey('Disposal', db_column='DisposalID', related_name='disposalpreparations', null=False, on_delete=models.CASCADE)
    loanreturnpreparation = models.ForeignKey('LoanReturnPreparation', db_column='LoanReturnPreparationID', related_name='disposalpreparations', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationID', related_name='disposalpreparations', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'disposalpreparation'
        ordering = ()

    save = partialmethod(custom_save)

class Division(models.Model):
    specify_model = datamodel.get_table('division')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='usergroupscopeid')

    # Fields
    abbrev = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Abbrev', db_index=False)
    altname = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='AltName', db_index=False)
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    discipline = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='DisciplineType', db_index=False)
    iconuri = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='IconURI', db_index=False)
    name = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Name', db_index=False)
    regnumber = models.CharField(blank=True, max_length=24, null=True, unique=False, db_column='RegNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    uri = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Uri', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    address = models.ForeignKey('Address', db_column='AddressID', related_name='divisions', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    institution = models.ForeignKey('Institution', db_column='InstitutionID', related_name='divisions', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'division'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='DivisionNameIDX')
        ]

    save = partialmethod(custom_save)

class Exchangein(models.Model):
    specify_model = datamodel.get_table('exchangein')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='exchangeinid')

    # Fields
    contents = models.TextField(blank=True, null=True, unique=False, db_column='Contents', db_index=False)
    descriptionofmaterial = models.CharField(blank=True, max_length=120, null=True, unique=False, db_column='DescriptionOfMaterial', db_index=False)
    exchangedate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ExchangeDate', db_index=False)
    exchangeinnumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='ExchangeInNumber', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    quantityexchanged = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='QuantityExchanged', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    srcgeography = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='SrcGeography', db_index=False)
    srctaxonomy = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='SrcTaxonomy', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    addressofrecord = models.ForeignKey('AddressOfRecord', db_column='AddressOfRecordID', related_name='exchangeins', null=True, on_delete=protect_with_blockers)
    agentcatalogedby = models.ForeignKey('Agent', db_column='CatalogedByID', related_name='+', null=False, on_delete=protect_with_blockers)
    agentreceivedfrom = models.ForeignKey('Agent', db_column='ReceivedFromOrganizationID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'exchangein'
        ordering = ()
        indexes = [
            # models.Index(fields=['ExchangeDate'], name='ExchangeDateIDX'),
            # models.Index(fields=['DescriptionOfMaterial'], name='DescriptionOfMaterialIDX')
        ]

    save = partialmethod(custom_save)

class Exchangeinattachment(models.Model):
    specify_model = datamodel.get_table('exchangeinattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='exchangeinattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='exchangeinattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    exchangein = models.ForeignKey('ExchangeIn', db_column='ExchangeInID', related_name='exchangeinattachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'exchangeinattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Exchangeinprep(models.Model):
    specify_model = datamodel.get_table('exchangeinprep')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='exchangeinprepid')

    # Fields
    comments = models.TextField(blank=True, null=True, unique=False, db_column='Comments', db_index=False)
    descriptionofmaterial = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='DescriptionOfMaterial', db_index=False)
    number1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number1', db_index=False)
    quantity = models.IntegerField(blank=True, null=True, unique=False, db_column='Quantity', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    exchangein = models.ForeignKey('ExchangeIn', db_column='ExchangeInID', related_name='exchangeinpreps', null=True, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationID', related_name='exchangeinpreps', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'exchangeinprep'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineID'], name='ExchgInPrepDspMemIDX')
        ]

    save = partialmethod(custom_save)

class Exchangeout(models.Model):
    specify_model = datamodel.get_table('exchangeout')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='exchangeoutid')

    # Fields
    contents = models.TextField(blank=True, null=True, unique=False, db_column='Contents', db_index=False)
    descriptionofmaterial = models.CharField(blank=True, max_length=120, null=True, unique=False, db_column='DescriptionOfMaterial', db_index=False)
    exchangedate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ExchangeDate', db_index=False)
    exchangeoutnumber = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='ExchangeOutNumber', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    quantityexchanged = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='QuantityExchanged', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    srcgeography = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='SrcGeography', db_index=False)
    srctaxonomy = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='SrcTaxonomy', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    addressofrecord = models.ForeignKey('AddressOfRecord', db_column='AddressOfRecordID', related_name='exchangeouts', null=True, on_delete=protect_with_blockers)
    agentcatalogedby = models.ForeignKey('Agent', db_column='CatalogedByID', related_name='+', null=False, on_delete=protect_with_blockers)
    agentsentto = models.ForeignKey('Agent', db_column='SentToOrganizationID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    deaccession = models.ForeignKey('Deaccession', db_column='DeaccessionID', related_name='exchangeouts', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'exchangeout'
        ordering = ()
        indexes = [
            # models.Index(fields=['ExchangeDate'], name='ExchangeOutdateIDX'),
            # models.Index(fields=['DescriptionOfMaterial'], name='DescriptionOfMaterialIDX2'),
            # models.Index(fields=['ExchangeOutNumber'], name='ExchangeOutNumberIDX')
        ]

    save = partialmethod(custom_save)

class Exchangeoutattachment(models.Model):
    specify_model = datamodel.get_table('exchangeoutattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='exchangeoutattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='exchangeoutattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    exchangeout = models.ForeignKey('ExchangeOut', db_column='ExchangeOutID', related_name='exchangeoutattachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'exchangeoutattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Exchangeoutprep(models.Model):
    specify_model = datamodel.get_table('exchangeoutprep')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='exchangeoutprepid')

    # Fields
    comments = models.TextField(blank=True, null=True, unique=False, db_column='Comments', db_index=False)
    descriptionofmaterial = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='DescriptionOfMaterial', db_index=False)
    number1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number1', db_index=False)
    quantity = models.IntegerField(blank=True, null=True, unique=False, db_column='Quantity', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    exchangeout = models.ForeignKey('ExchangeOut', db_column='ExchangeOutID', related_name='exchangeoutpreps', null=True, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationID', related_name='exchangeoutpreps', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'exchangeoutprep'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineID'], name='ExchgOutPrepDspMemIDX')
        ]

    save = partialmethod(custom_save)

class Exsiccata(models.Model):
    specify_model = datamodel.get_table('exsiccata')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='exsiccataid')

    # Fields
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    schedae = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Schedae', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=False, max_length=255, null=False, unique=False, db_column='Title', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='exsiccatae', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'exsiccata'
        ordering = ()

    save = partialmethod(custom_save)

class Exsiccataitem(models.Model):
    specify_model = datamodel.get_table('exsiccataitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='exsiccataitemid')

    # Fields
    fascicle = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='Fascicle', db_index=False)
    number = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='Number', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='exsiccataitems', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    exsiccata = models.ForeignKey('Exsiccata', db_column='ExsiccataID', related_name='exsiccataitems', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'exsiccataitem'
        ordering = ()

    save = partialmethod(custom_save)

class Extractor(models.Model):
    specify_model = datamodel.get_table('extractor')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='extractorid')

    # Fields
    ordernumber = models.IntegerField(blank=False, null=False, unique=False, db_column='OrderNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    dnasequence = models.ForeignKey('DNASequence', db_column='DNASequenceID', related_name='extractors', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'extractor'
        ordering = ('ordernumber',)

    save = partialmethod(custom_save)

class Fieldnotebook(models.Model):
    specify_model = datamodel.get_table('fieldnotebook')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='fieldnotebookid')

    # Fields
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    enddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EndDate', db_index=False)
    location = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Storage', db_index=False)
    name = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Name', db_index=False)
    startdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='StartDate', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collection = models.ForeignKey('Collection', db_column='CollectionID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    owneragent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'fieldnotebook'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='FNBNameIDX'),
            # models.Index(fields=['StartDate'], name='FNBStartDateIDX'),
            # models.Index(fields=['EndDate'], name='FNBEndDateIDX')
        ]

    save = partialmethod(custom_save)

class Fieldnotebookattachment(models.Model):
    specify_model = datamodel.get_table('fieldnotebookattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='fieldnotebookattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='fieldnotebookattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    fieldnotebook = models.ForeignKey('FieldNotebook', db_column='FieldNotebookID', related_name='attachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'fieldnotebookattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Fieldnotebookpage(models.Model):
    specify_model = datamodel.get_table('fieldnotebookpage')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='fieldnotebookpageid')

    # Fields
    description = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Description', db_index=False)
    pagenumber = models.CharField(blank=False, max_length=32, null=False, unique=False, db_column='PageNumber', db_index=False)
    scandate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ScanDate', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    pageset = models.ForeignKey('FieldNotebookPageSet', db_column='FieldNotebookPageSetID', related_name='pages', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'fieldnotebookpage'
        ordering = ()
        indexes = [
            # models.Index(fields=['PageNumber'], name='FNBPPageNumberIDX'),
            # models.Index(fields=['ScanDate'], name='FNBPScanDateIDX')
        ]

    save = partialmethod(custom_save)

class Fieldnotebookpageattachment(models.Model):
    specify_model = datamodel.get_table('fieldnotebookpageattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='fieldnotebookpageattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='fieldnotebookpageattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    fieldnotebookpage = models.ForeignKey('FieldNotebookPage', db_column='FieldNotebookPageID', related_name='attachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'fieldnotebookpageattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Fieldnotebookpageset(models.Model):
    specify_model = datamodel.get_table('fieldnotebookpageset')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='fieldnotebookpagesetid')

    # Fields
    description = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Description', db_index=False)
    enddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EndDate', db_index=False)
    method = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Method', db_index=False)
    ordernumber = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='OrderNumber', db_index=False)
    startdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='StartDate', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    fieldnotebook = models.ForeignKey('FieldNotebook', db_column='FieldNotebookID', related_name='pagesets', null=True, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    sourceagent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'fieldnotebookpageset'
        ordering = ()
        indexes = [
            # models.Index(fields=['StartDate'], name='FNBPSStartDateIDX'),
            # models.Index(fields=['EndDate'], name='FNBPSEndDateIDX')
        ]

    save = partialmethod(custom_save)

class Fieldnotebookpagesetattachment(models.Model):
    specify_model = datamodel.get_table('fieldnotebookpagesetattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='fieldnotebookpagesetattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='fieldnotebookpagesetattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    fieldnotebookpageset = models.ForeignKey('FieldNotebookPageSet', db_column='FieldNotebookPageSetID', related_name='attachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'fieldnotebookpagesetattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Fundingagent(models.Model):
    specify_model = datamodel.get_table('fundingagent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='fundingagentid')

    # Fields
    isprimary = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsPrimary', db_index=False)
    ordernumber = models.IntegerField(blank=False, null=False, unique=False, db_column='OrderNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    collectingtrip = models.ForeignKey('CollectingTrip', db_column='CollectingTripID', related_name='fundingagents', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'fundingagent'
        ordering = ()
        indexes = [
            # models.Index(fields=['DivisionID'], name='COLTRIPDivIDX')
        ]

    save = partialmethod(custom_save)

class Geocoorddetail(models.Model):
    specify_model = datamodel.get_table('geocoorddetail')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='geocoorddetailid')

    # Fields
    errorpolygon = models.TextField(blank=True, null=True, unique=False, db_column='ErrorPolygon', db_index=False)
    georefaccuracy = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='GeoRefAccuracy', db_index=False)
    georefaccuracyunits = models.CharField(blank=True, max_length=20, null=True, unique=False, db_column='GeoRefAccuracyUnits', db_index=False)
    georefcompileddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='GeoRefCompiledDate', db_index=False)
    georefdetdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='GeoRefDetDate', db_index=False)
    georefdetref = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='GeoRefDetRef', db_index=False)
    georefremarks = models.TextField(blank=True, null=True, unique=False, db_column='GeoRefRemarks', db_index=False)
    georefverificationstatus = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='GeoRefVerificationStatus', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer4 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    maxuncertaintyest = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='MaxUncertaintyEst', db_index=False)
    maxuncertaintyestunit = models.CharField(blank=True, max_length=8, null=True, unique=False, db_column='MaxUncertaintyEstUnit', db_index=False)
    namedplaceextent = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='NamedPlaceExtent', db_index=False)
    nogeorefbecause = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='NoGeoRefBecause', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    originalcoordsystem = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='OriginalCoordSystem', db_index=False)
    protocol = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Protocol', db_index=False)
    source = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Source', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    uncertaintypolygon = models.TextField(blank=True, null=True, unique=False, db_column='UncertaintyPolygon', db_index=False)
    validation = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Validation', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    georefcompiledby = models.ForeignKey('Agent', db_column='CompiledByID', related_name='+', null=True, on_delete=protect_with_blockers)
    georefdetby = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    locality = models.ForeignKey('Locality', db_column='LocalityID', related_name='geocoorddetails', null=True, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'geocoorddetail'
        ordering = ()

    save = partialmethod(custom_save)

class Geography(model_extras.Geography):
    specify_model = datamodel.get_table('geography')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='geographyid')

    # Fields
    abbrev = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='Abbrev', db_index=False)
    centroidlat = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='CentroidLat', db_index=False)
    centroidlon = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='CentroidLon', db_index=False)
    commonname = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='CommonName', db_index=False)
    fullname = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='FullName', db_index=False)
    geographycode = models.CharField(blank=True, max_length=24, null=True, unique=False, db_column='GeographyCode', db_index=False)
    gml = models.TextField(blank=True, null=True, unique=False, db_column='GML', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    highestchildnodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='HighestChildNodeNumber', db_index=False)
    isaccepted = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsAccepted', db_index=False)
    iscurrent = models.BooleanField(blank=True, null=True, unique=False, db_column='IsCurrent', db_index=False)
    name = models.CharField(blank=False, max_length=128, null=False, unique=False, db_column='Name', db_index=False)
    nodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='NodeNumber', db_index=False)
    number1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number2', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    timestampversion = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampVersion', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    acceptedgeography = models.ForeignKey('Geography', db_column='AcceptedID', related_name='acceptedchildren', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    definition = models.ForeignKey('GeographyTreeDef', db_column='GeographyTreeDefID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    definitionitem = models.ForeignKey('GeographyTreeDefItem', db_column='GeographyTreeDefItemID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('Geography', db_column='ParentID', related_name='children', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'geography'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='GeoNameIDX'),
            # models.Index(fields=['FullName'], name='GeoFullNameIDX')
        ]

    save = partialmethod(custom_save)

class Geographytreedef(models.Model):
    specify_model = datamodel.get_table('geographytreedef')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='geographytreedefid')

    # Fields
    fullnamedirection = models.IntegerField(blank=True, null=True, unique=False, db_column='FullNameDirection', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'geographytreedef'
        ordering = ()

    save = partialmethod(custom_save)

class Geographytreedefitem(models.Model):
    specify_model = datamodel.get_table('geographytreedefitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='geographytreedefitemid')

    # Fields
    fullnameseparator = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FullNameSeparator', db_index=False)
    isenforced = models.BooleanField(blank=True, null=True, unique=False, db_column='IsEnforced', db_index=False)
    isinfullname = models.BooleanField(blank=True, null=True, unique=False, db_column='IsInFullName', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    textafter = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextAfter', db_index=False)
    textbefore = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextBefore', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Title', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('GeographyTreeDefItem', db_column='ParentItemID', related_name='children', null=True, on_delete=protect_with_blockers)
    treedef = models.ForeignKey('GeographyTreeDef', db_column='GeographyTreeDefID', related_name='treedefitems', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'geographytreedefitem'
        ordering = ()

    save = partialmethod(custom_save)

class Geologictimeperiod(model_extras.Geologictimeperiod):
    specify_model = datamodel.get_table('geologictimeperiod')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='geologictimeperiodid')

    # Fields
    endperiod = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='EndPeriod', db_index=False)
    enduncertainty = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='EndUncertainty', db_index=False)
    fullname = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='FullName', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    highestchildnodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='HighestChildNodeNumber', db_index=False)
    isaccepted = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsAccepted', db_index=False)
    isbiostrat = models.BooleanField(blank=True, null=True, unique=False, db_column='IsBioStrat', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    nodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='NodeNumber', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    standard = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Standard', db_index=False)
    startperiod = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='StartPeriod', db_index=False)
    startuncertainty = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='StartUncertainty', db_index=False)
    text1 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    acceptedgeologictimeperiod = models.ForeignKey('GeologicTimePeriod', db_column='AcceptedID', related_name='acceptedchildren', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    definition = models.ForeignKey('GeologicTimePeriodTreeDef', db_column='GeologicTimePeriodTreeDefID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    definitionitem = models.ForeignKey('GeologicTimePeriodTreeDefItem', db_column='GeologicTimePeriodTreeDefItemID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('GeologicTimePeriod', db_column='ParentID', related_name='children', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'geologictimeperiod'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='GTPNameIDX'),
            # models.Index(fields=['FullName'], name='GTPFullNameIDX'),
            # models.Index(fields=['GUID'], name='GTPGuidIDX')
        ]

    save = partialmethod(custom_save)

class Geologictimeperiodtreedef(models.Model):
    specify_model = datamodel.get_table('geologictimeperiodtreedef')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='geologictimeperiodtreedefid')

    # Fields
    fullnamedirection = models.IntegerField(blank=True, null=True, unique=False, db_column='FullNameDirection', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'geologictimeperiodtreedef'
        ordering = ()

    save = partialmethod(custom_save)

class Geologictimeperiodtreedefitem(models.Model):
    specify_model = datamodel.get_table('geologictimeperiodtreedefitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='geologictimeperiodtreedefitemid')

    # Fields
    fullnameseparator = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FullNameSeparator', db_index=False)
    isenforced = models.BooleanField(blank=True, null=True, unique=False, db_column='IsEnforced', db_index=False)
    isinfullname = models.BooleanField(blank=True, null=True, unique=False, db_column='IsInFullName', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    textafter = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextAfter', db_index=False)
    textbefore = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextBefore', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Title', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('GeologicTimePeriodTreeDefItem', db_column='ParentItemID', related_name='children', null=True, on_delete=protect_with_blockers)
    treedef = models.ForeignKey('GeologicTimePeriodTreeDef', db_column='GeologicTimePeriodTreeDefID', related_name='treedefitems', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'geologictimeperiodtreedefitem'
        ordering = ()

    save = partialmethod(custom_save)

class Gift(models.Model):
    specify_model = datamodel.get_table('gift')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='giftid')

    # Fields
    contents = models.TextField(blank=True, null=True, unique=False, db_column='Contents', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    datereceived = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateReceived', db_index=False)
    giftdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='GiftDate', db_index=False)
    giftnumber = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='GiftNumber', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    isfinancialresponsibility = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFinancialResponsibility', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    purposeofgift = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='PurposeOfGift', db_index=False)
    receivedcomments = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='ReceivedComments', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    specialconditions = models.TextField(blank=True, null=True, unique=False, db_column='SpecialConditions', db_index=False)
    srcgeography = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='SrcGeography', db_index=False)
    srctaxonomy = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='SrcTaxonomy', db_index=False)
    status = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Status', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    addressofrecord = models.ForeignKey('AddressOfRecord', db_column='AddressOfRecordID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    deaccession = models.ForeignKey('Deaccession', db_column='DeaccessionID', related_name='gifts', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'gift'
        ordering = ()
        indexes = [
            # models.Index(fields=['GiftNumber'], name='GiftNumberIDX'),
            # models.Index(fields=['GiftDate'], name='GiftDateIDX')
        ]

    save = partialmethod(custom_save)

class Giftagent(models.Model):
    specify_model = datamodel.get_table('giftagent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='giftagentid')

    # Fields
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    role = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='Role', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    gift = models.ForeignKey('Gift', db_column='GiftID', related_name='giftagents', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'giftagent'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineID'], name='GiftAgDspMemIDX')
        ]

    save = partialmethod(custom_save)

class Giftattachment(models.Model):
    specify_model = datamodel.get_table('giftattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='giftattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='giftattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    gift = models.ForeignKey('Gift', db_column='GiftID', related_name='giftattachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'giftattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Giftpreparation(models.Model):
    specify_model = datamodel.get_table('giftpreparation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='giftpreparationid')

    # Fields
    descriptionofmaterial = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='DescriptionOfMaterial', db_index=False)
    incomments = models.TextField(blank=True, null=True, unique=False, db_column='InComments', db_index=False)
    outcomments = models.TextField(blank=True, null=True, unique=False, db_column='OutComments', db_index=False)
    quantity = models.IntegerField(blank=True, null=True, unique=False, db_column='Quantity', db_index=False)
    receivedcomments = models.TextField(blank=True, null=True, unique=False, db_column='ReceivedComments', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    gift = models.ForeignKey('Gift', db_column='GiftID', related_name='giftpreparations', null=True, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationID', related_name='giftpreparations', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'giftpreparation'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineID'], name='GiftPrepDspMemIDX')
        ]

    save = partialmethod(custom_save)

class Groupperson(models.Model):
    specify_model = datamodel.get_table('groupperson')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='grouppersonid')

    # Fields
    ordernumber = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='OrderNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=False, on_delete=protect_with_blockers)
    group = models.ForeignKey('Agent', db_column='GroupID', related_name='groups', null=False, on_delete=models.CASCADE)
    member = models.ForeignKey('Agent', db_column='MemberID', related_name='members', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'groupperson'
        ordering = ()

    save = partialmethod(custom_save)

class Inforequest(models.Model):
    specify_model = datamodel.get_table('inforequest')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='inforequestid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    email = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Email', db_index=False)
    firstname = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Firstname', db_index=False)
    inforeqnumber = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='InfoReqNumber', db_index=False)
    institution = models.CharField(blank=True, max_length=127, null=True, unique=False, db_column='Institution', db_index=False)
    lastname = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Lastname', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    replydate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ReplyDate', db_index=False)
    requestdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='RequestDate', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'inforequest'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='IRColMemIDX')
        ]

    save = partialmethod(custom_save)

class Institution(models.Model):
    specify_model = datamodel.get_table('institution')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='usergroupscopeid')

    # Fields
    altname = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='AltName', db_index=False)
    code = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Code', db_index=False)
    copyright = models.TextField(blank=True, null=True, unique=False, db_column='Copyright', db_index=False)
    currentmanagedrelversion = models.CharField(blank=True, max_length=8, null=True, unique=False, db_column='CurrentManagedRelVersion', db_index=False)
    currentmanagedschemaversion = models.CharField(blank=True, max_length=8, null=True, unique=False, db_column='CurrentManagedSchemaVersion', db_index=False)
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    disclaimer = models.TextField(blank=True, null=True, unique=False, db_column='Disclaimer', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    hasbeenasked = models.BooleanField(blank=True, null=True, unique=False, db_column='HasBeenAsked', db_index=False)
    iconuri = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='IconURI', db_index=False)
    ipr = models.TextField(blank=True, null=True, unique=False, db_column='Ipr', db_index=False)
    isaccessionsglobal = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsAccessionsGlobal', db_index=False)
    isanonymous = models.BooleanField(blank=True, null=True, unique=False, db_column='IsAnonymous', db_index=False)
    isreleasemanagedglobally = models.BooleanField(blank=True, null=True, unique=False, db_column='IsReleaseManagedGlobally', db_index=False)
    issecurityon = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsSecurityOn', db_index=False)
    isserverbased = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsServerBased', db_index=False)
    issharinglocalities = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsSharingLocalities', db_index=False)
    issinglegeographytree = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsSingleGeographyTree', db_index=False)
    license = models.TextField(blank=True, null=True, unique=False, db_column='License', db_index=False)
    lsidauthority = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='LsidAuthority', db_index=False)
    minimumpwdlength = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='MinimumPwdLength', db_index=False)
    name = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Name', db_index=False)
    regnumber = models.CharField(blank=True, max_length=24, null=True, unique=False, db_column='RegNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    termsofuse = models.TextField(blank=True, null=True, unique=False, db_column='TermsOfUse', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    uri = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Uri', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    address = models.ForeignKey('Address', db_column='AddressID', related_name='insitutions', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    storagetreedef = models.ForeignKey('StorageTreeDef', db_column='StorageTreeDefID', related_name='institutions', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'institution'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='InstNameIDX'),
            # models.Index(fields=['GUID'], name='InstGuidIDX')
        ]

    save = partialmethod(custom_save)

class Institutionnetwork(models.Model):
    specify_model = datamodel.get_table('institutionnetwork')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='institutionnetworkid')

    # Fields
    altname = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='AltName', db_index=False)
    code = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Code', db_index=False)
    copyright = models.TextField(blank=True, null=True, unique=False, db_column='Copyright', db_index=False)
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    disclaimer = models.TextField(blank=True, null=True, unique=False, db_column='Disclaimer', db_index=False)
    iconuri = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='IconURI', db_index=False)
    ipr = models.TextField(blank=True, null=True, unique=False, db_column='Ipr', db_index=False)
    license = models.TextField(blank=True, null=True, unique=False, db_column='License', db_index=False)
    name = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Name', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    termsofuse = models.TextField(blank=True, null=True, unique=False, db_column='TermsOfUse', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    uri = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Uri', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    address = models.ForeignKey('Address', db_column='AddressID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'institutionnetwork'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='InstNetworkNameIDX')
        ]

    save = partialmethod(custom_save)

class Journal(models.Model):
    specify_model = datamodel.get_table('journal')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='journalid')

    # Fields
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    issn = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='ISSN', db_index=False)
    journalabbreviation = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='JournalAbbreviation', db_index=False)
    journalname = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='JournalName', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text1', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    institution = models.ForeignKey('Institution', db_column='InstitutionID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'journal'
        ordering = ()
        indexes = [
            # models.Index(fields=['JournalName'], name='JournalNameIDX'),
            # models.Index(fields=['GUID'], name='JournalGUIDIDX')
        ]

    save = partialmethod(custom_save)

class Latlonpolygon(models.Model):
    specify_model = datamodel.get_table('latlonpolygon')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='latlonpolygonid')

    # Fields
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    ispolyline = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsPolyline', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    locality = models.ForeignKey('Locality', db_column='LocalityID', related_name='latlonpolygons', null=True, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    visualquery = models.ForeignKey('SpVisualQuery', db_column='SpVisualQueryID', related_name='polygons', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'latlonpolygon'
        ordering = ()

    save = partialmethod(custom_save)

class Latlonpolygonpnt(models.Model):
    specify_model = datamodel.get_table('latlonpolygonpnt')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='latlonpolygonpntid')

    # Fields
    elevation = models.IntegerField(blank=True, null=True, unique=False, db_column='Elevation', db_index=False)
    latitude = models.DecimalField(blank=False, max_digits=22, decimal_places=10, null=False, unique=False, db_column='Latitude', db_index=False)
    longitude = models.DecimalField(blank=False, max_digits=22, decimal_places=10, null=False, unique=False, db_column='Longitude', db_index=False)
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)

    # Relationships: Many-to-One
    latlonpolygon = models.ForeignKey('LatLonPolygon', db_column='LatLonPolygonID', related_name='points', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'latlonpolygonpnt'
        ordering = ()

    save = partialmethod(custom_save)

class Lithostrat(model_extras.Lithostrat):
    specify_model = datamodel.get_table('lithostrat')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='lithostratid')

    # Fields
    fullname = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='FullName', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    highestchildnodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='HighestChildNodeNumber', db_index=False)
    isaccepted = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsAccepted', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    nodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='NodeNumber', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    acceptedlithostrat = models.ForeignKey('LithoStrat', db_column='AcceptedID', related_name='acceptedchildren', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    definition = models.ForeignKey('LithoStratTreeDef', db_column='LithoStratTreeDefID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    definitionitem = models.ForeignKey('LithoStratTreeDefItem', db_column='LithoStratTreeDefItemID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('LithoStrat', db_column='ParentID', related_name='children', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'lithostrat'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='LithoNameIDX'),
            # models.Index(fields=['FullName'], name='LithoFullNameIDX'),
            # models.Index(fields=['GUID'], name='LithoGuidIDX')
        ]

    save = partialmethod(custom_save)

class Lithostrattreedef(models.Model):
    specify_model = datamodel.get_table('lithostrattreedef')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='lithostrattreedefid')

    # Fields
    fullnamedirection = models.IntegerField(blank=True, null=True, unique=False, db_column='FullNameDirection', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'lithostrattreedef'
        ordering = ()

    save = partialmethod(custom_save)

class Lithostrattreedefitem(models.Model):
    specify_model = datamodel.get_table('lithostrattreedefitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='lithostrattreedefitemid')

    # Fields
    fullnameseparator = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FullNameSeparator', db_index=False)
    isenforced = models.BooleanField(blank=True, null=True, unique=False, db_column='IsEnforced', db_index=False)
    isinfullname = models.BooleanField(blank=True, null=True, unique=False, db_column='IsInFullName', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    textafter = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextAfter', db_index=False)
    textbefore = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextBefore', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Title', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('LithoStratTreeDefItem', db_column='ParentItemID', related_name='children', null=True, on_delete=protect_with_blockers)
    treedef = models.ForeignKey('LithoStratTreeDef', db_column='LithoStratTreeDefID', related_name='treedefitems', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'lithostrattreedefitem'
        ordering = ()

    save = partialmethod(custom_save)

class Loan(models.Model):
    specify_model = datamodel.get_table('loan')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='loanid')

    # Fields
    contents = models.TextField(blank=True, null=True, unique=False, db_column='Contents', db_index=False)
    currentduedate = models.DateTimeField(blank=True, null=True, unique=False, db_column='CurrentDueDate', db_index=False)
    dateclosed = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateClosed', db_index=False)
    datereceived = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateReceived', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    isclosed = models.BooleanField(blank=True, null=True, unique=False, db_column='IsClosed', db_index=False)
    isfinancialresponsibility = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFinancialResponsibility', db_index=False)
    loandate = models.DateTimeField(blank=True, null=True, unique=False, db_column='LoanDate', db_index=False)
    loannumber = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='LoanNumber', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    originalduedate = models.DateTimeField(blank=True, null=True, unique=False, db_column='OriginalDueDate', db_index=False)
    overduenotisentdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='OverdueNotiSetDate', db_index=False)
    purposeofloan = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='PurposeOfLoan', db_index=False)
    receivedcomments = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='ReceivedComments', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    specialconditions = models.TextField(blank=True, null=True, unique=False, db_column='SpecialConditions', db_index=False)
    srcgeography = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='SrcGeography', db_index=False)
    srctaxonomy = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='SrcTaxonomy', db_index=False)
    status = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Status', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    addressofrecord = models.ForeignKey('AddressOfRecord', db_column='AddressOfRecordID', related_name='loans', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'loan'
        ordering = ()
        indexes = [
            # models.Index(fields=['LoanNumber'], name='LoanNumberIDX'),
            # models.Index(fields=['LoanDate'], name='LoanDateIDX'),
            # models.Index(fields=['CurrentDueDate'], name='CurrentDueDateIDX')
        ]

    save = partialmethod(custom_save)

class Loanagent(models.Model):
    specify_model = datamodel.get_table('loanagent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='loanagentid')

    # Fields
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    role = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='Role', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    loan = models.ForeignKey('Loan', db_column='LoanID', related_name='loanagents', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'loanagent'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineID'], name='LoanAgDspMemIDX')
        ]

    save = partialmethod(custom_save)

class Loanattachment(models.Model):
    specify_model = datamodel.get_table('loanattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='loanattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='loanattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    loan = models.ForeignKey('Loan', db_column='LoanID', related_name='loanattachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'loanattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Loanpreparation(models.Model):
    specify_model = datamodel.get_table('loanpreparation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='loanpreparationid')

    # Fields
    descriptionofmaterial = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='DescriptionOfMaterial', db_index=False)
    incomments = models.TextField(blank=True, null=True, unique=False, db_column='InComments', db_index=False)
    isresolved = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsResolved', db_index=False)
    outcomments = models.TextField(blank=True, null=True, unique=False, db_column='OutComments', db_index=False)
    quantity = models.IntegerField(blank=True, null=True, unique=False, db_column='Quantity', db_index=False)
    quantityresolved = models.IntegerField(blank=True, null=True, unique=False, db_column='QuantityResolved', db_index=False)
    quantityreturned = models.IntegerField(blank=True, null=True, unique=False, db_column='QuantityReturned', db_index=False)
    receivedcomments = models.TextField(blank=True, null=True, unique=False, db_column='ReceivedComments', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    loan = models.ForeignKey('Loan', db_column='LoanID', related_name='loanpreparations', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationID', related_name='loanpreparations', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'loanpreparation'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineID'], name='LoanPrepDspMemIDX')
        ]

    save = partialmethod(custom_save)

class Loanreturnpreparation(models.Model):
    specify_model = datamodel.get_table('loanreturnpreparation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='loanreturnpreparationid')

    # Fields
    quantityresolved = models.IntegerField(blank=True, null=True, unique=False, db_column='QuantityResolved', db_index=False)
    quantityreturned = models.IntegerField(blank=True, null=True, unique=False, db_column='QuantityReturned', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    returneddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ReturnedDate', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    loanpreparation = models.ForeignKey('LoanPreparation', db_column='LoanPreparationID', related_name='loanreturnpreparations', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    receivedby = models.ForeignKey('Agent', db_column='ReceivedByID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'loanreturnpreparation'
        ordering = ()
        indexes = [
            # models.Index(fields=['ReturnedDate'], name='LoanReturnedDateIDX'),
            # models.Index(fields=['DisciplineID'], name='LoanRetPrepDspMemIDX')
        ]

    save = partialmethod(custom_save)

class Locality(models.Model):
    specify_model = datamodel.get_table('locality')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='localityid')

    # Fields
    datum = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Datum', db_index=False)
    elevationaccuracy = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='ElevationAccuracy', db_index=False)
    elevationmethod = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='ElevationMethod', db_index=False)
    gml = models.TextField(blank=True, null=True, unique=False, db_column='GML', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    lat1text = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Lat1Text', db_index=False)
    lat2text = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Lat2Text', db_index=False)
    latlongaccuracy = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='LatLongAccuracy', db_index=False)
    latlongmethod = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='LatLongMethod', db_index=False)
    latlongtype = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='LatLongType', db_index=False)
    latitude1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Latitude1', db_index=False)
    latitude2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Latitude2', db_index=False)
    localityname = models.CharField(blank=False, max_length=1024, null=False, unique=False, db_column='LocalityName', db_index=False)
    long1text = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Long1Text', db_index=False)
    long2text = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Long2Text', db_index=False)
    longitude1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Longitude1', db_index=False)
    longitude2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Longitude2', db_index=False)
    maxelevation = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='MaxElevation', db_index=False)
    minelevation = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='MinElevation', db_index=False)
    namedplace = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='NamedPlace', db_index=False)
    originalelevationunit = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='OriginalElevationUnit', db_index=False)
    originallatlongunit = models.IntegerField(blank=True, null=True, unique=False, db_column='OriginalLatLongUnit', db_index=False)
    relationtonamedplace = models.CharField(blank=True, max_length=120, null=True, unique=False, db_column='RelationToNamedPlace', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    sgrstatus = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='SGRStatus', db_index=False)
    shortname = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='ShortName', db_index=False)
    srclatlongunit = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='SrcLatLongUnit', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    uniqueidentifier = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='UniqueIdentifier', db_index=False)
    verbatimelevation = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='VerbatimElevation', db_index=False)
    verbatimlatitude = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='VerbatimLatitude', db_index=False)
    verbatimlongitude = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='VerbatimLongitude', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    visibility = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Visibility', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    geography = models.ForeignKey('Geography', db_column='GeographyID', related_name='localities', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    paleocontext = models.ForeignKey('PaleoContext', db_column='PaleoContextID', related_name='localities', null=True, on_delete=protect_with_blockers)
    visibilitysetby = models.ForeignKey('SpecifyUser', db_column='VisibilitySetByID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'locality'
        ordering = ()
        indexes = [
            # models.Index(fields=['LocalityName'], name='localityNameIDX'),
            # models.Index(fields=['DisciplineID'], name='LocalityDisciplineIDX'),
            # models.Index(fields=['NamedPlace'], name='NamedPlaceIDX'),
            # models.Index(fields=['UniqueIdentifier'], name='LocalityUniqueIdentifierIDX'),
            # models.Index(fields=['RelationToNamedPlace'], name='RelationToNamedPlaceIDX')
        ]

    save = partialmethod(custom_save)

class Localityattachment(models.Model):
    specify_model = datamodel.get_table('localityattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='localityattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='localityattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    locality = models.ForeignKey('Locality', db_column='LocalityID', related_name='localityattachments', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'localityattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Localitycitation(models.Model):
    specify_model = datamodel.get_table('localitycitation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='localitycitationid')

    # Fields
    figurenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FigureNumber', db_index=False)
    isfigured = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFigured', db_index=False)
    pagenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PageNumber', db_index=False)
    platenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PlateNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    locality = models.ForeignKey('Locality', db_column='LocalityID', related_name='localitycitations', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='localitycitations', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'localitycitation'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineID'], name='LocCitDspMemIDX')
        ]

    save = partialmethod(custom_save)

class Localitydetail(models.Model):
    specify_model = datamodel.get_table('localitydetail')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='localitydetailid')

    # Fields
    basemeridian = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='BaseMeridian', db_index=False)
    drainage = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Drainage', db_index=False)
    enddepth = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='EndDepth', db_index=False)
    enddepthunit = models.CharField(blank=True, max_length=23, null=True, unique=False, db_column='EndDepthUnit', db_index=False)
    enddepthverbatim = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='EndDepthVerbatim', db_index=False)
    gml = models.TextField(blank=True, null=True, unique=False, db_column='GML', db_index=False)
    huccode = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='HucCode', db_index=False)
    island = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Island', db_index=False)
    islandgroup = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='IslandGroup', db_index=False)
    mgrszone = models.CharField(blank=True, max_length=4, null=True, unique=False, db_column='MgrsZone', db_index=False)
    nationalparkname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='NationalParkName', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    paleolat = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PaleoLat', db_index=False)
    paleolng = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='PaleoLng', db_index=False)
    rangedesc = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='RangeDesc', db_index=False)
    rangedirection = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='RangeDirection', db_index=False)
    section = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Section', db_index=False)
    sectionpart = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='SectionPart', db_index=False)
    startdepth = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='StartDepth', db_index=False)
    startdepthunit = models.CharField(blank=True, max_length=23, null=True, unique=False, db_column='StartDepthUnit', db_index=False)
    startdepthverbatim = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='StartDepthVerbatim', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    township = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Township', db_index=False)
    townshipdirection = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='TownshipDirection', db_index=False)
    utmdatum = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='UtmDatum', db_index=False)
    utmeasting = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='UtmEasting', db_index=False)
    utmfalseeasting = models.IntegerField(blank=True, null=True, unique=False, db_column='UtmFalseEasting', db_index=False)
    utmfalsenorthing = models.IntegerField(blank=True, null=True, unique=False, db_column='UtmFalseNorthing', db_index=False)
    utmnorthing = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='UtmNorthing', db_index=False)
    utmoriglatitude = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='UtmOrigLatitude', db_index=False)
    utmoriglongitude = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='UtmOrigLongitude', db_index=False)
    utmscale = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='UtmScale', db_index=False)
    utmzone = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='UtmZone', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    waterbody = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='WaterBody', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    locality = models.ForeignKey('Locality', db_column='LocalityID', related_name='localitydetails', null=True, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'localitydetail'
        ordering = ()

    save = partialmethod(custom_save)

class Localitynamealias(models.Model):
    specify_model = datamodel.get_table('localitynamealias')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='localitynamealiasid')

    # Fields
    name = models.CharField(blank=False, max_length=255, null=False, unique=False, db_column='Name', db_index=False)
    source = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Source', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    locality = models.ForeignKey('Locality', db_column='LocalityID', related_name='localitynamealiass', null=False, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'localitynamealias'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='LocalityNameAliasIDX')
        ]

    save = partialmethod(custom_save)

class Materialsample(models.Model):
    specify_model = datamodel.get_table('materialsample')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='materialsampleid')

    # Fields
    ggbn_absorbanceratio260_230 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='GGBNAbsorbanceRatio260_230', db_index=False)
    ggbn_absorbanceratio260_280 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='GGBNAbsorbanceRatio260_280', db_index=False)
    ggbn_absorbanceratiomethod = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GGBNRAbsorbanceRatioMethod', db_index=False)
    ggbn_concentration = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='GGBNConcentration', db_index=False)
    ggbn_concentrationunit = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GGBNConcentrationUnit', db_index=False)
    ggbn_materialsampletype = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GGBNMaterialSampleType', db_index=False)
    ggbn_medium = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GGBNMedium', db_index=False)
    ggbn_purificationmethod = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GGBNPurificationMethod', db_index=False)
    ggbn_quality = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GGBNQuality', db_index=False)
    ggbn_qualitycheckdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='GGBNQualityCheckDate', db_index=False)
    ggbn_qualityremarks = models.TextField(blank=True, null=True, unique=False, db_column='GGBNQualityRemarks', db_index=False)
    ggbn_sampledesignation = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GGBNSampleDesignation', db_index=False)
    ggbn_samplesize = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='GGBNSampleSize', db_index=False)
    ggbn_volume = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='GGBNVolume', db_index=False)
    ggbn_volumeunit = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GGBNVolumeUnit', db_index=False)
    ggbn_weight = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='GGBNWeight', db_index=False)
    ggbn_weightmethod = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GGBNWeightMethod', db_index=False)
    ggbn_weightunit = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GGBNWeightUnit', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    extractiondate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ExtractionDate', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    reservedinteger3 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger3', db_index=False)
    reservedinteger4 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger4', db_index=False)
    reservednumber3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='ReservedNumber3', db_index=False)
    reservednumber4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='ReservedNumber4', db_index=False)
    reservedtext3 = models.TextField(blank=True, null=True, unique=False, db_column='ReservedText3', db_index=False)
    reservedtext4 = models.TextField(blank=True, null=True, unique=False, db_column='ReservedText4', db_index=False)
    srabioprojectid = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SRABioProjectID', db_index=False)
    srabiosampleid = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SRABioSampleID', db_index=False)
    sraprojectid = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SRAProjectID', db_index=False)
    srasampleid = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='SRASampleID', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    extractor = models.ForeignKey('Agent', db_column='ExtractorID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationID', related_name='materialsamples', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'materialsample'
        ordering = ()
        indexes = [
            # models.Index(fields=['GGBNSampleDesignation'], name='DesignationIDX')
        ]

    save = partialmethod(custom_save)

class Morphbankview(models.Model):
    specify_model = datamodel.get_table('morphbankview')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='morphbankviewid')

    # Fields
    developmentstate = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='DevelopmentState', db_index=False)
    form = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Form', db_index=False)
    imagingpreparationtechnique = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ImagingPreparationTechnique', db_index=False)
    imagingtechnique = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ImagingTechnique', db_index=False)
    morphbankexternalviewid = models.IntegerField(blank=True, null=True, unique=False, db_column='MorphBankExternalViewID', db_index=False)
    sex = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Sex', db_index=False)
    specimenpart = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='SpecimenPart', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    viewangle = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ViewAngle', db_index=False)
    viewname = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ViewName', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'morphbankview'
        ordering = ()

    save = partialmethod(custom_save)

class Otheridentifier(models.Model):
    specify_model = datamodel.get_table('otheridentifier')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='otheridentifierid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    date2 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date2', db_index=False)
    date2precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date2Precision', db_index=False)
    identifier = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Identifier', db_index=False)
    institution = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Institution', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    agent1 = models.ForeignKey('Agent', db_column='Agent1ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent2 = models.ForeignKey('Agent', db_column='Agent2ID', related_name='+', null=True, on_delete=protect_with_blockers)
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='otheridentifiers', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'otheridentifier'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='OthIdColMemIDX')
        ]

    save = partialmethod(custom_save)

class Paleocontext(models.Model):
    specify_model = datamodel.get_table('paleocontext')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='paleocontextid')

    # Fields
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    paleocontextname = models.CharField(blank=True, max_length=80, null=True, unique=False, db_column='PaleoContextName', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)

    # Relationships: Many-to-One
    biostrat = models.ForeignKey('GeologicTimePeriod', db_column='BioStratID', related_name='biostratspaleocontext', null=True, on_delete=protect_with_blockers)
    chronosstrat = models.ForeignKey('GeologicTimePeriod', db_column='ChronosStratID', related_name='chronosstratspaleocontext', null=True, on_delete=protect_with_blockers)
    chronosstratend = models.ForeignKey('GeologicTimePeriod', db_column='ChronosStratEndID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    lithostrat = models.ForeignKey('LithoStrat', db_column='LithoStratID', related_name='paleocontexts', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'paleocontext'
        ordering = ()
        indexes = [
            # models.Index(fields=['PaleoContextName'], name='PaleoCxtNameIDX'),
            # models.Index(fields=['DisciplineID'], name='PaleoCxtDisciplineIDX')
        ]

    save = partialmethod(custom_save)

class Pcrperson(models.Model):
    specify_model = datamodel.get_table('pcrperson')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='pcrpersonid')

    # Fields
    ordernumber = models.IntegerField(blank=False, null=False, unique=False, db_column='OrderNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    dnasequence = models.ForeignKey('DNASequence', db_column='DNASequenceID', related_name='pcrpersons', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'pcrperson'
        ordering = ()

    save = partialmethod(custom_save)

class Permit(models.Model):
    specify_model = datamodel.get_table('permit')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='permitid')

    # Fields
    copyright = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Copyright', db_index=False)
    enddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EndDate', db_index=False)
    isavailable = models.BooleanField(blank=True, null=True, unique=False, db_column='IsAvailable', db_index=False)
    isrequired = models.BooleanField(blank=True, null=True, unique=False, db_column='IsRequired', db_index=False)
    issueddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='IssuedDate', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    permitnumber = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='PermitNumber', db_index=False)
    permittext = models.TextField(blank=True, null=True, unique=False, db_column='PermitText', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    renewaldate = models.DateTimeField(blank=True, null=True, unique=False, db_column='RenewalDate', db_index=False)
    reservedinteger1 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger1', db_index=False)
    reservedinteger2 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger2', db_index=False)
    reservedtext3 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ReservedText3', db_index=False)
    reservedtext4 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ReservedText4', db_index=False)
    startdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='StartDate', db_index=False)
    status = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Status', db_index=False)
    statusqualifier = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='StatusQualifier', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    institution = models.ForeignKey('Institution', db_column='InstitutionID', related_name='+', null=False, on_delete=protect_with_blockers)
    issuedby = models.ForeignKey('Agent', db_column='IssuedByID', related_name='+', null=True, on_delete=protect_with_blockers)
    issuedto = models.ForeignKey('Agent', db_column='IssuedToID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'permit'
        ordering = ()
        indexes = [
            # models.Index(fields=['PermitNumber'], name='PermitNumberIDX'),
            # models.Index(fields=['IssuedDate'], name='IssuedDateIDX')
        ]

    save = partialmethod(custom_save)

class Permitattachment(models.Model):
    specify_model = datamodel.get_table('permitattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='permitattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='permitattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    permit = models.ForeignKey('Permit', db_column='PermitID', related_name='permitattachments', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'permitattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Picklist(models.Model):
    specify_model = datamodel.get_table('picklist')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='picklistid')

    # Fields
    fieldname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='FieldName', db_index=False)
    filterfieldname = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FilterFieldName', db_index=False)
    filtervalue = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FilterValue', db_index=False)
    formatter = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Formatter', db_index=False)
    issystem = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsSystem', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    readonly = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='ReadOnly', db_index=False)
    sizelimit = models.IntegerField(blank=True, null=True, unique=False, db_column='SizeLimit', db_index=False)
    sorttype = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='SortType', db_index=False)
    tablename = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TableName', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collection = models.ForeignKey('Collection', db_column='CollectionID', related_name='picklists', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'picklist'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='PickListNameIDX')
        ]

    save = partialmethod(custom_save)

class Picklistitem(models.Model):
    specify_model = datamodel.get_table('picklistitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='picklistitemid')

    # Fields
    ordinal = models.IntegerField(blank=True, null=True, unique=False, db_column='Ordinal', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=False, max_length=1024, null=False, unique=False, db_column='Title', db_index=False)
    value = models.CharField(blank=True, max_length=1024, null=True, unique=False, db_column='Value', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    picklist = models.ForeignKey('PickList', db_column='PickListID', related_name='picklistitems', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'picklistitem'
        ordering = ('ordinal',)

    save = partialmethod(custom_save)

class Preptype(models.Model):
    specify_model = datamodel.get_table('preptype')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='preptypeid')

    # Fields
    isloanable = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsLoanable', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collection = models.ForeignKey('Collection', db_column='CollectionID', related_name='preptypes', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'preptype'
        ordering = ()

    save = partialmethod(custom_save)

class Preparation(model_extras.Preparation):
    specify_model = datamodel.get_table('preparation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='preparationid')

    # Fields
    barcode = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='BarCode', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    countamt = models.IntegerField(blank=True, null=True, unique=False, db_column='CountAmt', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    date2 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date2', db_index=False)
    date2precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date2Precision', db_index=False)
    date3 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date3', db_index=False)
    date3precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date3Precision', db_index=False)
    date4 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date4', db_index=False)
    date4precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date4Precision', db_index=False)
    description = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Description', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    prepareddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='PreparedDate', db_index=False)
    prepareddateprecision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='PreparedDatePrecision', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    reservedinteger3 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger3', db_index=False)
    reservedinteger4 = models.IntegerField(blank=True, null=True, unique=False, db_column='ReservedInteger4', db_index=False)
    samplenumber = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='SampleNumber', db_index=False)
    status = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Status', db_index=False)
    storagelocation = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='StorageLocation', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text10 = models.TextField(blank=True, null=True, unique=False, db_column='Text10', db_index=False)
    text11 = models.TextField(blank=True, null=True, unique=False, db_column='Text11', db_index=False)
    text12 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text12', db_index=False)
    text13 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text13', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.TextField(blank=True, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.TextField(blank=True, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.TextField(blank=True, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.TextField(blank=True, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)

    # Relationships: Many-to-One
    alternatestorage = models.ForeignKey('Storage', db_column='AlternateStorageID', related_name='+', null=True, on_delete=protect_with_blockers)
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='preparations', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preptype = models.ForeignKey('PrepType', db_column='PrepTypeID', related_name='+', null=False, on_delete=protect_with_blockers)
    preparationattribute = models.ForeignKey('PreparationAttribute', db_column='PreparationAttributeID', related_name='preparations', null=True, on_delete=protect_with_blockers)
    preparedbyagent = models.ForeignKey('Agent', db_column='PreparedByID', related_name='+', null=True, on_delete=protect_with_blockers)
    storage = models.ForeignKey('Storage', db_column='StorageID', related_name='preparations', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'preparation'
        ordering = ()
        indexes = [
            # models.Index(fields=['preparedDate'], name='PreparedDateIDX'),
            # models.Index(fields=['CollectionMemberID'], name='PrepColMemIDX'),
            # models.Index(fields=['GUID'], name='PrepGuidIDX'),
            # models.Index(fields=['SampleNumber'], name='PrepSampleNumIDX'),
            # models.Index(fields=['BarCode'], name='PrepBarCodeIDX')
        ]

    save = partialmethod(custom_save)

class Preparationattachment(models.Model):
    specify_model = datamodel.get_table('preparationattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='preparationattachmentid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='preparationattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationID', related_name='preparationattachments', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'preparationattachment'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='PrepAttColMemIDX')
        ]

    save = partialmethod(custom_save)

class Preparationattr(models.Model):
    specify_model = datamodel.get_table('preparationattr')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='attrid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    dblvalue = models.FloatField(blank=True, null=True, unique=False, db_column='DoubleValue', db_index=False)
    strvalue = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='StrValue', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    definition = models.ForeignKey('AttributeDef', db_column='AttributeDefID', related_name='preparationattrs', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationId', related_name='preparationattrs', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'preparationattr'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='PrepAttrColMemIDX')
        ]

    save = partialmethod(custom_save)

class Preparationattribute(models.Model):
    specify_model = datamodel.get_table('preparationattribute')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='preparationattributeid')

    # Fields
    attrdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='AttrDate', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number5', db_index=False)
    number6 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number6', db_index=False)
    number7 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number7', db_index=False)
    number8 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number8', db_index=False)
    number9 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Number9', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text10 = models.TextField(blank=True, null=True, unique=False, db_column='Text10', db_index=False)
    text11 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text11', db_index=False)
    text12 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text12', db_index=False)
    text13 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text13', db_index=False)
    text14 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text14', db_index=False)
    text15 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text15', db_index=False)
    text16 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text16', db_index=False)
    text17 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text17', db_index=False)
    text18 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text18', db_index=False)
    text19 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text19', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text20 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text20', db_index=False)
    text21 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text21', db_index=False)
    text22 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text22', db_index=False)
    text23 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text23', db_index=False)
    text24 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text24', db_index=False)
    text25 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text25', db_index=False)
    text26 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text26', db_index=False)
    text3 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'preparationattribute'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='PrepAttrsColMemIDX')
        ]

    save = partialmethod(custom_save)

class Preparationproperty(models.Model):
    specify_model = datamodel.get_table('preparationproperty')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='preparationpropertyid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date10 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date10', db_index=False)
    date11 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date11', db_index=False)
    date12 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date12', db_index=False)
    date13 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date13', db_index=False)
    date14 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date14', db_index=False)
    date15 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date15', db_index=False)
    date16 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date16', db_index=False)
    date17 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date17', db_index=False)
    date18 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date18', db_index=False)
    date19 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date19', db_index=False)
    date2 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date2', db_index=False)
    date20 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date20', db_index=False)
    date3 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date3', db_index=False)
    date4 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date4', db_index=False)
    date5 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date5', db_index=False)
    date6 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date6', db_index=False)
    date7 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date7', db_index=False)
    date8 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date8', db_index=False)
    date9 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date9', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    integer1 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer10 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer10', db_index=False)
    integer11 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer11', db_index=False)
    integer12 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer12', db_index=False)
    integer13 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer13', db_index=False)
    integer14 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer14', db_index=False)
    integer15 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer15', db_index=False)
    integer16 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer16', db_index=False)
    integer17 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer17', db_index=False)
    integer18 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer18', db_index=False)
    integer19 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer19', db_index=False)
    integer2 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer20 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer20', db_index=False)
    integer21 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer21', db_index=False)
    integer22 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer22', db_index=False)
    integer23 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer23', db_index=False)
    integer24 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer24', db_index=False)
    integer25 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer25', db_index=False)
    integer26 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer26', db_index=False)
    integer27 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer27', db_index=False)
    integer28 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer28', db_index=False)
    integer29 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer29', db_index=False)
    integer3 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer30 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer30', db_index=False)
    integer4 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    integer6 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer6', db_index=False)
    integer7 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer7', db_index=False)
    integer8 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer8', db_index=False)
    integer9 = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Integer9', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number10 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number10', db_index=False)
    number11 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number11', db_index=False)
    number12 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number12', db_index=False)
    number13 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number13', db_index=False)
    number14 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number14', db_index=False)
    number15 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number15', db_index=False)
    number16 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number16', db_index=False)
    number17 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number17', db_index=False)
    number18 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number18', db_index=False)
    number19 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number19', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number20 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number20', db_index=False)
    number21 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number21', db_index=False)
    number22 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number22', db_index=False)
    number23 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number23', db_index=False)
    number24 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number24', db_index=False)
    number25 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number25', db_index=False)
    number26 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number26', db_index=False)
    number27 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number27', db_index=False)
    number28 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number28', db_index=False)
    number29 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number29', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number30 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number30', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    number6 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number6', db_index=False)
    number7 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number7', db_index=False)
    number8 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number8', db_index=False)
    number9 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number9', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text1', db_index=False)
    text10 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text10', db_index=False)
    text11 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text11', db_index=False)
    text12 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text12', db_index=False)
    text13 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text13', db_index=False)
    text14 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text14', db_index=False)
    text15 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text15', db_index=False)
    text16 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text16', db_index=False)
    text17 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text17', db_index=False)
    text18 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text18', db_index=False)
    text19 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text19', db_index=False)
    text2 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text2', db_index=False)
    text20 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text20', db_index=False)
    text21 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text21', db_index=False)
    text22 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text22', db_index=False)
    text23 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text23', db_index=False)
    text24 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text24', db_index=False)
    text25 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text25', db_index=False)
    text26 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text26', db_index=False)
    text27 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text27', db_index=False)
    text28 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text28', db_index=False)
    text29 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text29', db_index=False)
    text3 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text3', db_index=False)
    text30 = models.CharField(blank=True, max_length=100, null=True, unique=False, db_column='Text30', db_index=False)
    text31 = models.TextField(blank=True, null=True, unique=False, db_column='Text31', db_index=False)
    text32 = models.TextField(blank=True, null=True, unique=False, db_column='Text32', db_index=False)
    text33 = models.TextField(blank=True, null=True, unique=False, db_column='Text33', db_index=False)
    text34 = models.TextField(blank=True, null=True, unique=False, db_column='Text34', db_index=False)
    text35 = models.TextField(blank=True, null=True, unique=False, db_column='Text35', db_index=False)
    text36 = models.TextField(blank=True, null=True, unique=False, db_column='Text36', db_index=False)
    text37 = models.TextField(blank=True, null=True, unique=False, db_column='Text37', db_index=False)
    text38 = models.TextField(blank=True, null=True, unique=False, db_column='Text38', db_index=False)
    text39 = models.TextField(blank=True, null=True, unique=False, db_column='Text39', db_index=False)
    text4 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text4', db_index=False)
    text40 = models.TextField(blank=True, null=True, unique=False, db_column='Text40', db_index=False)
    text5 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno10 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo10', db_index=False)
    yesno11 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo11', db_index=False)
    yesno12 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo12', db_index=False)
    yesno13 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo13', db_index=False)
    yesno14 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo14', db_index=False)
    yesno15 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo15', db_index=False)
    yesno16 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo16', db_index=False)
    yesno17 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo17', db_index=False)
    yesno18 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo18', db_index=False)
    yesno19 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo19', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno20 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo20', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)
    yesno6 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo6', db_index=False)
    yesno7 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo7', db_index=False)
    yesno8 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo8', db_index=False)
    yesno9 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo9', db_index=False)

    # Relationships: Many-to-One
    agent1 = models.ForeignKey('Agent', db_column='Agent1ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent10 = models.ForeignKey('Agent', db_column='Agent10ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent11 = models.ForeignKey('Agent', db_column='Agent11ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent12 = models.ForeignKey('Agent', db_column='Agent12ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent13 = models.ForeignKey('Agent', db_column='Agent13ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent14 = models.ForeignKey('Agent', db_column='Agent14ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent15 = models.ForeignKey('Agent', db_column='Agent15ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent16 = models.ForeignKey('Agent', db_column='Agent16ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent17 = models.ForeignKey('Agent', db_column='Agent17ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent18 = models.ForeignKey('Agent', db_column='Agent18ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent19 = models.ForeignKey('Agent', db_column='Agent19ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent2 = models.ForeignKey('Agent', db_column='Agent2ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent20 = models.ForeignKey('Agent', db_column='Agent20ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent3 = models.ForeignKey('Agent', db_column='Agent3ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent4 = models.ForeignKey('Agent', db_column='Agent4ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent5 = models.ForeignKey('Agent', db_column='Agent5ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent6 = models.ForeignKey('Agent', db_column='Agent6ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent7 = models.ForeignKey('Agent', db_column='Agent7ID', related_name='+', null=True, on_delete=protect_with_blockers)
    agent8 = models.ForeignKey('Agent', db_column='Agent8D', related_name='+', null=True, on_delete=protect_with_blockers)
    agent9 = models.ForeignKey('Agent', db_column='Agent9ID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    preparation = models.ForeignKey('Preparation', db_column='PreparationID', related_name='preparationproperties', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'preparationproperty'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='PREPPROPColMemIDX')
        ]

    save = partialmethod(custom_save)

class Project(models.Model):
    specify_model = datamodel.get_table('project')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='projectid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    enddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EndDate', db_index=False)
    grantagency = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GrantAgency', db_index=False)
    grantnumber = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='GrantNumber', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    projectdescription = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='ProjectDescription', db_index=False)
    projectname = models.CharField(blank=False, max_length=128, null=False, unique=False, db_column='ProjectName', db_index=False)
    projectnumber = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='ProjectNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    startdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='StartDate', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    url = models.CharField(blank=True, max_length=1024, null=True, unique=False, db_column='URL', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    agent = models.ForeignKey('Agent', db_column='ProjectAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'project'
        ordering = ()
        indexes = [
            # models.Index(fields=['ProjectName'], name='ProjectNameIDX'),
            # models.Index(fields=['ProjectNumber'], name='ProjectNumberIDX')
        ]

    save = partialmethod(custom_save)

class Recordset(models.Model):
    specify_model = datamodel.get_table('recordset')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='recordsetid')

    # Fields
    allpermissionlevel = models.IntegerField(blank=True, null=True, unique=False, db_column='AllPermissionLevel', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    dbtableid = models.IntegerField(blank=False, null=False, unique=False, db_column='TableID', db_index=False)
    grouppermissionlevel = models.IntegerField(blank=True, null=True, unique=False, db_column='GroupPermissionLevel', db_index=False)
    name = models.CharField(blank=False, max_length=280, null=False, unique=False, db_column='Name', db_index=False)
    ownerpermissionlevel = models.IntegerField(blank=True, null=True, unique=False, db_column='OwnerPermissionLevel', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    group = models.ForeignKey('SpPrincipal', db_column='SpPrincipalID', related_name='+', null=True, on_delete=protect_with_blockers)
    inforequest = models.ForeignKey('InfoRequest', db_column='InfoRequestID', related_name='recordsets', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    specifyuser = models.ForeignKey('SpecifyUser', db_column='SpecifyUserID', related_name='+', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'recordset'
        ordering = ()
        indexes = [
            # models.Index(fields=['name'], name='RecordSetNameIDX')
        ]

    save = partialmethod(custom_save)

class Recordsetitem(models.Model):
    specify_model = datamodel.get_table('recordsetitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='recordsetitemid')

    # Fields
    order = models.IntegerField(blank=True, null=True, unique=False, db_column='OrderNumber', db_index=False)
    recordid = models.IntegerField(blank=False, null=False, unique=False, db_column='RecordId', db_index=False)

    # Relationships: Many-to-One
    recordset = models.ForeignKey('RecordSet', db_column='RecordSetID', related_name='recordsetitems', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recordsetitem'
        ordering = ('recordid',)

    save = partialmethod(custom_save)

class Referencework(models.Model):
    specify_model = datamodel.get_table('referencework')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='referenceworkid')

    # Fields
    doi = models.TextField(blank=True, null=True, unique=False, db_column='Doi', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    ispublished = models.BooleanField(blank=True, null=True, unique=False, db_column='IsPublished', db_index=False)
    isbn = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='ISBN', db_index=False)
    librarynumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='LibraryNumber', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    pages = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Pages', db_index=False)
    placeofpublication = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PlaceOfPublication', db_index=False)
    publisher = models.CharField(blank=True, max_length=250, null=True, unique=False, db_column='Publisher', db_index=False)
    referenceworktype = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='ReferenceWorkType', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=False, max_length=500, null=False, unique=False, db_column='Title', db_index=False)
    uri = models.TextField(blank=True, null=True, unique=False, db_column='Uri', db_index=False)
    url = models.CharField(blank=True, max_length=1024, null=True, unique=False, db_column='URL', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    volume = models.CharField(blank=True, max_length=25, null=True, unique=False, db_column='Volume', db_index=False)
    workdate = models.CharField(blank=True, max_length=25, null=True, unique=False, db_column='WorkDate', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    containedrfparent = models.ForeignKey('ReferenceWork', db_column='ContainedRFParentID', related_name='containedreferenceworks', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    institution = models.ForeignKey('Institution', db_column='InstitutionID', related_name='+', null=False, on_delete=protect_with_blockers)
    journal = models.ForeignKey('Journal', db_column='JournalID', related_name='referenceworks', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'referencework'
        ordering = ()
        indexes = [
            # models.Index(fields=['Title'], name='RefWrkTitleIDX'),
            # models.Index(fields=['Publisher'], name='RefWrkPublisherIDX'),
            # models.Index(fields=['GUID'], name='RefWrkGuidIDX'),
            # models.Index(fields=['ISBN'], name='ISBNIDX')
        ]

    save = partialmethod(custom_save)

class Referenceworkattachment(models.Model):
    specify_model = datamodel.get_table('referenceworkattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='referenceworkattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='referenceworkattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='referenceworkattachments', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'referenceworkattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Repositoryagreement(models.Model):
    specify_model = datamodel.get_table('repositoryagreement')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='repositoryagreementid')

    # Fields
    datereceived = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateReceived', db_index=False)
    enddate = models.DateTimeField(blank=True, null=True, unique=False, db_column='EndDate', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    repositoryagreementnumber = models.CharField(blank=False, max_length=60, null=False, unique=False, db_column='RepositoryAgreementNumber', db_index=False)
    startdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='StartDate', db_index=False)
    status = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Status', db_index=False)
    text1 = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Text3', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    addressofrecord = models.ForeignKey('AddressOfRecord', db_column='AddressOfRecordID', related_name='repositoryagreements', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    originator = models.ForeignKey('Agent', db_column='AgentID', related_name='+', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'repositoryagreement'
        ordering = ()
        indexes = [
            # models.Index(fields=['RepositoryAgreementNumber'], name='RefWrkNumberIDX'),
            # models.Index(fields=['StartDate'], name='RefWrkStartDate')
        ]

    save = partialmethod(custom_save)

class Repositoryagreementattachment(models.Model):
    specify_model = datamodel.get_table('repositoryagreementattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='repositoryagreementattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=True, null=True, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='repositoryagreementattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    repositoryagreement = models.ForeignKey('RepositoryAgreement', db_column='RepositoryAgreementID', related_name='repositoryagreementattachments', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'repositoryagreementattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Shipment(models.Model):
    specify_model = datamodel.get_table('shipment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='shipmentid')

    # Fields
    insuredforamount = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='InsuredForAmount', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    numberofpackages = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='NumberOfPackages', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    shipmentdate = models.DateTimeField(blank=True, null=True, unique=False, db_column='ShipmentDate', db_index=False)
    shipmentmethod = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='ShipmentMethod', db_index=False)
    shipmentnumber = models.CharField(blank=False, max_length=50, null=False, unique=False, db_column='ShipmentNumber', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    weight = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Weight', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    borrow = models.ForeignKey('Borrow', db_column='BorrowID', related_name='shipments', null=True, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=False, on_delete=protect_with_blockers)
    exchangeout = models.ForeignKey('ExchangeOut', db_column='ExchangeOutID', related_name='shipments', null=True, on_delete=protect_with_blockers)
    gift = models.ForeignKey('Gift', db_column='GiftID', related_name='shipments', null=True, on_delete=models.CASCADE)
    loan = models.ForeignKey('Loan', db_column='LoanID', related_name='shipments', null=True, on_delete=models.CASCADE)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    shippedby = models.ForeignKey('Agent', db_column='ShippedByID', related_name='+', null=True, on_delete=protect_with_blockers)
    shippedto = models.ForeignKey('Agent', db_column='ShippedToID', related_name='+', null=True, on_delete=protect_with_blockers)
    shipper = models.ForeignKey('Agent', db_column='ShipperID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'shipment'
        ordering = ()
        indexes = [
            # models.Index(fields=['ShipmentNumber'], name='ShipmentNumberIDX'),
            # models.Index(fields=['ShipmentDate'], name='ShipmentDateIDX'),
            # models.Index(fields=['DisciplineID'], name='ShipmentDspMemIDX'),
            # models.Index(fields=['ShipmentMethod'], name='ShipmentMethodIDX')
        ]

    save = partialmethod(custom_save)

class Spappresource(models.Model):
    specify_model = datamodel.get_table('spappresource')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spappresourceid')

    # Fields
    allpermissionlevel = models.IntegerField(blank=True, null=True, unique=False, db_column='AllPermissionLevel', db_index=False)
    description = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Description', db_index=False)
    grouppermissionlevel = models.IntegerField(blank=True, null=True, unique=False, db_column='GroupPermissionLevel', db_index=False)
    level = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='Level', db_index=False)
    metadata = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='MetaData', db_index=False)
    mimetype = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='MimeType', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    ownerpermissionlevel = models.IntegerField(blank=True, null=True, unique=False, db_column='OwnerPermissionLevel', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    group = models.ForeignKey('SpPrincipal', db_column='SpPrincipalID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    spappresourcedir = models.ForeignKey('SpAppResourceDir', db_column='SpAppResourceDirID', related_name='sppersistedappresources', null=False, on_delete=models.CASCADE)
    specifyuser = models.ForeignKey('SpecifyUser', db_column='SpecifyUserID', related_name='spappresources', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'spappresource'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='SpAppResNameIDX'),
            # models.Index(fields=['MimeType'], name='SpAppResMimeTypeIDX')
        ]

    save = partialmethod(custom_save)

class Spappresourcedata(models.Model):
    specify_model = datamodel.get_table('spappresourcedata')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spappresourcedataid')

    # Fields
    data = models.TextField(blank=True, null=True, unique=False, db_column='data', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    spappresource = models.ForeignKey('SpAppResource', db_column='SpAppResourceID', related_name='spappresourcedatas', null=True, on_delete=models.CASCADE)
    spviewsetobj = models.ForeignKey('SpViewSetObj', db_column='SpViewSetObjID', related_name='spappresourcedatas', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'spappresourcedata'
        ordering = ()

    save = partialmethod(custom_save)

class Spappresourcedir(models.Model):
    specify_model = datamodel.get_table('spappresourcedir')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spappresourcedirid')

    # Fields
    disciplinetype = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='DisciplineType', db_index=False)
    ispersonal = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsPersonal', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    usertype = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='UserType', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collection = models.ForeignKey('Collection', db_column='CollectionID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    specifyuser = models.ForeignKey('SpecifyUser', db_column='SpecifyUserID', related_name='spappresourcedirs', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'spappresourcedir'
        ordering = ()
        indexes = [
            # models.Index(fields=['DisciplineType'], name='SpAppResourceDirDispTypeIDX')
        ]

    save = partialmethod(custom_save)

class Spauditlog(models.Model):
    specify_model = datamodel.get_table('spauditlog')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spauditlogid')

    # Fields
    action = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='Action', db_index=False)
    parentrecordid = models.IntegerField(blank=True, null=True, unique=False, db_column='ParentRecordId', db_index=False)
    parenttablenum = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='ParentTableNum', db_index=False)
    recordid = models.IntegerField(blank=True, null=True, unique=False, db_column='RecordId', db_index=False)
    recordversion = models.IntegerField(blank=False, null=False, unique=False, db_column='RecordVersion', db_index=False)
    tablenum = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='TableNum', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spauditlog'
        ordering = ()

    save = partialmethod(custom_save)

class Spauditlogfield(models.Model):
    specify_model = datamodel.get_table('spauditlogfield')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spauditlogfieldid')

    # Fields
    fieldname = models.CharField(blank=False, max_length=128, null=False, unique=False, db_column='FieldName', db_index=False)
    newvalue = models.TextField(blank=True, null=True, unique=False, db_column='NewValue', db_index=False)
    oldvalue = models.TextField(blank=True, null=True, unique=False, db_column='OldValue', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    spauditlog = models.ForeignKey('SpAuditLog', db_column='SpAuditLogID', related_name='fields', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spauditlogfield'
        ordering = ()

    save = partialmethod(custom_save)

class Spexportschema(models.Model):
    specify_model = datamodel.get_table('spexportschema')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spexportschemaid')

    # Fields
    description = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Description', db_index=False)
    schemaname = models.CharField(blank=True, max_length=80, null=True, unique=False, db_column='SchemaName', db_index=False)
    schemaversion = models.CharField(blank=True, max_length=80, null=True, unique=False, db_column='SchemaVersion', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='spexportschemas', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spexportschema'
        ordering = ()

    save = partialmethod(custom_save)

class Spexportschemaitem(models.Model):
    specify_model = datamodel.get_table('spexportschemaitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spexportschemaitemid')

    # Fields
    datatype = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='DataType', db_index=False)
    description = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Description', db_index=False)
    fieldname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='FieldName', db_index=False)
    formatter = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Formatter', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    spexportschema = models.ForeignKey('SpExportSchema', db_column='SpExportSchemaID', related_name='spexportschemaitems', null=False, on_delete=protect_with_blockers)
    splocalecontaineritem = models.ForeignKey('SpLocaleContainerItem', db_column='SpLocaleContainerItemID', related_name='spexportschemaitems', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spexportschemaitem'
        ordering = ()

    save = partialmethod(custom_save)

class Spexportschemaitemmapping(models.Model):
    specify_model = datamodel.get_table('spexportschemaitemmapping')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spexportschemaitemmappingid')

    # Fields
    exportedfieldname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='ExportedFieldName', db_index=False)
    extensionitem = models.BooleanField(blank=True, null=True, unique=False, db_column='ExtensionItem', db_index=False)
    remarks = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Remarks', db_index=False)
    rowtype = models.CharField(blank=True, max_length=500, null=True, unique=False, db_column='RowType', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    exportschemaitem = models.ForeignKey('SpExportSchemaItem', db_column='ExportSchemaItemID', related_name='+', null=True, on_delete=protect_with_blockers)
    exportschemamapping = models.ForeignKey('SpExportSchemaMapping', db_column='SpExportSchemaMappingID', related_name='mappings', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    queryfield = models.ForeignKey('SpQueryField', db_column='SpQueryFieldID', related_name='mappings', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spexportschemaitemmapping'
        ordering = ()

    save = partialmethod(custom_save)

class Spexportschemamapping(models.Model):
    specify_model = datamodel.get_table('spexportschemamapping')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spexportschemamappingid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    description = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Description', db_index=False)
    mappingname = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='MappingName', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampexported = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimeStampExported', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spexportschemamapping'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='SPEXPSCHMMAPColMemIDX')
        ]

    save = partialmethod(custom_save)

class Spfieldvaluedefault(models.Model):
    specify_model = datamodel.get_table('spfieldvaluedefault')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spfieldvaluedefaultid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    fieldname = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FieldName', db_index=False)
    idvalue = models.IntegerField(blank=True, null=True, unique=False, db_column='IdValue', db_index=False)
    strvalue = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='StrValue', db_index=False)
    tablename = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='TableName', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spfieldvaluedefault'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='SpFieldValueDefaultColMemIDX')
        ]

    save = partialmethod(custom_save)

class Splocalecontainer(models.Model):
    specify_model = datamodel.get_table('splocalecontainer')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='splocalecontainerid')

    # Fields
    aggregator = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Aggregator', db_index=False)
    defaultui = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='DefaultUI', db_index=False)
    format = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Format', db_index=False)
    ishidden = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsHidden', db_index=False)
    issystem = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsSystem', db_index=False)
    isuiformatter = models.BooleanField(blank=True, null=True, unique=False, db_column='IsUIFormatter', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    picklistname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='PickListName', db_index=False)
    schematype = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='SchemaType', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='splocalecontainers', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'splocalecontainer'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='SpLocaleContainerNameIDX')
        ]

    save = partialmethod(custom_save)

class Splocalecontaineritem(models.Model):
    specify_model = datamodel.get_table('splocalecontaineritem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='splocalecontaineritemid')

    # Fields
    format = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Format', db_index=False)
    ishidden = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsHidden', db_index=False)
    isrequired = models.BooleanField(blank=True, null=True, unique=False, db_column='IsRequired', db_index=False)
    issystem = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsSystem', db_index=False)
    isuiformatter = models.BooleanField(blank=True, null=True, unique=False, db_column='IsUIFormatter', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    picklistname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='PickListName', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    type = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    weblinkname = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='WebLinkName', db_index=False)

    # Relationships: Many-to-One
    container = models.ForeignKey('SpLocaleContainer', db_column='SpLocaleContainerID', related_name='items', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'splocalecontaineritem'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='SpLocaleContainerItemNameIDX')
        ]

    save = partialmethod(custom_save)

class Splocaleitemstr(models.Model):
    specify_model = datamodel.get_table('splocaleitemstr')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='splocaleitemstrid')

    # Fields
    country = models.CharField(blank=True, max_length=2, null=True, unique=False, db_column='Country', db_index=False)
    language = models.CharField(blank=False, max_length=2, null=False, unique=False, db_column='Language', db_index=False)
    text = models.CharField(blank=False, max_length=2048, null=False, unique=False, db_column='Text', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    variant = models.CharField(blank=True, max_length=2, null=True, unique=False, db_column='Variant', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    containerdesc = models.ForeignKey('SpLocaleContainer', db_column='SpLocaleContainerDescID', related_name='descs', null=True, on_delete=protect_with_blockers)
    containername = models.ForeignKey('SpLocaleContainer', db_column='SpLocaleContainerNameID', related_name='names', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    itemdesc = models.ForeignKey('SpLocaleContainerItem', db_column='SpLocaleContainerItemDescID', related_name='descs', null=True, on_delete=protect_with_blockers)
    itemname = models.ForeignKey('SpLocaleContainerItem', db_column='SpLocaleContainerItemNameID', related_name='names', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'splocaleitemstr'
        ordering = ()
        indexes = [
            # models.Index(fields=['Language'], name='SpLocaleLanguageIDX'),
            # models.Index(fields=['Country'], name='SpLocaleCountyIDX')
        ]

    save = partialmethod(custom_save)

class Sppermission(models.Model):
    specify_model = datamodel.get_table('sppermission')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='sppermissionid')

    # Fields
    actions = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Actions', db_index=False)
    name = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Name', db_index=False)
    permissionclass = models.CharField(blank=False, max_length=256, null=False, unique=False, db_column='PermissionClass', db_index=False)
    targetid = models.IntegerField(blank=True, null=True, unique=False, db_column='TargetId', db_index=False)

    class Meta:
        db_table = 'sppermission'
        ordering = ()

    save = partialmethod(custom_save)

class Spprincipal(models.Model):
    specify_model = datamodel.get_table('spprincipal')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spprincipalid')

    # Fields
    groupsubclass = models.CharField(blank=False, max_length=255, null=False, unique=False, db_column='GroupSubClass', db_index=False)
    grouptype = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='groupType', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    priority = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='Priority', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    userGroupScopeID = models.IntegerField(blank=True, null=True, db_column='userGroupScopeID')

    class Meta:
        db_table = 'spprincipal'
        ordering = ()

    save = partialmethod(custom_save)

class Spquery(models.Model):
    specify_model = datamodel.get_table('spquery')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spqueryid')

    # Fields
    contextname = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='ContextName', db_index=False)
    contexttableid = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='ContextTableId', db_index=False)
    countonly = models.BooleanField(blank=True, null=True, unique=False, db_column='CountOnly', db_index=False)
    formatauditrecids = models.BooleanField(blank=True, null=True, unique=False, db_column='FormatAuditRecIds', db_index=False)
    isfavorite = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFavorite', db_index=False)
    name = models.CharField(blank=False, max_length=256, null=False, unique=False, db_column='Name', db_index=False)
    ordinal = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    searchsynonymy = models.BooleanField(blank=True, null=True, unique=False, db_column='SearchSynonymy', db_index=False)
    selectdistinct = models.BooleanField(blank=True, null=True, unique=False, db_column='SelectDistinct', db_index=False)
    smushed = models.BooleanField(blank=True, null=True, unique=False, db_column='Smushed', db_index=False)
    sqlstr = models.TextField(blank=True, null=True, unique=False, db_column='SqlStr', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    specifyuser = models.ForeignKey('SpecifyUser', db_column='SpecifyUserID', related_name='spquerys', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spquery'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='SpQueryNameIDX')
        ]

    save = partialmethod(custom_save)

class Spqueryfield(models.Model):
    specify_model = datamodel.get_table('spqueryfield')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spqueryfieldid')

    # Fields
    allownulls = models.BooleanField(blank=True, null=True, unique=False, db_column='AllowNulls', db_index=False)
    alwaysfilter = models.BooleanField(blank=True, null=True, unique=False, db_column='AlwaysFilter', db_index=False)
    columnalias = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='ColumnAlias', db_index=False)
    contexttableident = models.IntegerField(blank=True, null=True, unique=False, db_column='ContextTableIdent', db_index=False)
    endvalue = models.TextField(blank=True, null=True, unique=False, db_column='EndValue', db_index=False)
    fieldname = models.CharField(blank=False, max_length=32, null=False, unique=False, db_column='FieldName', db_index=False)
    formatname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='FormatName', db_index=False)
    isdisplay = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsDisplay', db_index=False)
    isnot = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsNot', db_index=False)
    isprompt = models.BooleanField(blank=True, null=True, unique=False, db_column='IsPrompt', db_index=False)
    isrelfld = models.BooleanField(blank=True, null=True, unique=False, db_column='IsRelFld', db_index=False)
    operend = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='OperEnd', db_index=False)
    operstart = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='OperStart', db_index=False)
    position = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='Position', db_index=False)
    sorttype = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='SortType', db_index=False)
    startvalue = models.TextField(blank=False, null=False, unique=False, db_column='StartValue', db_index=False)
    stringid = models.CharField(blank=False, max_length=500, null=False, unique=False, db_column='StringId', db_index=False)
    tablelist = models.CharField(blank=False, max_length=500, null=False, unique=False, db_column='TableList', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    query = models.ForeignKey('SpQuery', db_column='SpQueryID', related_name='fields', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'spqueryfield'
        ordering = ('position',)

    save = partialmethod(custom_save)

class Spreport(models.Model):
    specify_model = datamodel.get_table('spreport')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spreportid')

    # Fields
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    repeatcount = models.IntegerField(blank=True, null=True, unique=False, db_column='RepeatCount', db_index=False)
    repeatfield = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='RepeatField', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: One-to-One
    workbenchTemplate = models.OneToOneField('WorkbenchTemplate', db_column='WorkbenchTemplateID', related_name='+', null=True, on_delete=protect_with_blockers)

    # Relationships: Many-to-One
    appresource = models.ForeignKey('SpAppResource', db_column='AppResourceID', related_name='spreports', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    query = models.ForeignKey('SpQuery', db_column='SpQueryID', related_name='reports', null=True, on_delete=protect_with_blockers)
    specifyuser = models.ForeignKey('SpecifyUser', db_column='SpecifyUserID', related_name='+', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spreport'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='SpReportNameIDX')
        ]

    save = partialmethod(custom_save)

class Spsymbiotainstance(models.Model):
    specify_model = datamodel.get_table('spsymbiotainstance')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spsymbiotainstanceid')

    # Fields
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    description = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Description', db_index=False)
    instancename = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='InstanceName', db_index=False)
    lastcachebuild = models.DateTimeField(blank=True, null=True, unique=False, db_column='LastCacheBuild', db_index=False)
    lastpull = models.DateTimeField(blank=True, null=True, unique=False, db_column='LastPull', db_index=False)
    lastpush = models.DateTimeField(blank=True, null=True, unique=False, db_column='LastPush', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    symbiotakey = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='SymbiotaKey', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    schemamapping = models.ForeignKey('SpExportSchemaMapping', db_column='SchemaMappingID', related_name='symbiotainstances', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spsymbiotainstance'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='SPSYMINSTColMemIDX')
        ]

    save = partialmethod(custom_save)

class Sptasksemaphore(models.Model):
    specify_model = datamodel.get_table('sptasksemaphore')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='tasksemaphoreid')

    # Fields
    context = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Context', db_index=False)
    islocked = models.BooleanField(blank=True, null=True, unique=False, db_column='IsLocked', db_index=False)
    lockedtime = models.DateTimeField(blank=True, null=True, unique=False, db_column='LockedTime', db_index=False)
    machinename = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='MachineName', db_index=False)
    scope = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Scope', db_index=False)
    taskname = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='TaskName', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    usagecount = models.IntegerField(blank=True, null=True, unique=False, db_column='UsageCount', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    collection = models.ForeignKey('Collection', db_column='CollectionID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    discipline = models.ForeignKey('Discipline', db_column='DisciplineID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    owner = models.ForeignKey('SpecifyUser', db_column='OwnerID', related_name='tasksemaphores', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'sptasksemaphore'
        ordering = ()

    save = partialmethod(custom_save)

class Spversion(models.Model):
    specify_model = datamodel.get_table('spversion')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spversionid')

    # Fields
    appname = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='AppName', db_index=False)
    appversion = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='AppVersion', db_index=False)
    dbclosedby = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='DbClosedBy', db_index=False)
    isdbclosed = models.BooleanField(blank=True, null=True, unique=False, db_column='IsDBClosed', db_index=False)
    schemaversion = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='SchemaVersion', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    workbenchschemaversion = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='WorkbenchSchemaVersion', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spversion'
        ordering = ()

    save = partialmethod(custom_save)

class Spviewsetobj(models.Model):
    specify_model = datamodel.get_table('spviewsetobj')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spviewsetobjid')

    # Fields
    description = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Description', db_index=False)
    filename = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='FileName', db_index=False)
    level = models.SmallIntegerField(blank=False, null=False, unique=False, db_column='Level', db_index=False)
    metadata = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='MetaData', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    spappresourcedir = models.ForeignKey('SpAppResourceDir', db_column='SpAppResourceDirID', related_name='sppersistedviewsets', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spviewsetobj'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='SpViewObjNameIDX')
        ]

    save = partialmethod(custom_save)

class Spvisualquery(models.Model):
    specify_model = datamodel.get_table('spvisualquery')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='spvisualqueryid')

    # Fields
    description = models.TextField(blank=True, null=True, unique=False, db_column='Description', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    specifyuser = models.ForeignKey('SpecifyUser', db_column='SpecifyUserID', related_name='+', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'spvisualquery'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='SpVisualQueryNameIDX')
        ]

    save = partialmethod(custom_save)

class Specifyuser(model_extras.Specifyuser):
    specify_model = datamodel.get_table('specifyuser')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='specifyuserid')

    # Fields
    accumminloggedin = models.BigIntegerField(blank=True, null=True, unique=False, db_column='AccumMinLoggedIn', db_index=False)
    email = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='EMail', db_index=False)
    isloggedin = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsLoggedIn', db_index=False)
    isloggedinreport = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsLoggedInReport', db_index=False)
    logincollectionname = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='LoginCollectionName', db_index=False)
    logindisciplinename = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='LoginDisciplineName', db_index=False)
    loginouttime = models.DateTimeField(blank=True, null=True, unique=False, db_column='LoginOutTime', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=True, db_column='Name', db_index=False)
    password = models.CharField(blank=False, max_length=255, null=False, unique=False, db_column='Password', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    usertype = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='UserType', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'specifyuser'
        ordering = ()

    # save = partialmethod(custom_save)

class Storage(model_extras.Storage):
    specify_model = datamodel.get_table('storage')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='storageid')

    # Fields
    abbrev = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='Abbrev', db_index=False)
    fullname = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='FullName', db_index=False)
    highestchildnodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='HighestChildNodeNumber', db_index=False)
    isaccepted = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsAccepted', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    nodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='NodeNumber', db_index=False)
    number1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number2', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    timestampversion = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampVersion', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    acceptedstorage = models.ForeignKey('Storage', db_column='AcceptedID', related_name='acceptedchildren', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    definition = models.ForeignKey('StorageTreeDef', db_column='StorageTreeDefID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    definitionitem = models.ForeignKey('StorageTreeDefItem', db_column='StorageTreeDefItemID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('Storage', db_column='ParentID', related_name='children', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'storage'
        ordering = ()
        indexes = [
            # models.Index(fields=['Name'], name='StorNameIDX'),
            # models.Index(fields=['FullName'], name='StorFullNameIDX')
        ]

    save = partialmethod(custom_save)

class Storageattachment(models.Model):
    specify_model = datamodel.get_table('storageattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='storageattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='storageattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    storage = models.ForeignKey('Storage', db_column='StorageID', related_name='storageattachments', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'storageattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Storagetreedef(models.Model):
    specify_model = datamodel.get_table('storagetreedef')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='storagetreedefid')

    # Fields
    fullnamedirection = models.IntegerField(blank=True, null=True, unique=False, db_column='FullNameDirection', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'storagetreedef'
        ordering = ()

    save = partialmethod(custom_save)

class Storagetreedefitem(models.Model):
    specify_model = datamodel.get_table('storagetreedefitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='storagetreedefitemid')

    # Fields
    fullnameseparator = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FullNameSeparator', db_index=False)
    isenforced = models.BooleanField(blank=True, null=True, unique=False, db_column='IsEnforced', db_index=False)
    isinfullname = models.BooleanField(blank=True, null=True, unique=False, db_column='IsInFullName', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    textafter = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextAfter', db_index=False)
    textbefore = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextBefore', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Title', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('StorageTreeDefItem', db_column='ParentItemID', related_name='children', null=True, on_delete=protect_with_blockers)
    treedef = models.ForeignKey('StorageTreeDef', db_column='StorageTreeDefID', related_name='treedefitems', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'storagetreedefitem'
        ordering = ()

    save = partialmethod(custom_save)

class Taxon(model_extras.Taxon):
    specify_model = datamodel.get_table('taxon')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='taxonid')

    # Fields
    author = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Author', db_index=False)
    citesstatus = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='CitesStatus', db_index=False)
    colstatus = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='COLStatus', db_index=False)
    commonname = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='CommonName', db_index=False)
    cultivarname = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='CultivarName', db_index=False)
    environmentalprotectionstatus = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='EnvironmentalProtectionStatus', db_index=False)
    esastatus = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='EsaStatus', db_index=False)
    fullname = models.CharField(blank=True, max_length=512, null=True, unique=False, db_column='FullName', db_index=False)
    groupnumber = models.CharField(blank=True, max_length=20, null=True, unique=False, db_column='GroupNumber', db_index=False)
    guid = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='GUID', db_index=False)
    highestchildnodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='HighestChildNodeNumber', db_index=False)
    integer1 = models.BigIntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.BigIntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.BigIntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    integer4 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer4', db_index=False)
    integer5 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer5', db_index=False)
    isaccepted = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsAccepted', db_index=False)
    ishybrid = models.BooleanField(blank=False, default=False, null=False, unique=False, db_column='IsHybrid', db_index=False)
    isisnumber = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='IsisNumber', db_index=False)
    labelformat = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='LabelFormat', db_index=False)
    lsid = models.TextField(blank=True, null=True, unique=False, db_column='LSID', db_index=False)
    name = models.CharField(blank=False, max_length=256, null=False, unique=False, db_column='Name', db_index=False)
    ncbitaxonnumber = models.CharField(blank=True, max_length=8, null=True, unique=False, db_column='NcbiTaxonNumber', db_index=False)
    nodenumber = models.IntegerField(blank=True, null=True, unique=False, db_column='NodeNumber', db_index=False)
    number1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    source = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Source', db_index=False)
    taxonomicserialnumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='TaxonomicSerialNumber', db_index=False)
    text1 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text1', db_index=False)
    text10 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text10', db_index=False)
    text11 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text11', db_index=False)
    text12 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text12', db_index=False)
    text13 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text13', db_index=False)
    text14 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text14', db_index=False)
    text15 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text15', db_index=False)
    text16 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text16', db_index=False)
    text17 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text17', db_index=False)
    text18 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text18', db_index=False)
    text19 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text19', db_index=False)
    text2 = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='Text2', db_index=False)
    text20 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text20', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    text6 = models.TextField(blank=True, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.TextField(blank=True, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.TextField(blank=True, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.TextField(blank=True, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    unitind1 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='UnitInd1', db_index=False)
    unitind2 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='UnitInd2', db_index=False)
    unitind3 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='UnitInd3', db_index=False)
    unitind4 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='UnitInd4', db_index=False)
    unitname1 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='UnitName1', db_index=False)
    unitname2 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='UnitName2', db_index=False)
    unitname3 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='UnitName3', db_index=False)
    unitname4 = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='UnitName4', db_index=False)
    usfwscode = models.CharField(blank=True, max_length=16, null=True, unique=False, db_column='UsfwsCode', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    visibility = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Visibility', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno10 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo10', db_index=False)
    yesno11 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo11', db_index=False)
    yesno12 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo12', db_index=False)
    yesno13 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo13', db_index=False)
    yesno14 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo14', db_index=False)
    yesno15 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo15', db_index=False)
    yesno16 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo16', db_index=False)
    yesno17 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo17', db_index=False)
    yesno18 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo18', db_index=False)
    yesno19 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo19', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)
    yesno6 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo6', db_index=False)
    yesno7 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo7', db_index=False)
    yesno8 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo8', db_index=False)
    yesno9 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo9', db_index=False)

    # Relationships: Many-to-One
    acceptedtaxon = models.ForeignKey('Taxon', db_column='AcceptedID', related_name='acceptedchildren', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    definition = models.ForeignKey('TaxonTreeDef', db_column='TaxonTreeDefID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    definitionitem = models.ForeignKey('TaxonTreeDefItem', db_column='TaxonTreeDefItemID', related_name='treeentries', null=False, on_delete=protect_with_blockers)
    hybridparent1 = models.ForeignKey('Taxon', db_column='HybridParent1ID', related_name='hybridchildren1', null=True, on_delete=protect_with_blockers)
    hybridparent2 = models.ForeignKey('Taxon', db_column='HybridParent2ID', related_name='hybridchildren2', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('Taxon', db_column='ParentID', related_name='children', null=True, on_delete=protect_with_blockers)
    taxonattribute = models.ForeignKey('TaxonAttribute', db_column='TaxonAttributeID', related_name='taxons', null=True, on_delete=protect_with_blockers)
    visibilitysetby = models.ForeignKey('SpecifyUser', db_column='VisibilitySetByID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'taxon'
        ordering = ()
        indexes = [
            # models.Index(fields=['GUID'], name='TaxonGuidIDX'),
            # models.Index(fields=['TaxonomicSerialNumber'], name='TaxonomicSerialNumberIDX'),
            # models.Index(fields=['CommonName'], name='TaxonCommonNameIDX'),
            # models.Index(fields=['Name'], name='TaxonNameIDX'),
            # models.Index(fields=['FullName'], name='TaxonFullNameIDX'),
            # models.Index(fields=['EnvironmentalProtectionStatus'], name='EnvironmentalProtectionStatusIDX')
        ]

    save = partialmethod(custom_save)

class Taxonattachment(models.Model):
    specify_model = datamodel.get_table('taxonattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='taxonattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='taxonattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    taxon = models.ForeignKey('Taxon', db_column='TaxonID', related_name='taxonattachments', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'taxonattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Taxonattribute(models.Model):
    specify_model = datamodel.get_table('taxonattribute')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='taxonattributeid')

    # Fields
    date1 = models.DateTimeField(blank=True, null=True, unique=False, db_column='Date1', db_index=False)
    date1precision = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='Date1Precision', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number10 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number10', db_index=False)
    number11 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number11', db_index=False)
    number12 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number12', db_index=False)
    number13 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number13', db_index=False)
    number14 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number14', db_index=False)
    number15 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number15', db_index=False)
    number16 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number16', db_index=False)
    number17 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number17', db_index=False)
    number18 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number18', db_index=False)
    number19 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number19', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number20 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number20', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    number6 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number6', db_index=False)
    number7 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number7', db_index=False)
    number8 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number8', db_index=False)
    number9 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number9', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text1', db_index=False)
    text10 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text10', db_index=False)
    text11 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text11', db_index=False)
    text12 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text12', db_index=False)
    text13 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text13', db_index=False)
    text14 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text14', db_index=False)
    text15 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text15', db_index=False)
    text16 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text16', db_index=False)
    text17 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text17', db_index=False)
    text18 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text18', db_index=False)
    text19 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text19', db_index=False)
    text2 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text2', db_index=False)
    text20 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text20', db_index=False)
    text21 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text21', db_index=False)
    text22 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text22', db_index=False)
    text23 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text23', db_index=False)
    text24 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text24', db_index=False)
    text25 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text25', db_index=False)
    text26 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text26', db_index=False)
    text27 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text27', db_index=False)
    text28 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text28', db_index=False)
    text29 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text29', db_index=False)
    text3 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text3', db_index=False)
    text30 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text30', db_index=False)
    text31 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text31', db_index=False)
    text32 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text32', db_index=False)
    text33 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text33', db_index=False)
    text34 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text34', db_index=False)
    text35 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text35', db_index=False)
    text36 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text36', db_index=False)
    text37 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text37', db_index=False)
    text38 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text38', db_index=False)
    text39 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text39', db_index=False)
    text4 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text4', db_index=False)
    text40 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text40', db_index=False)
    text41 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text41', db_index=False)
    text42 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text42', db_index=False)
    text43 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text43', db_index=False)
    text44 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text44', db_index=False)
    text45 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text45', db_index=False)
    text46 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text46', db_index=False)
    text47 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text47', db_index=False)
    text48 = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Text48', db_index=False)
    text49 = models.TextField(blank=True, null=True, unique=False, db_column='Text49', db_index=False)
    text5 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text5', db_index=False)
    text50 = models.TextField(blank=True, null=True, unique=False, db_column='Text50', db_index=False)
    text51 = models.TextField(blank=True, null=True, unique=False, db_column='Text51', db_index=False)
    text52 = models.TextField(blank=True, null=True, unique=False, db_column='Text52', db_index=False)
    text53 = models.TextField(blank=True, null=True, unique=False, db_column='Text53', db_index=False)
    text54 = models.TextField(blank=True, null=True, unique=False, db_column='Text54', db_index=False)
    text55 = models.TextField(blank=True, null=True, unique=False, db_column='Text55', db_index=False)
    text56 = models.TextField(blank=True, null=True, unique=False, db_column='Text56', db_index=False)
    text57 = models.TextField(blank=True, null=True, unique=False, db_column='Text57', db_index=False)
    text58 = models.TextField(blank=True, null=True, unique=False, db_column='Text58', db_index=False)
    text6 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text6', db_index=False)
    text7 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text7', db_index=False)
    text8 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text8', db_index=False)
    text9 = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Text9', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno10 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo10', db_index=False)
    yesno11 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo11', db_index=False)
    yesno12 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo12', db_index=False)
    yesno13 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo13', db_index=False)
    yesno14 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo14', db_index=False)
    yesno15 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo15', db_index=False)
    yesno16 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo16', db_index=False)
    yesno17 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo17', db_index=False)
    yesno18 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo18', db_index=False)
    yesno19 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo19', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno20 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo20', db_index=False)
    yesno21 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo21', db_index=False)
    yesno22 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo22', db_index=False)
    yesno23 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo23', db_index=False)
    yesno24 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo24', db_index=False)
    yesno25 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo25', db_index=False)
    yesno26 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo26', db_index=False)
    yesno27 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo27', db_index=False)
    yesno28 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo28', db_index=False)
    yesno29 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo29', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)
    yesno30 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo30', db_index=False)
    yesno31 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo31', db_index=False)
    yesno32 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo32', db_index=False)
    yesno33 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo33', db_index=False)
    yesno34 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo34', db_index=False)
    yesno35 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo35', db_index=False)
    yesno36 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo36', db_index=False)
    yesno37 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo37', db_index=False)
    yesno38 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo38', db_index=False)
    yesno39 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo39', db_index=False)
    yesno4 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo4', db_index=False)
    yesno40 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo40', db_index=False)
    yesno41 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo41', db_index=False)
    yesno42 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo42', db_index=False)
    yesno43 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo43', db_index=False)
    yesno44 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo44', db_index=False)
    yesno45 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo45', db_index=False)
    yesno46 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo46', db_index=False)
    yesno47 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo47', db_index=False)
    yesno48 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo48', db_index=False)
    yesno49 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo49', db_index=False)
    yesno5 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo5', db_index=False)
    yesno50 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo50', db_index=False)
    yesno51 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo51', db_index=False)
    yesno52 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo52', db_index=False)
    yesno53 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo53', db_index=False)
    yesno54 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo54', db_index=False)
    yesno55 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo55', db_index=False)
    yesno56 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo56', db_index=False)
    yesno57 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo57', db_index=False)
    yesno58 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo58', db_index=False)
    yesno59 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo59', db_index=False)
    yesno6 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo6', db_index=False)
    yesno60 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo60', db_index=False)
    yesno61 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo61', db_index=False)
    yesno62 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo62', db_index=False)
    yesno63 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo63', db_index=False)
    yesno64 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo64', db_index=False)
    yesno65 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo65', db_index=False)
    yesno66 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo66', db_index=False)
    yesno67 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo67', db_index=False)
    yesno68 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo68', db_index=False)
    yesno69 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo69', db_index=False)
    yesno7 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo7', db_index=False)
    yesno70 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo70', db_index=False)
    yesno71 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo71', db_index=False)
    yesno72 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo72', db_index=False)
    yesno73 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo73', db_index=False)
    yesno74 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo74', db_index=False)
    yesno75 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo75', db_index=False)
    yesno76 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo76', db_index=False)
    yesno77 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo77', db_index=False)
    yesno78 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo78', db_index=False)
    yesno79 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo79', db_index=False)
    yesno8 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo8', db_index=False)
    yesno80 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo80', db_index=False)
    yesno81 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo81', db_index=False)
    yesno82 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo82', db_index=False)
    yesno9 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo9', db_index=False)

    # Relationships: Many-to-One
    agent1 = models.ForeignKey('Agent', db_column='Agent1ID', related_name='+', null=True, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'taxonattribute'
        ordering = ()

    save = partialmethod(custom_save)

class Taxoncitation(models.Model):
    specify_model = datamodel.get_table('taxoncitation')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='taxoncitationid')

    # Fields
    figurenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FigureNumber', db_index=False)
    isfigured = models.BooleanField(blank=True, null=True, unique=False, db_column='IsFigured', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    pagenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PageNumber', db_index=False)
    platenumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='PlateNumber', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    referencework = models.ForeignKey('ReferenceWork', db_column='ReferenceWorkID', related_name='taxoncitations', null=False, on_delete=protect_with_blockers)
    taxon = models.ForeignKey('Taxon', db_column='TaxonID', related_name='taxoncitations', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'taxoncitation'
        ordering = ()

    save = partialmethod(custom_save)

class Taxontreedef(models.Model):
    specify_model = datamodel.get_table('taxontreedef')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='taxontreedefid')

    # Fields
    fullnamedirection = models.IntegerField(blank=True, null=True, unique=False, db_column='FullNameDirection', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    remarks = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: One-to-One

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'taxontreedef'
        ordering = ()

    save = partialmethod(custom_save)

class Taxontreedefitem(models.Model):
    specify_model = datamodel.get_table('taxontreedefitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='taxontreedefitemid')

    # Fields
    formattoken = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FormatToken', db_index=False)
    fullnameseparator = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='FullNameSeparator', db_index=False)
    isenforced = models.BooleanField(blank=True, null=True, unique=False, db_column='IsEnforced', db_index=False)
    isinfullname = models.BooleanField(blank=True, null=True, unique=False, db_column='IsInFullName', db_index=False)
    name = models.CharField(blank=False, max_length=64, null=False, unique=False, db_column='Name', db_index=False)
    rankid = models.IntegerField(blank=False, null=False, unique=False, db_column='RankID', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    textafter = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextAfter', db_index=False)
    textbefore = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TextBefore', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    title = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Title', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    parent = models.ForeignKey('TaxonTreeDefItem', db_column='ParentItemID', related_name='children', null=True, on_delete=protect_with_blockers)
    treedef = models.ForeignKey('TaxonTreeDef', db_column='TaxonTreeDefID', related_name='treedefitems', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'taxontreedefitem'
        ordering = ()

    save = partialmethod(custom_save)

class Treatmentevent(models.Model):
    specify_model = datamodel.get_table('treatmentevent')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='treatmenteventid')

    # Fields
    dateboxed = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateBoxed', db_index=False)
    datecleaned = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateCleaned', db_index=False)
    datecompleted = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateCompleted', db_index=False)
    datereceived = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateReceived', db_index=False)
    datetoisolation = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateToIsolation', db_index=False)
    datetreatmentended = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateTreatmentEnded', db_index=False)
    datetreatmentstarted = models.DateTimeField(blank=True, null=True, unique=False, db_column='DateTreatmentStarted', db_index=False)
    fieldnumber = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='FieldNumber', db_index=False)
    location = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Storage', db_index=False)
    number1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    number4 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number4', db_index=False)
    number5 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number5', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    text4 = models.TextField(blank=True, null=True, unique=False, db_column='Text4', db_index=False)
    text5 = models.TextField(blank=True, null=True, unique=False, db_column='Text5', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    treatmentnumber = models.CharField(blank=True, max_length=32, null=True, unique=False, db_column='TreatmentNumber', db_index=False)
    type = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='Type', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)

    # Relationships: Many-to-One
    accession = models.ForeignKey('Accession', db_column='AccessionID', related_name='treatmentevents', null=True, on_delete=protect_with_blockers)
    authorizedby = models.ForeignKey('Agent', db_column='AuthorizedByID', related_name='+', null=True, on_delete=protect_with_blockers)
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='treatmentevents', null=True, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    division = models.ForeignKey('Division', db_column='DivisionID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    performedby = models.ForeignKey('Agent', db_column='PerformedByID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'treatmentevent'
        ordering = ()
        indexes = [
            # models.Index(fields=['DateReceived'], name='TEDateReceivedIDX'),
            # models.Index(fields=['DateTreatmentStarted'], name='TEDateTreatmentStartedIDX'),
            # models.Index(fields=['FieldNumber'], name='TEFieldNumberIDX'),
            # models.Index(fields=['TreatmentNumber'], name='TETreatmentNumberIDX')
        ]

    save = partialmethod(custom_save)

class Treatmenteventattachment(models.Model):
    specify_model = datamodel.get_table('treatmenteventattachment')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='treatmenteventattachmentid')

    # Fields
    ordinal = models.IntegerField(blank=False, null=False, unique=False, db_column='Ordinal', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    attachment = models.ForeignKey('Attachment', db_column='AttachmentID', related_name='treatmenteventattachments', null=False, on_delete=protect_with_blockers)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    treatmentevent = models.ForeignKey('TreatmentEvent', db_column='TreatmentEventID', related_name='treatmenteventattachments', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'treatmenteventattachment'
        ordering = ()

    save = partialmethod(custom_save)

class Voucherrelationship(models.Model):
    specify_model = datamodel.get_table('voucherrelationship')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='voucherrelationshipid')

    # Fields
    collectioncode = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='CollectionCode', db_index=False)
    collectionmemberid = models.IntegerField(blank=False, null=False, unique=False, db_column='CollectionMemberID', db_index=False)
    institutioncode = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='InstitutionCode', db_index=False)
    integer1 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer1', db_index=False)
    integer2 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer2', db_index=False)
    integer3 = models.IntegerField(blank=True, null=True, unique=False, db_column='Integer3', db_index=False)
    number1 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number1', db_index=False)
    number2 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number2', db_index=False)
    number3 = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='Number3', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    text1 = models.TextField(blank=True, null=True, unique=False, db_column='Text1', db_index=False)
    text2 = models.TextField(blank=True, null=True, unique=False, db_column='Text2', db_index=False)
    text3 = models.TextField(blank=True, null=True, unique=False, db_column='Text3', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    urllink = models.CharField(blank=True, max_length=1024, null=True, unique=False, db_column='UrlLink', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    vouchernumber = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='VoucherNumber', db_index=False)
    yesno1 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo1', db_index=False)
    yesno2 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo2', db_index=False)
    yesno3 = models.BooleanField(blank=True, null=True, unique=False, db_column='YesNo3', db_index=False)

    # Relationships: Many-to-One
    collectionobject = models.ForeignKey('CollectionObject', db_column='CollectionObjectID', related_name='voucherrelationships', null=False, on_delete=models.CASCADE)
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'voucherrelationship'
        ordering = ()
        indexes = [
            # models.Index(fields=['CollectionMemberID'], name='VRXDATColMemIDX')
        ]

    save = partialmethod(custom_save)

class Workbench(models.Model):
    specify_model = datamodel.get_table('workbench')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='workbenchid')

    # Fields
    allpermissionlevel = models.IntegerField(blank=True, null=True, unique=False, db_column='AllPermissionLevel', db_index=False)
    dbtableid = models.IntegerField(blank=True, null=True, unique=False, db_column='TableID', db_index=False)
    exportinstitutionname = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ExportInstitutionName', db_index=False)
    exportedfromtablename = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='ExportedFromTableName', db_index=False)
    formid = models.IntegerField(blank=True, null=True, unique=False, db_column='FormId', db_index=False)
    grouppermissionlevel = models.IntegerField(blank=True, null=True, unique=False, db_column='GroupPermissionLevel', db_index=False)
    lockedbyusername = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='LockedByUserName', db_index=False)
    name = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Name', db_index=False)
    ownerpermissionlevel = models.IntegerField(blank=True, null=True, unique=False, db_column='OwnerPermissionLevel', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    srcfilepath = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='SrcFilePath', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    group = models.ForeignKey('SpPrincipal', db_column='SpPrincipalID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    specifyuser = models.ForeignKey('SpecifyUser', db_column='SpecifyUserID', related_name='workbenches', null=False, on_delete=protect_with_blockers)
    workbenchtemplate = models.ForeignKey('WorkbenchTemplate', db_column='WorkbenchTemplateID', related_name='workbenches', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'workbench'
        ordering = ()
        indexes = [
            # models.Index(fields=['name'], name='WorkbenchNameIDX')
        ]

    save = partialmethod(custom_save)

class Workbenchdataitem(models.Model):
    specify_model = datamodel.get_table('workbenchdataitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='workbenchdataitemid')

    # Fields
    celldata = models.TextField(blank=True, null=True, unique=False, db_column='CellData', db_index=False)
    rownumber = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='RowNumber', db_index=False)
    validationstatus = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='ValidationStatus', db_index=False)

    # Relationships: Many-to-One
    workbenchrow = models.ForeignKey('WorkbenchRow', db_column='WorkbenchRowID', related_name='workbenchdataitems', null=False, on_delete=models.DO_NOTHING)
    workbenchtemplatemappingitem = models.ForeignKey('WorkbenchTemplateMappingItem', db_column='WorkbenchTemplateMappingItemID', related_name='workbenchdataitems', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'workbenchdataitem'
        ordering = ()
        indexes = [
            # models.Index(fields=['rowNumber'], name='DataItemRowNumberIDX')
        ]

    save = partialmethod(custom_save)

class Workbenchrow(models.Model):
    specify_model = datamodel.get_table('workbenchrow')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='workbenchrowid')

    # Fields
    biogeomancerresults = models.TextField(blank=True, null=True, unique=False, db_column='BioGeomancerResults', db_index=False)
    cardimagedata = models.TextField(blank=True, null=True, unique=False, db_column='CardImageData', db_index=False)
    cardimagefullpath = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='CardImageFullPath', db_index=False)
    errorestimate = models.DecimalField(blank=True, max_digits=22, decimal_places=10, null=True, unique=False, db_column='ErrorEstimate', db_index=False)
    errorpolygon = models.TextField(blank=True, null=True, unique=False, db_column='ErrorPolygon', db_index=False)
    lat1text = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Lat1Text', db_index=False)
    lat2text = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Lat2Text', db_index=False)
    long1text = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Long1Text', db_index=False)
    long2text = models.CharField(blank=True, max_length=50, null=True, unique=False, db_column='Long2Text', db_index=False)
    recordid = models.IntegerField(blank=True, null=True, unique=False, db_column='RecordID', db_index=False)
    rownumber = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='RowNumber', db_index=False)
    sgrstatus = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='SGRStatus', db_index=False)
    uploadstatus = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='UploadStatus', db_index=False)

    # Relationships: Many-to-One
    workbench = models.ForeignKey('Workbench', db_column='WorkbenchID', related_name='workbenchrows', null=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'workbenchrow'
        ordering = ()
        indexes = [
            # models.Index(fields=['RowNumber'], name='RowNumberIDX')
        ]

    save = partialmethod(custom_save)

class Workbenchrowexportedrelationship(models.Model):
    specify_model = datamodel.get_table('workbenchrowexportedrelationship')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='workbenchrowexportedrelationshipid')

    # Fields
    recordid = models.IntegerField(blank=True, null=True, unique=False, db_column='RecordID', db_index=False)
    relationshipname = models.CharField(blank=True, max_length=120, null=True, unique=False, db_column='RelationshipName', db_index=False)
    sequence = models.IntegerField(blank=True, null=True, unique=False, db_column='Sequence', db_index=False)
    tablename = models.CharField(blank=True, max_length=120, null=True, unique=False, db_column='TableName', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    workbenchrow = models.ForeignKey('WorkbenchRow', db_column='WorkbenchRowID', related_name='workbenchrowexportedrelationships', null=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'workbenchrowexportedrelationship'
        ordering = ()

    save = partialmethod(custom_save)

class Workbenchrowimage(models.Model):
    specify_model = datamodel.get_table('workbenchrowimage')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='workbenchrowimageid')

    # Fields
    attachtotablename = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='AttachToTableName', db_index=False)
    cardimagedata = models.TextField(blank=True, null=True, unique=False, db_column='CardImageData', db_index=False)
    cardimagefullpath = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='CardImageFullPath', db_index=False)
    imageorder = models.IntegerField(blank=True, null=True, unique=False, db_column='ImageOrder', db_index=False)

    # Relationships: Many-to-One
    workbenchrow = models.ForeignKey('WorkbenchRow', db_column='WorkbenchRowID', related_name='workbenchrowimages', null=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'workbenchrowimage'
        ordering = ()

    save = partialmethod(custom_save)

class Workbenchtemplate(models.Model):
    specify_model = datamodel.get_table('workbenchtemplate')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='workbenchtemplateid')

    # Fields
    name = models.CharField(blank=True, max_length=256, null=True, unique=False, db_column='Name', db_index=False)
    remarks = models.TextField(blank=True, null=True, unique=False, db_column='Remarks', db_index=False)
    srcfilepath = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='SrcFilePath', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    specifyuser = models.ForeignKey('SpecifyUser', db_column='SpecifyUserID', related_name='workbenchtemplates', null=False, on_delete=protect_with_blockers)

    class Meta:
        db_table = 'workbenchtemplate'
        ordering = ()

    save = partialmethod(custom_save)

class Workbenchtemplatemappingitem(models.Model):
    specify_model = datamodel.get_table('workbenchtemplatemappingitem')

    # ID Field
    id = models.AutoField(primary_key=True, db_column='workbenchtemplatemappingitemid')

    # Fields
    caption = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='Caption', db_index=False)
    carryforward = models.BooleanField(blank=True, null=True, unique=False, db_column='CarryForward', db_index=False)
    datafieldlength = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='DataFieldLength', db_index=False)
    fieldname = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='FieldName', db_index=False)
    fieldtype = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='FieldType', db_index=False)
    importedcolname = models.CharField(blank=True, max_length=255, null=True, unique=False, db_column='ImportedColName', db_index=False)
    iseditable = models.BooleanField(blank=True, null=True, unique=False, db_column='IsEditable', db_index=False)
    isexportabletocontent = models.BooleanField(blank=True, null=True, unique=False, db_column='IsExportableToContent', db_index=False)
    isincludedintitle = models.BooleanField(blank=True, null=True, unique=False, db_column='IsIncludedInTitle', db_index=False)
    isrequired = models.BooleanField(blank=True, null=True, unique=False, db_column='IsRequired', db_index=False)
    metadata = models.CharField(blank=True, max_length=128, null=True, unique=False, db_column='MetaData', db_index=False)
    origimportcolumnindex = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='DataColumnIndex', db_index=False)
    srctableid = models.IntegerField(blank=True, null=True, unique=False, db_column='TableId', db_index=False)
    tablename = models.CharField(blank=True, max_length=64, null=True, unique=False, db_column='TableName', db_index=False)
    timestampcreated = models.DateTimeField(blank=False, null=False, unique=False, db_column='TimestampCreated', db_index=False)
    timestampmodified = models.DateTimeField(blank=True, null=True, unique=False, db_column='TimestampModified', db_index=False)
    version = models.IntegerField(blank=True, null=True, unique=False, db_column='Version', db_index=False)
    vieworder = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='ViewOrder', db_index=False)
    xcoord = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='XCoord', db_index=False)
    ycoord = models.SmallIntegerField(blank=True, null=True, unique=False, db_column='YCoord', db_index=False)

    # Relationships: Many-to-One
    createdbyagent = models.ForeignKey('Agent', db_column='CreatedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    modifiedbyagent = models.ForeignKey('Agent', db_column='ModifiedByAgentID', related_name='+', null=True, on_delete=protect_with_blockers)
    workbenchtemplate = models.ForeignKey('WorkbenchTemplate', db_column='WorkbenchTemplateID', related_name='workbenchtemplatemappingitems', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'workbenchtemplatemappingitem'
        ordering = ()

    save = partialmethod(custom_save)

from specifyweb.workbench.models import Spdataset

# models_by_tableid = {
#     7: Accession,
#     12: Accessionagent,
#     108: Accessionattachment,
#     13: Accessionauthorization,
#     159: Accessioncitation,
#     8: Address,
#     125: Addressofrecord,
#     5: Agent,
#     109: Agentattachment,
#     78: Agentgeography,
#     168: Agentidentifier,
#     86: Agentspecialty,
#     107: Agentvariant,
#     67: Appraisal,
#     41: Attachment,
#     139: Attachmentimageattribute,
#     42: Attachmentmetadata,
#     130: Attachmenttag,
#     16: Attributedef,
#     17: Author,
#     97: Autonumberingscheme,
#     18: Borrow,
#     19: Borrowagent,
#     145: Borrowattachment,
#     20: Borrowmaterial,
#     21: Borrowreturnmaterial,
#     10: Collectingevent,
#     110: Collectingeventattachment,
#     25: Collectingeventattr,
#     92: Collectingeventattribute,
#     152: Collectingeventauthorization,
#     87: Collectingtrip,
#     156: Collectingtripattachment,
#     157: Collectingtripattribute,
#     158: Collectingtripauthorization,
#     23: Collection,
#     1: Collectionobject,
#     111: Collectionobjectattachment,
#     28: Collectionobjectattr,
#     93: Collectionobjectattribute,
#     29: Collectionobjectcitation,
#     153: Collectionobjectproperty,
#     98: Collectionreltype,
#     99: Collectionrelationship,
#     30: Collector,
#     106: Commonnametx,
#     134: Commonnametxcitation,
#     103: Conservdescription,
#     112: Conservdescriptionattachment,
#     73: Conservevent,
#     113: Conserveventattachment,
#     31: Container,
#     150: Dnaprimer,
#     121: Dnasequence,
#     147: Dnasequenceattachment,
#     88: Dnasequencingrun,
#     135: Dnasequencingrunattachment,
#     105: Dnasequencingruncitation,
#     33: Datatype,
#     163: Deaccession,
#     164: Deaccessionagent,
#     165: Deaccessionattachment,
#     9: Determination,
#     38: Determinationcitation,
#     167: Determiner,
#     26: Discipline,
#     34: Disposal,
#     35: Disposalagent,
#     166: Disposalattachment,
#     36: Disposalpreparation,
#     96: Division,
#     39: Exchangein,
#     169: Exchangeinattachment,
#     140: Exchangeinprep,
#     40: Exchangeout,
#     170: Exchangeoutattachment,
#     141: Exchangeoutprep,
#     89: Exsiccata,
#     104: Exsiccataitem,
#     160: Extractor,
#     83: Fieldnotebook,
#     127: Fieldnotebookattachment,
#     85: Fieldnotebookpage,
#     129: Fieldnotebookpageattachment,
#     84: Fieldnotebookpageset,
#     128: Fieldnotebookpagesetattachment,
#     146: Fundingagent,
#     123: Geocoorddetail,
#     3: Geography,
#     44: Geographytreedef,
#     45: Geographytreedefitem,
#     46: Geologictimeperiod,
#     47: Geologictimeperiodtreedef,
#     48: Geologictimeperiodtreedefitem,
#     131: Gift,
#     133: Giftagent,
#     144: Giftattachment,
#     132: Giftpreparation,
#     49: Groupperson,
#     50: Inforequest,
#     94: Institution,
#     142: Institutionnetwork,
#     51: Journal,
#     136: Latlonpolygon,
#     137: Latlonpolygonpnt,
#     100: Lithostrat,
#     101: Lithostrattreedef,
#     102: Lithostrattreedefitem,
#     52: Loan,
#     53: Loanagent,
#     114: Loanattachment,
#     54: Loanpreparation,
#     55: Loanreturnpreparation,
#     2: Locality,
#     115: Localityattachment,
#     57: Localitycitation,
#     124: Localitydetail,
#     120: Localitynamealias,
#     151: Materialsample,
#     138: Morphbankview,
#     61: Otheridentifier,
#     32: Paleocontext,
#     161: Pcrperson,
#     6: Permit,
#     116: Permitattachment,
#     500: Picklist,
#     501: Picklistitem,
#     65: Preptype,
#     63: Preparation,
#     117: Preparationattachment,
#     64: Preparationattr,
#     91: Preparationattribute,
#     154: Preparationproperty,
#     66: Project,
#     68: Recordset,
#     502: Recordsetitem,
#     69: Referencework,
#     143: Referenceworkattachment,
#     70: Repositoryagreement,
#     118: Repositoryagreementattachment,
#     71: Shipment,
#     514: Spappresource,
#     515: Spappresourcedata,
#     516: Spappresourcedir,
#     530: Spauditlog,
#     531: Spauditlogfield,
#     524: Spexportschema,
#     525: Spexportschemaitem,
#     527: Spexportschemaitemmapping,
#     528: Spexportschemamapping,
#     520: Spfieldvaluedefault,
#     503: Splocalecontainer,
#     504: Splocalecontaineritem,
#     505: Splocaleitemstr,
#     521: Sppermission,
#     522: Spprincipal,
#     517: Spquery,
#     518: Spqueryfield,
#     519: Spreport,
#     533: Spsymbiotainstance,
#     526: Sptasksemaphore,
#     529: Spversion,
#     513: Spviewsetobj,
#     532: Spvisualquery,
#     72: Specifyuser,
#     58: Storage,
#     148: Storageattachment,
#     59: Storagetreedef,
#     60: Storagetreedefitem,
#     4: Taxon,
#     119: Taxonattachment,
#     162: Taxonattribute,
#     75: Taxoncitation,
#     76: Taxontreedef,
#     77: Taxontreedefitem,
#     122: Treatmentevent,
#     149: Treatmenteventattachment,
#     155: Voucherrelationship,
#     79: Workbench,
#     80: Workbenchdataitem,
#     90: Workbenchrow,
#     126: Workbenchrowexportedrelationship,
#     95: Workbenchrowimage,
#     81: Workbenchtemplate,
#     82: Workbenchtemplatemappingitem,
#     # 1000: Spuserexternalid, # set in own models module
#     # 1001: Spattachmentdataset, # set in own models module
#     # 1002: UniquenessRule, # set in own models module
#     # 1003: UniquenessRule_Field, # set in own models module
#     # 1004: Message, # set in own models module
#     # 1005: Spmerging, # set in own models module
#     # 1006: UserPolicy, # set in own models module
#     # 1007: Role, # set in own models module
#     # 1008: LibraryRole, # set in own models module
#     # 1009: UserRole, # set in own models module
#     # 1010: RolePolicy, # set in own models module
#     # 1011: LibraryRolePolicy, # set in own models module
#     1012: Spdataset # set in own models module
# }
