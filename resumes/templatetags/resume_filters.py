from django import template

register = template.Library()

@register.filter
def split_technologies(value):
    return [tech.strip() for tech in value.split(',')]
