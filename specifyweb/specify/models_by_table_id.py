# from specifyweb.accounts.models import Spuserexternalid
# from specifyweb.attachment_gw.models import Spattachmentdataset
# from specifyweb.businessrules.models import UniquenessRule, UniquenessRule_Field
# from specifyweb.notifications.models import Message, Spmerging
# from specifyweb.permissions.models import UserPolicy, Role, LibraryRole, UserRole, RolePolicy, LibraryRolePolicy
# from specifyweb.workbench.models import Spdataset
# from specifyweb.specify.models import Accession, Accessionagent, Accessionattachment, Accessionauthorization, \
#     Accessioncitation, Address, Addressofrecord, Agent, Agentattachment, Agentgeography, Agentidentifier, \
#     Agentspecialty, Agentvariant, Appraisal, Attachment, Attachmentimageattribute, Attachmentmetadata, \
#     Attachmenttag, Attributedef, Author, Autonumberingscheme, Borrow, Borrowagent, Borrowattachment, \
#     Borrowmaterial, Borrowreturnmaterial, Collectingevent, Collectingeventattachment, Collectingeventattr, \
#     Collectingeventattribute, Collectingeventauthorization, Collectingtrip, Collectingtripattachment, \
#     Collectingtripattribute, Collectingtripauthorization, Collection, Collectionobject, Collectionobjectattachment, \
#     Collectionobjectattr, Collectionobjectattribute, Collectionobjectcitation, Collectionobjectproperty, \
#     Collectionreltype, Collectionrelationship, Collector, Commonnametx, Commonnametxcitation, Conservdescription, \
#     Conservdescriptionattachment, Conservevent, Conserveventattachment, Container, Dnaprimer, Dnasequence, \
#     Dnasequenceattachment, Dnasequencingrun, Dnasequencingrunattachment, Dnasequencingruncitation, Datatype,\
#     Deaccession, Deaccessionagent, Deaccessionattachment, Determination, Determinationcitation, Determiner, \
#     Discipline, Disposal, Disposalagent, Disposalattachment, Disposalpreparation, Division, Exchangein, \
#     Exchangeinattachment, Exchangeinprep, Exchangeout, Exchangeoutattachment, Exchangeoutprep, Exsiccata, \
#     Exsiccataitem, Extractor, Fieldnotebook, Fieldnotebookattachment, Fieldnotebookpage, Fieldnotebookpageattachment, \
#     Fieldnotebookpageset, Fieldnotebookpagesetattachment, Fundingagent, Geocoorddetail, Geography, Geographytreedef, \
#     Geographytreedefitem, Geologictimeperiod, Geologictimeperiodtreedef, Geologictimeperiodtreedefitem, Gift, \
#     Giftagent, Giftattachment, Giftpreparation, Groupperson, Inforequest, Institution, Institutionnetwork, Journal, \
#     Latlonpolygon, Latlonpolygonpnt, Lithostrat, Lithostrattreedef, Lithostrattreedefitem, Loan, Loanagent, \
#     Loanattachment, Loanpreparation, Loanreturnpreparation, Locality, Localityattachment, Localitycitation, \
#     Localitydetail, Localitynamealias, Materialsample, Morphbankview, Otheridentifier, Paleocontext, Pcrperson, \
#     Permit, Permitattachment, Picklist, Picklistitem, Preptype, Preparation, Preparationattachment, Preparationattr, \
#     Preparationattribute, Preparationproperty, Project, Recordset, Recordsetitem, Referencework, \
#     Referenceworkattachment, Repositoryagreement, Repositoryagreementattachment, Shipment, Spappresource, \
#     Spappresourcedata, Spappresourcedir, Spauditlog, Spauditlogfield, Spexportschema, Spexportschemaitem, \
#     Spexportschemaitemmapping, Spexportschemamapping, Spfieldvaluedefault, Splocalecontainer, Splocalecontaineritem, \
#     Splocaleitemstr, Sppermission, Spprincipal, Spquery, Spqueryfield, Spreport, Spsymbiotainstance, Sptasksemaphore, \
#     Spversion, Spviewsetobj, Spvisualquery, Specifyuser, Storage, Storageattachment, Storagetreedef, \
#     Storagetreedefitem, Taxon, Taxonattachment, Taxonattribute, Taxoncitation, Taxontreedef, Taxontreedefitem, \
#     Treatmentevent, Treatmenteventattachment, Voucherrelationship, Workbench, Workbenchdataitem, Workbenchrow, \
#     Workbenchrowexportedrelationship, Workbenchrowimage, Workbenchtemplate, Workbenchtemplatemappingitem

