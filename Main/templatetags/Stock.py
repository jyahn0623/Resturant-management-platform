from django import template
register = template.Library()

@register.simple_tag
def isExhaust(boolean):
    print(boolean)
    return "It Works!"
