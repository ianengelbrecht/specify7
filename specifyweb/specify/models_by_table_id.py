# from django.apps import apps
# from django.core.exceptions import AppRegistryNotReady

# This needed to be move from specify.models to it's own module to avoid circular imports
model_names_by_table_id = {
    7:'Accession',
    12:'Accessionagent',
    108:'Accessionattachment',
    13:'Accessionauthorization',
    159:'Accessioncitation',
    8:'Address',
    125:'Addressofrecord',
    5:'Agent',
    109:'Agentattachment',
    78:'Agentgeography',
    168:'Agentidentifier',
    86:'Agentspecialty',
    107:'Agentvariant',
    67:'Appraisal',
    41:'Attachment',
    139:'Attachmentimageattribute',
    42:'Attachmentmetadata',
    130:'Attachmenttag',
    16:'Attributedef',
    17:'Author',
    97:'Autonumberingscheme',
    18:'Borrow',
    19:'Borrowagent',
    145:'Borrowattachment',
    20:'Borrowmaterial',
    21:'Borrowreturnmaterial',
    10:'Collectingevent',
    110:'Collectingeventattachment',
    25:'Collectingeventattr',
    92:'Collectingeventattribute',
    152:'Collectingeventauthorization',
    87:'Collectingtrip',
    156:'Collectingtripattachment',
    157:'Collectingtripattribute',
    158:'Collectingtripauthorization',
    23:'Collection',
    1:'Collectionobject',
    111:'Collectionobjectattachment',
    28:'Collectionobjectattr',
    93:'Collectionobjectattribute',
    29:'Collectionobjectcitation',
    153:'Collectionobjectproperty',
    98:'Collectionreltype',
    99:'Collectionrelationship',
    30:'Collector',
    106:'Commonnametx',
    134:'Commonnametxcitation',
    103:'Conservdescription',
    112:'Conservdescriptionattachment',
    73:'Conservevent',
    113:'Conserveventattachment',
    31:'Container',
    150:'Dnaprimer',
    121:'Dnasequence',
    147:'Dnasequenceattachment',
    88:'Dnasequencingrun',
    135:'Dnasequencingrunattachment',
    105:'Dnasequencingruncitation',
    33:'Datatype',
    163:'Deaccession',
    164:'Deaccessionagent',
    165:'Deaccessionattachment',
    9:'Determination',
    38:'Determinationcitation',
    167:'Determiner',
    26:'Discipline',
    34:'Disposal',
    35:'Disposalagent',
    166:'Disposalattachment',
    36:'Disposalpreparation',
    96:'Division',
    39:'Exchangein',
    169:'Exchangeinattachment',
    140:'Exchangeinprep',
    40:'Exchangeout',
    170:'Exchangeoutattachment',
    141:'Exchangeoutprep',
    89:'Exsiccata',
    104:'Exsiccataitem',
    160:'Extractor',
    83:'Fieldnotebook',
    127:'Fieldnotebookattachment',
    85:'Fieldnotebookpage',
    129:'Fieldnotebookpageattachment',
    84:'Fieldnotebookpageset',
    128:'Fieldnotebookpagesetattachment',
    146:'Fundingagent',
    123:'Geocoorddetail',
    3:'Geography',
    44:'Geographytreedef',
    45:'Geographytreedefitem',
    46:'Geologictimeperiod',
    47:'Geologictimeperiodtreedef',
    48:'Geologictimeperiodtreedefitem',
    131:'Gift',
    133:'Giftagent',
    144:'Giftattachment',
    132:'Giftpreparation',
    49:'Groupperson',
    50:'Inforequest',
    94:'Institution',
    142:'Institutionnetwork',
    51:'Journal',
    136:'Latlonpolygon',
    137:'Latlonpolygonpnt',
    100:'Lithostrat',
    101:'Lithostrattreedef',
    102:'Lithostrattreedefitem',
    52:'Loan',
    53:'Loanagent',
    114:'Loanattachment',
    54:'Loanpreparation',
    55:'Loanreturnpreparation',
    2:'Locality',
    115:'Localityattachment',
    57:'Localitycitation',
    124:'Localitydetail',
    120:'Localitynamealias',
    151:'Materialsample',
    138:'Morphbankview',
    61:'Otheridentifier',
    32:'Paleocontext',
    161:'Pcrperson',
    6:'Permit',
    116:'Permitattachment',
    500:'Picklist',
    501:'Picklistitem',
    65:'Preptype',
    63:'Preparation',
    117:'Preparationattachment',
    64:'Preparationattr',
    91:'Preparationattribute',
    154:'Preparationproperty',
    66:'Project',
    68:'Recordset',
    502:'Recordsetitem',
    69:'Referencework',
    143:'Referenceworkattachment',
    70:'Repositoryagreement',
    118:'Repositoryagreementattachment',
    71:'Shipment',
    514:'Spappresource',
    515:'Spappresourcedata',
    516:'Spappresourcedir',
    530:'Spauditlog',
    531:'Spauditlogfield',
    524:'Spexportschema',
    525:'Spexportschemaitem',
    527:'Spexportschemaitemmapping',
    528:'Spexportschemamapping',
    520:'Spfieldvaluedefault',
    503:'Splocalecontainer',
    504:'Splocalecontaineritem',
    505:'Splocaleitemstr',
    521:'Sppermission',
    522:'Spprincipal',
    517:'Spquery',
    518:'Spqueryfield',
    519:'Spreport',
    533:'Spsymbiotainstance',
    526:'Sptasksemaphore',
    529:'Spversion',
    513:'Spviewsetobj',
    532:'Spvisualquery',
    72:'Specifyuser',
    58:'Storage',
    148:'Storageattachment',
    59:'Storagetreedef',
    60:'Storagetreedefitem',
    4:'Taxon',
    119:'Taxonattachment',
    162:'Taxonattribute',
    75:'Taxoncitation',
    76:'Taxontreedef',
    77:'Taxontreedefitem',
    122:'Treatmentevent',
    149:'Treatmenteventattachment',
    155:'Voucherrelationship',
    79:'Workbench',
    80:'Workbenchdataitem',
    90:'Workbenchrow',
    126:'Workbenchrowexportedrelationship',
    95:'Workbenchrowimage',
    81:'Workbenchtemplate',
    82:'Workbenchtemplatemappingitem',
    1000:'Spuserexternalid',
    1001:'Spattachmentdataset',
    1002:'UniquenessRule',
    1003:'UniquenessRuleField',
    1004:'Message',
    1005:'Spmerging',
    1006:'UserPolicy',
    1007:'Role',
    1008:'LibraryRole',
    1009:'UserRole',
    1010:'RolePolicy',
    1011:'LibraryRolePolicy',
    1012:'Spdataset',
    1013: 'LocalityUpdate',
    1014: 'LocalityUpdateRowResult',
    1015: 'CollectionObjectType',
    1016: 'CollectionObjectGroup',
    1017: 'CollectionObjectGroupJoin',
}