from django.apps import apps
from django.core.exceptions import AppRegistryNotReady

# def get_app_label(model_name):
#     try:
#         model = apps.get_model('specifyweb', model_name)
#         return model._meta.app_label
#     except LookupError:
#         return None

# def import_model(model_name):
#     model_app = get_app_label(model_name)
#     if model_app is None:
#         raise ValueError(f"Model {model_name} not found in any app")
#     return lambda: __import__(f"specifyweb.{model_app}.models").__dict__[model_name]

# def import_model(model_name):
#     for app_name, model_names in model_names_by_app.items():
#             if model_name in model_names:
#                 module = import_module(f"specifyweb.{app}.models")
#                 return getattr(module, model)

# def import_model(model_name):
#     try:
#         for app in apps.get_app_configs():
#             if model_name in [m.__name__ for m in app.get_models()]:
#                 return apps.get_model(app.name, model_name)
#     except AppRegistryNotReady:
#         for app_name, model_names in model_names_by_app.items():
#             if model_name in model_names:
#                 module = import_module(f"specifyweb.{app_name}.models")
#                 return getattr(module, model_name)
#     raise ValueError(f"Model {model_name} not found in any app")

def import_model(model_name):
    try:
        for app in apps.get_app_configs():
            if model_name in [m.__name__ for m in app.get_models()]:
                return apps.get_model(app.name, model_name)
    except AppRegistryNotReady:
        for app_name, model_names in model_names_by_app.items():
            if model_name in model_names:
                def get_model():
                    from importlib import import_module
                    module = import_module(f"specifyweb.{app_name}.models")
                    return getattr(module, model_name)
                return get_model
    raise ValueError(f"Model {model_name} not found in any app")

# def import_model(model_name):
#     model_app = None
#     for app, models in model_names_by_app.items():
#         if model_name in models:
#             model_app = app
#             break
#     if model_app is None:
#         raise ValueError(f"Model {model_name} not found in any app")
#     return lambda: __import__(f"specifyweb.{model_app}.models").__dict__[model_name]

model_names_by_app = {
    'accounts': {
        'Spuserexternalid'
    },
    'attachment_gw': {
        'Spattachmentdataset'
    },
    'businessrules': {
        'UniquenessRule',
        'UniquenessRule_Field'
    },
    'notifications': {
        'Message',
        'Spmerging'
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
        'Workbenchtemplatemappingitem'
    }
}

