from django.views.decorators.http import require_GET
from django.http import HttpResponse, Http404
from django.db import connection

from .views import login_required
from .api import get_object_or_404, obj_to_data, toJson

from . import tree_sqls

@login_required
@require_GET
def tree_view(request, tree, parentid):
    try:
        sql = getattr(tree_sqls, tree)
    except AttributeError as e:
        raise Http404(e)

    colmemid = request.specify_collection.id
    cursor = connection.cursor()
    cursor.execute(sql, [colmemid, colmemid, parentid])

    return HttpResponse(toJson(cursor.fetchall()), content_type='application/json')

@login_required
@require_GET
def path(request, model, id):
    id = int(id)
    tree_node = get_object_or_404(model, id=id)

    data = {node.definitionitem.name: obj_to_data(node)
            for node in get_tree_path(tree_node)}

    data['resource_uri'] = '/api/specify_tree/%s/%d/path/' % (model, id)

    return HttpResponse(toJson(data), content_type='application/json')

def get_tree_path(tree_node):
    while tree_node is not None:
        yield tree_node
        tree_node = tree_node.parent
