from specifyweb.stored_queries.query_ops import QueryOps

from .related import RelatedSearch, F

class CollObjToDeterminer(RelatedSearch):
    id = 1
    definitions = [
        'Collectionobject.determinations.determiner',
        'Collectionobject.determinations',
        'Collectionobject.determinations.taxon',
        'Collectionobject'
        ]
    distinct = True
    filters = [['determinations.iscurrent', QueryOps.op_true, None]]
    columns = [
        'determinations.taxon.fullname',
        'determinations.taxon.commonname',
        'determinations.determiner.lastname',
        'determinations.determiner.firstname',
        'determinations.determiner.agenttype',
        ]

class CollObToLocality(RelatedSearch):
    id = 2
    definitions = [
        'Collectingevent.locality',
        'Collectingevent'
        ]
    columns = [
        'locality.localityname',
        'startdate',
        'enddate',
        'locality.latitude1',
        'locality.longitude1',
        ]

class CollObject(RelatedSearch):
    id = 3
    definitions = [
        'Collectionobject.determinations.taxon',
        'Collectionobject'
        ]
    distinct = True
    columns = [
        'catalognumber',
        'catalogeddate',
        'determinations.taxon.fullname',
        ]

class GeoToTaxon(RelatedSearch):
    id = 4
    definitions = [
        'Collectionobject.determinations.taxon',
        'Collectionobject.collectingevent.locality.geography'
        ]
    distinct = True
    filters = [['determinations.iscurrent', QueryOps.op_true, None]]
    columns = [
        'determinations.taxon.fullname',
        'collectingevent.locality.geography.fullname',
        ]

class ColObjCollectors(RelatedSearch):
    id = 5
    definitions = [
        'Collectionobject.collectingevent.collectors.agent',
        'collectionobject.collectingevent',
        'Collectionobject'
        ]
    distinct = True
    columns = [
        'catalognumber',
        'catalogeddate',
        'collectingevent.startdate',
        'collectingevent.collectors.agent.lastname',
        ]

class AcceptedTaxon(RelatedSearch):
    id = 6
    definitions = [
        'Taxon.acceptedtaxon',
        'Taxon'
        ]
    columns = [
        'fullname',
        'acceptedtaxon.fullname',
        ]

class SynonymCollObjs(RelatedSearch):
    id = 7
    definitions = [
        'Collectionobject.determinations.taxon',
        'Collectionobject.determinations.preferredtaxon',
        'Collectionobject'
        ]
    distinct = True
    excludes = [['determinations.taxon.taxonid', QueryOps.op_equals, F('determinations.preferredtaxon.taxonid')]]
    columns = [
        'catalognumber',
        'determinations.taxon.fullname',
        'determinations.preferredtaxon.fullname',
        ]

class OtherSynsCollObjs(RelatedSearch):
    id = 9
    definitions = [
        'Collectionobject.determinations.preferredtaxon.acceptedchildren',
        'Collectionobject.determinations.preferredtaxon',
        'Collectionobject.determinations.taxon',
        'Collectionobject'
        ]
    distinct = True
    excludes = [['determinations.preferredtaxon.acceptedchildren.taxonid', QueryOps.op_equals, F('determinations.preferredtaxon.taxonid')]]
    columns = [
        'catalognumber',
        'determinations.taxon.fullname',
        'determinations.preferredtaxon.fullname',
        'determinations.preferredtaxon.acceptedchildren.fullname',
        ]

class CurrCollObject(RelatedSearch):
    id = 10
    definitions = [
        'Collectionobject.determinations.taxon',
        'Collectionobject'
        ]
    distinct = True
    filters = [['determinations.iscurrent', QueryOps.op_true, None]]
    columns = [
        'catalognumber',
        'catalogeddate',
        'determinations.taxon.fullname',
        ]

class AgentFromAgentVariant(RelatedSearch):
    id = 11
    definitions = [
        'Agentvariant.agent',
        'Agentvariant'
        ]
    columns = [
        'name',
        'agent.lastname',
        'agent.firstname',
        ]

class LocalityAlias(RelatedSearch):
    id = 12
    definitions = [
        'Locality.localitynamealiass',
        'Locality'
        ]
    excludes = [['localitynamealiass.localitynamealiasid', QueryOps.op_empty, None]]
    columns = [
        'localityname',
        'localitynamealiass.name'
        ]

class CEToCO(RelatedSearch):
    id = 13
    definitions = [
        'Collectingevent.collectionobjects',
        'Collectingevent'
        ]
    columns = [
        'collectionobjects.catalognumber',
        'startdate',
        'enddate',
        ]

