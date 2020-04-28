from django import template

register = template.Library()

@register.filter
def arrayindex(arr, idx):
    try:
        return arr[idx]
    except KeyError:
        return ''
