from django import template
register = template.Library()

@register.simple_tag
def isExhaust(boolean):
    print(boolean)
    return "It Works!"

@register.simple_tag
def calcWithProfitAndSpending(a, b):
    if a == None:
        a = 0
    if b == None:
        b = 0
    return int(a)-int(b)