# This needed to be move from specify.models to it's own module to avoid circular imports
models_by_tableid = {
    7: import_model('Accession'),
    12: import_model('Accessionagent'),
    108: import_model('Accessionattachment'),
    13: import_model('Accessionauthorization'),
    159: import_model('Accessioncitation'),
    8: import_model('Address'),
    125: import_model('Addressofrecord'),
    5: import_model('Agent'),
    109: import_model('Agentattachment'),
    78: import_model('Agentgeography'),
    168: import_model('Agentidentifier'),
    86: import_model('Agentspecialty'),
    107: import_model('Agentvariant'),
    67: import_model('Appraisal'),
    41: import_model('Attachment'),
    139: import_model('Attachmentimageattribute'),
    42: import_model('Attachmentmetadata'),
    130: import_model('Attachmenttag'),
    16: import_model('Attributedef'),
    17: import_model('Author'),
    97: import_model('Autonumberingscheme'),
    18: import_model('Borrow'),
    19: import_model('Borrowagent'),
    145: import_model('Borrowattachment'),
    20: import_model('Borrowmaterial'),
    21: import_model('Borrowreturnmaterial'),
    10: import_model('Collectingevent'),
    110: import_model('Collectingeventattachment'),
    25: import_model('Collectingeventattr'),
    92: import_model('Collectingeventattribute'),
    152: import_model('Collectingeventauthorization'),
    87: import_model('Collectingtrip'),
    156: import_model('Collectingtripattachment'),
    157: import_model('Collectingtripattribute'),
    158: import_model('Collectingtripauthorization'),
    23: import_model('Collection'),
    1: import_model('Collectionobject'),
    111: import_model('Collectionobjectattachment'),
    28: import_model('Collectionobjectattr'),
    93: import_model('Collectionobjectattribute'),
    29: import_model('Collectionobjectcitation'),
    153: import_model('Collectionobjectproperty'),
    98: import_model('Collectionreltype'),
    99: import_model('Collectionrelationship'),
    30: import_model('Collector'),
    106: import_model('Commonnametx'),
    134: import_model('Commonnametxcitation'),
    103: import_model('Conservdescription'),
    112: import_model('Conservdescriptionattachment'),
    73: import_model('Conservevent'),
    113: import_model('Conserveventattachment'),
    31: import_model('Container'),
    150: import_model('Dnaprimer'),
    121: import_model('Dnasequence'),
    147: import_model('Dnasequenceattachment'),
    88: import_model('Dnasequencingrun'),
    135: import_model('Dnasequencingrunattachment'),
    105: import_model('Dnasequencingruncitation'),
    33: import_model('Datatype'),
    163: import_model('Deaccession'),
    164: import_model('Deaccessionagent'),
    165: import_model('Deaccessionattachment'),
    9: import_model('Determination'),
    38: import_model('Determinationcitation'),
    167: import_model('Determiner'),
    26: import_model('Discipline'),
    34: import_model('Disposal'),
    35: import_model('Disposalagent'),
    166: import_model('Disposalattachment'),
    36: import_model('Disposalpreparation'),
    96: import_model('Division'),
    39: import_model('Exchangein'),
    169: import_model('Exchangeinattachment'),
    140: import_model('Exchangeinprep'),
    40: import_model('Exchangeout'),
    170: import_model('Exchangeoutattachment'),
    141: import_model('Exchangeoutprep'),
    89: import_model('Exsiccata'),
    104: import_model('Exsiccataitem'),
    160: import_model('Extractor'),
    83: import_model('Fieldnotebook'),
    127: import_model('Fieldnotebookattachment'),
    85: import_model('Fieldnotebookpage'),
    129: import_model('Fieldnotebookpageattachment'),
    84: import_model('Fieldnotebookpageset'),
    128: import_model('Fieldnotebookpagesetattachment'),
    146: import_model('Fundingagent'),
    123: import_model('Geocoorddetail'),
    3: import_model('Geography'),
    44: import_model('Geographytreedef'),
    45: import_model('Geographytreedefitem'),
    46: import_model('Geologictimeperiod'),
    47: import_model('Geologictimeperiodtreedef'),
    48: import_model('Geologictimeperiodtreedefitem'),
    131: import_model('Gift'),
    133: import_model('Giftagent'),
    144: import_model('Giftattachment'),
    132: import_model('Giftpreparation'),
    49: import_model('Groupperson'),
    50: import_model('Inforequest'),
    94: import_model('Institution'),
    142: import_model('Institutionnetwork'),
    51: import_model('Journal'),
    136: import_model('Latlonpolygon'),
    137: import_model('Latlonpolygonpnt'),
    100: import_model('Lithostrat'),
    101: import_model('Lithostrattreedef'),
    102: import_model('Lithostrattreedefitem'),
    52: import_model('Loan'),
    53: import_model('Loanagent'),
    114: import_model('Loanattachment'),
    54: import_model('Loanpreparation'),
    55: import_model('Loanreturnpreparation'),
    2: import_model('Locality'),
    115: import_model('Localityattachment'),
    57: import_model('Localitycitation'),
    124: import_model('Localitydetail'),
    120: import_model('Localitynamealias'),
    151: import_model('Materialsample'),
    138: import_model('Morphbankview'),
    61: import_model('Otheridentifier'),
    32: import_model('Paleocontext'),
    161: import_model('Pcrperson'),
    6: import_model('Permit'),
    116: import_model('Permitattachment'),
    500: import_model('Picklist'),
    501: import_model('Picklistitem'),
    65: import_model('Preptype'),
    63: import_model('Preparation'),
    117: import_model('Preparationattachment'),
    64: import_model('Preparationattr'),
    91: import_model('Preparationattribute'),
    154: import_model('Preparationproperty'),
    66: import_model('Project'),
    68: import_model('Recordset'),
    502: import_model('Recordsetitem'),
    69: import_model('Referencework'),
    143: import_model('Referenceworkattachment'),
    70: import_model('Repositoryagreement'),
    118: import_model('Repositoryagreementattachment'),
    71: import_model('Shipment'),
    514: import_model('Spappresource'),
    515: import_model('Spappresourcedata'),
    516: import_model('Spappresourcedir'),
    530: import_model('Spauditlog'),
    531: import_model('Spauditlogfield'),
    524: import_model('Spexportschema'),
    525: import_model('Spexportschemaitem'),
    527: import_model('Spexportschemaitemmapping'),
    528: import_model('Spexportschemamapping'),
    520: import_model('Spfieldvaluedefault'),
    503: import_model('Splocalecontainer'),
    504: import_model('Splocalecontaineritem'),
    505: import_model('Splocaleitemstr'),
    521: import_model('Sppermission'),
    522: import_model('Spprincipal'),
    517: import_model('Spquery'),
    518: import_model('Spqueryfield'),
    519: import_model('Spreport'),
    533: import_model('Spsymbiotainstance'),
    526: import_model('Sptasksemaphore'),
    529: import_model('Spversion'),
    513: import_model('Spviewsetobj'),
    532: import_model('Spvisualquery'),
    72: import_model('Specifyuser'),
    58: import_model('Storage'),
    148: import_model('Storageattachment'),
    59: import_model('Storagetreedef'),
    60: import_model('Storagetreedefitem'),
    4: import_model('Taxon'),
    119: import_model('Taxonattachment'),
    162: import_model('Taxonattribute'),
    75: import_model('Taxoncitation'),
    76: import_model('Taxontreedef'),
    77: import_model('Taxontreedefitem'),
    122: import_model('Treatmentevent'),
    149: import_model('Treatmenteventattachment'),
    155: import_model('Voucherrelationship'),
    79: import_model('Workbench'),
    80: import_model('Workbenchdataitem'),
    90: import_model('Workbenchrow'),
    126: import_model('Workbenchrowexportedrelationship'),
    95: import_model('Workbenchrowimage'),
    81: import_model('Workbenchtemplate'),
    82: import_model('Workbenchtemplatemappingitem'),
    1000: import_model('Spuserexternalid'),
    1001: import_model('Spattachmentdataset'),
    1002: import_model('UniquenessRule'),
    1003: import_model('UniquenessRule_Field'),
    1004: import_model('Message'),
    1005: import_model('Spmerging'),
    1006: import_model('UserPolicy'),
    1007: import_model('Role'),
    1008: import_model('LibraryRole'),
    1009: import_model('UserRole'),
    1010: import_model('RolePolicy'),
    1011: import_model('LibraryRolePolicy'),
    1012: import_model('Spdataset')
}