class LocToCO(RelatedSearch):
    id = 29
    definitions = [
        'Locality.collectingevents.collectionobjects',
        'Locality.collectingevents',
        'Locality'
        ]
    columns = [
        'collectingevents.collectionobjects.catalognumber',
        'collectingevents.startdate',
        'localityname',
        'latitude1',
        'longitude1',
        ]

class AccessionToCo(RelatedSearch):
    id = 31
    definitions = [
        'Accession.collectionobjects',
        'Accession'
        ]
    distinct = True
    filters = [['collectionobjects.determinations.iscurrent', QueryOps.op_true, None]]
    columns = [
        'collectionobjects.catalognumber',
        'collectionobjects.determinations.taxon.fullname',
        'accessionnumber',
        ]

class AccessionToAgent(RelatedSearch):
    id = 32
    definitions = [
        'Accession.accessionagents.agent',
        'Accession'
        ]
    columns = [
        'accessionagents.agent.lastname',
        'accessionagents.agent.firstname',
        'accessionagents.role',
        'accessionnumber',
        ]

class BorrowToAgent(RelatedSearch):
    id = 33
    definitions = [
        'Borrow.borrowagents.agent',
        'Borrow'
        ]
    columns = [
        'invoicenumber',
        'borrowagents.agent.lastname',
        'borrowagents.agent.firstname',
        'borrowagents.role',
        ]

class AppraisalToAgent(RelatedSearch):
    id = 34
    definitions = [
        'Appraisal.agent',
        'Appraisal'
        ]
    columns = [
        'appraisalnumber',
        'agent.lastname',
        'agent.firstname',
        ]

class GeoTimePeriodToCO(RelatedSearch):
    id = 35
    definitions = [
        'Geologictimeperiod.chronosstratspaleocontext.collectionobjects',
        'Geologictimeperiod'
        ]
    columns = [
        'fullname',
        'chronosstratspaleocontext.collectionobjects.catalognumber'
        ]

class CollEventToCollectors(RelatedSearch):
    id = 36
    definitions = [
        'Collectingevent.collectors.agent',
        'Collectingevent'
        ]
    columns = [
        'collectors.agent.lastname',
        'collectors.agent.firstname',
        'startdate',
        'stationfieldnumber'
        ]

# class CollTripCollEvent(RelatedSearch):
#     id = 37
#     definitions = [
# 'Collectingevent.collectingtrip',
# 'Collectingtrip'
# ]
#     columns = [
#         'stationfieldnumber',
#         'collectingtrip.collectingtripname',
#         'startdate'
#         ]

class AgentExchangeIn(RelatedSearch):
    id = 38
    definitions = [
        'Exchangein.agentreceivedfrom',
        'Exchangein'
        ]
    columns = [
        'exchangedate',
        'descriptionofmaterial',
        'agentreceivedfrom.abbreviation'
        ]

class AgentExchangeOut(RelatedSearch):
    id = 39
    definitions = [
        'Exchangeout.agentsentto',
        'Exchangeout'
        ]
    columns = [
        'exchangedate',
        'descriptionofmaterial',
        'agentsentto.abbreviation'
        ]

class GeographyCE(RelatedSearch):
    id = 40
    definitions = [
        'Geography.localities.collectingevents',
        'Geography'
        ]
    columns = [
        'localities.collectingevents.startdate',
        'localities.collectingevents.stationfieldnumber',
        'fullname'
        ]

class GeographyCO(RelatedSearch):
    id = 41
    definitions = [
        'Geography.localities.collectingevents.collectionobjects',
        'Geography'
        ]
    columns = [
        'localities.collectingevents.collectionobjects.catalognumber',
        'fullname'
        ]

class GiftCO(RelatedSearch):
    id = 42
    definitions = [
        'Gift.giftpreparations.preparation.collectionobject',
        'Gift'
        ]
    columns = [
        'giftpreparations.preparation.collectionobject.catalognumber',
        'giftpreparations.preparation.preptype.name',
        'giftnumber'
        ]

class GiftAgent(RelatedSearch):
    id = 43
    definitions = [
        'Gift.giftagents.agent',
        'Gift'
        ]
    columns = [
        'giftagents.agent.lastname',
        'giftagents.agent.firstname',
        'giftagents.role',
        'giftnumber'
        ]

