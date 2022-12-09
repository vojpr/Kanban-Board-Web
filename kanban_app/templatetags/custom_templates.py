from django import template
register = template.Library()


@register.filter
def prev_index(query_set, x):
    list_query_set = list(query_set)
    if list_query_set.index(x) == 0:
        return 0
    else:
        task = list_query_set[list_query_set.index(x)-1]
        return task.pk


@register.filter
def index(query_set, x):
    list_query_set = list(query_set)
    return list_query_set[x]