model_names_by_app = {
    'accounts': {
        'Spuserexternalid'
    },
    'attachment_gw': {
        'Spattachmentdataset'
    },
    'businessrules': {
        'UniquenessRule',
        'UniquenessRuleField'
    },
    'notifications': {
        'Message',
        'Spmerging',
        'LocalityUpdate',
        'LocalityUpdateRowResult'
    },
    'permissions': {
        'UserPolicy',
        'Role',
        'LibraryRole',
        'UserRole',
        'RolePolicy',
        'LibraryRolePolicy'
    },
    'workbench': {
        'Spdataset'
    },
    'specify': {
        'Accession',
        'Accessionagent',
        'Accessionattachment',
        'Accessionauthorization',
        'Accessioncitation',
        'Address',
        'Addressofrecord',
        'Agent',
        'Agentattachment',
        'Agentgeography',
        'Agentidentifier',
        'Agentspecialty',
        'Agentvariant',
        'Appraisal',
        'Attachment',
        'Attachmentimageattribute',
        'Attachmentmetadata',
        'Attachmenttag',
        'Attributedef',
        'Author',
        'Autonumberingscheme',
        'Borrow',
        'Borrowagent',
        'Borrowattachment',
        'Borrowmaterial',
        'Borrowreturnmaterial',
        'Collectingevent',
        'Collectingeventattachment',
        'Collectingeventattr',
        'Collectingeventattribute',
        'Collectingeventauthorization',
        'Collectingtrip',
        'Collectingtripattachment',
        'Collectingtripattribute',
        'Collectingtripauthorization',
        'Collection',
        'Collectionobject',
        'Collectionobjectattachment',
        'Collectionobjectattr',
        'Collectionobjectattribute',
        'Collectionobjectcitation',
        'Collectionobjectproperty',
        'Collectionreltype',
        'Collectionrelationship',
        'Collector',
        'Commonnametx',
        'Commonnametxcitation',
        'Conservdescription',
        'Conservdescriptionattachment',
        'Conservevent',
        'Conserveventattachment',
        'Container',
        'Dnaprimer',
        'Dnasequence',
        'Dnasequenceattachment',
        'Dnasequencingrun',
        'Dnasequencingrunattachment',
        'Dnasequencingruncitation',
        'Datatype',
        'Deaccession',
        'Deaccessionagent',
        'Deaccessionattachment',
        'Determination',
        'Determinationcitation',
        'Determiner',
        'Discipline',
        'Disposal',
        'Disposalagent',
        'Disposalattachment',
        'Disposalpreparation',
        'Division',
        'Exchangein',
        'Exchangeinattachment',
        'Exchangeinprep',
        'Exchangeout',
        'Exchangeoutattachment',
        'Exchangeoutprep',
        'Exsiccata',
        'Exsiccataitem',
        'Extractor',
        'Fieldnotebook',
        'Fieldnotebookattachment',
        'Fieldnotebookpage',
        'Fieldnotebookpageattachment',
        'Fieldnotebookpageset',
        'Fieldnotebookpagesetattachment',
        'Fundingagent',
        'Geocoorddetail',
        'Geography',
        'Geographytreedef',
        'Geographytreedefitem',
        'Geologictimeperiod',
        'Geologictimeperiodtreedef',
        'Geologictimeperiodtreedefitem',
        'Gift',
        'Giftagent',
        'Giftattachment',
        'Giftpreparation',
        'Groupperson',
        'Inforequest',
        'Institution',
        'Institutionnetwork',
        'Journal',
        'Latlonpolygon',
        'Latlonpolygonpnt',
        'Lithostrat',
        'Lithostrattreedef',
        'Lithostrattreedefitem',
        'Loan',
        'Loanagent',
        'Loanattachment',
        'Loanpreparation',
        'Loanreturnpreparation',
        'Locality',
        'Localityattachment',
        'Localitycitation',
        'Localitydetail',
        'Localitynamealias',
        'Materialsample',
        'Morphbankview',
        'Otheridentifier',
        'Paleocontext',
        'Pcrperson',
        'Permit',
        'Permitattachment',
        'Picklist',
        'Picklistitem',
        'Preptype',
        'Preparation',
        'Preparationattachment',
        'Preparationattr',
        'Preparationattribute',
        'Preparationproperty',
        'Project',
        'Recordset',
        'Recordsetitem',
        'Referencework',
        'Referenceworkattachment',
        'Repositoryagreement',
        'Repositoryagreementattachment',
        'Shipment',
        'Spappresource',
        'Spappresourcedata',
        'Spappresourcedir',
        'Spauditlog',
        'Spauditlogfield',
        'Spexportschema',
        'Spexportschemaitem',
        'Spexportschemaitemmapping',
        'Spexportschemamapping',
        'Spfieldvaluedefault',
        'Splocalecontainer',
        'Splocalecontaineritem',
        'Splocaleitemstr',
        'Sppermission',
        'Spprincipal',
        'Spquery',
        'Spqueryfield',
        'Spreport',
        'Spsymbiotainstance',
        'Sptasksemaphore',
        'Spversion',
        'Spviewsetobj',
        'Spvisualquery',
        'Specifyuser',
        'Storage',
        'Storageattachment',
        'Storagetreedef',
        'Storagetreedefitem',
        'Taxon',
        'Taxonattachment',
        'Taxonattribute',
        'Taxoncitation',
        'Taxontreedef',
        'Taxontreedefitem',
        'Treatmentevent',
        'Treatmenteventattachment',
        'Voucherrelationship',
        'Workbench',
        'Workbenchdataitem',
        'Workbenchrow',
        'Workbenchrowexportedrelationship',
        'Workbenchrowimage',
        'Workbenchtemplate',
        'Workbenchtemplatemappingitem',
        'CollectionObjectType',
        'CollectionObjectGroup',
        'CollectionObjectGroupJoin'
    }
}

# def import_model(model_name):
#     try:
#         for app in apps.get_app_configs():
#             if model_name in [m.__name__ for m in app.get_models()]:
#                 return apps.get_model(app.name, model_name)
#     except AppRegistryNotReady:
#         for app_name, model_names in model_names_by_app.items():
#             if model_name in model_names:
#                 def get_model():
#                     from importlib import import_module
#                     module = import_module(f"specifyweb.{app_name}.models")
#                     return getattr(module, model_name)
#                 return get_model
#     raise ValueError(f"Model {model_name} not found in any app")

def import_model(model_name):
    for app_name, model_names in model_names_by_app.items():
        if model_name in model_names:
            def get_model():
                from importlib import import_module
                module = import_module(f"specifyweb.{app_name}.models")
                return getattr(module, model_name)
            return get_model
    raise ValueError(f"Model {model_name} not found in any app")

def get_model_by_table_id(tableid):
    model_name = model_names_by_table_id.get(tableid)
    model = import_model(model_name)
    if callable(model):
        model = model()
    return model

def models_iterator():
    for tableid, _ in model_names_by_table_id.items():
        model = get_model_by_table_id(tableid)
        yield model