class LoanCO(RelatedSearch):
    id = 44
    definitions = [
        'Loan.loanpreparations.preparation.collectionobject',
        'Loan'
        ]
    columns = [
        'loanpreparations.preparation.collectionobject.catalognumber',
        'loanpreparations.preparation.preptype.name',
        'loannumber'
        ]

class LoanAgent(RelatedSearch):
    id = 45
    definitions = [
        'Loan.loanagents.agent',
        'Loan'
        ]
    columns = [
        'loanagents.agent.lastname',
        'loanagents.agent.firstname',
        'loanagents.role',
        'loannumber'
        ]

class LithoStratToCO(RelatedSearch):
    id = 46
    definitions = [
        'Lithostrat.paleocontexts.collectionobjects',
        'Lithostrat'
        ]
    columns = [
        'paleocontexts.collectionobjects.catalognumber',
        'fullname'
        ]

class PermitToCO(RelatedSearch):
    id = 47
    definitions = [
        'Permit.accessionauthorizations.accession.collectionobjects',
        'Permit'
        ]
    columns = [
        'accessionauthorizations.accession.collectionobjects.catalognumber',
        'permitnumber'
        ]

class PermitIssuedToAgent(RelatedSearch):
    id = 48
    definitions = [
        'Permit.issuedto'
        ]
    columns = [
        'issuedto.lastname',
        'issuedto.firstname',
        'permitnumber'
        ]

class PermitIssuedByAgent(RelatedSearch):
    id = 49
    definitions = [
        'Permit.issuedby',
        'Permit'
        ]
    columns = [
        'issuedby.lastname',
        'issuedby.firstname',
        'permitnumber'
        ]

# class ProjectCO(RelatedSearch):
#     id = 50
#     definitions = [
# 'Project.collectionobjects',
# 'Project'
# ]
#     columns = [
#         'collectionobjects.catalognumber',
#         'projectname',
#         'projectnumber'
#         ]

class ProjectAgent(RelatedSearch):
    id = 51
    definitions = [
        'Project.agent',
        'Project'
        ]
    columns = [
        'agent.lastname',
        'agent.firstname',
        'projectname',
        'projectnumber'
        ]

class RepoAgreeAgent(RelatedSearch):
    id = 52
    definitions = [
        'Repositoryagreement.originator',
        'Repositoryagreement'
        ]
    columns = [
        'originator.lastname',
        'originator.firstname',
        'repositoryagreementnumber'
        ]

class StorageCO(RelatedSearch):
    id = 53
    definitions = [
        'Storage.preparations.collectionobject',
        'Storage'
        ]
    columns = [
        'preparations.collectionobject.catalognumber',
        'name',
        'fullname'
        ]

class TaxCollObject(RelatedSearch):
    id = 54
    distinct = True
    definitions = [
        'Collectionobject.determinations.taxon'
        ]
    columns = [
        'catalognumber',
        'catalogeddate',
        'determinations.iscurrent',
        'determinations.taxon.fullname'
        ]

# class ColObjToContainer(RelatedSearch):
#     id = 55
#     definitions = [
# 'Collectionobject.container'
# ]
#     columns = [
#         'container.type',
#         'container.name',
#         'catalognumber'
#         ]

# class ContainerToKids(RelatedSearch):
#     id = 56
#     definitions = [
# "Collectionobject.container"
# ]
#     columns = [
#         'catalognumber',
#         'catalogeddate',
#         'container.name'
#         ]

# class ContainerToContainerKids(RelatedSearch):
#     id = 57
#     definitions = [
#          "Container.children"
#         ]
#     columns = [
#         'name',
#         'children.name'
#         ]

class ExchangeInCO(RelatedSearch):
    id = 58
    definitions = [
        'Exchangein.exchangeinpreps.preparation.collectionobject',
        'Exchangein'
        ]
    columns = [
        'exchangeinpreps.preparation.collectionobject.catalognumber',
        'exchangeinpreps.preparation.preptype.name',
        'exchangedate'
        ]

class ExchangeOutCO(RelatedSearch):
    id = 59
    definitions = [
        'Exchangeout.exchangeoutpreps.preparation.collectionobject',
        'Exchangeout'
        ]
    columns = [
        'exchangeoutpreps.preparation.collectionobject.catalognumber',
        'exchangeoutpreps.preparation.preptype.name',
        'exchangedate'
        ]

__all__ = [cls.__name__ for cls in globals().values()
           if isinstance(cls, type) and
           issubclass(cls, RelatedSearch) and
           not cls is RelatedSearch]
