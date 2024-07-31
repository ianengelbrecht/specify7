from typing import Tuple, List
from django.db.models import Q, Count, Model
import specifyweb.specify.models as spmodels

lookup = lambda tree: (tree.lower() + 'def')

def get_search_filters(collection: spmodels.Collection, tree: str):
    tree_name = tree.lower()
    if tree_name == 'storage':
        return Q(institution=collection.discipline.division.institution)
    discipline_query = Q(discipline=collection.discipline)
    if tree_name == 'taxon':
        discipline_query |= Q(
            # TEST: should this only be added if discipline is null?
            cotypes__collection=collection
            )
    tree_at_discipline = getattr(collection.discipline, lookup(tree))
    if tree_at_discipline:
        discipline_query |= Q(id=tree_at_discipline.id)
    return discipline_query

def get_treedef(collection: spmodels.Collection, tree_name: str) ->  List[Tuple[int, int, int]]:
    # Get the appropriate TreeDef based on the Collection and tree_name

    # Mimic the old behavior of limiting the query to the first item for trees other than taxon.
    # Even though the queryconstruct can handle trees with multiple types.
    _limit = lambda query: (query if tree_name.lower() == 'taxon' else query[:1])
    search_filters = get_search_filters(collection, tree_name)

    lookup_tree = lookup(tree_name)
    tree_model: Model = getattr(spmodels, lookup_tree)

    # Get all the treedefids, and the count of item in each, corresponding to our search predicates
    search_query = _limit(
        tree_model.objects.filter(search_filters)
        .annotate(item_counts=Count("treedefitems", distinct=True))
        .distinct()
        .values_list("id", "item_counts")
    )

    result = list(search_query)

    assert len(result) > 0, "No definition to query on"

    return result

def get_taxon_treedef(collection: spmodels.Collection, collection_object_type: spmodels.CollectionObjectType = None):
    # Use the provided collection_object_type if not None
    if collection_object_type and collection_object_type.taxontreedef:
        return collection_object_type.taxontreedef

    # Use the collection's default collectionobjecttype if it exists
    if collection.collectionobjecttype and collection.collectionobjecttype.taxontreedef:
        return collection.collectionobjecttype.taxontreedef

    # Otherwise, try to get the first CollectionObjectType related to the collection
    cot = spmodels.CollectionObjectType.objects.filter(collection=collection).first()
    if cot:
        return cot.taxontreedef

    # Fallback to the old method of discipline's taxontreedef if no CollectionObjectType is found
    if collection.discipline.taxontreedef:
        return collection.discipline.taxontreedef

    # If all else fails crash
    raise Exception("Couldn't find a corresponding treedef")

def get_taxon_treedefs(collection: spmodels.Collection):
    return spmodels.Taxontreedef.objects.filter(discipline=collection.discipline).values_list('id', flat=True)

def get_all_taxon_treedefs():
    # Get all TaxonTreedefs
    return spmodels.Taxontreedef.objects.all()

def get_all_taxon_treedef_ids() -> Tuple[int]:
    # Get all TaxonTreedef IDs
    return tuple(spmodels.Taxontreedef.objects.values_list("id", flat=True))
