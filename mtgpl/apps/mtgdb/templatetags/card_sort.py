from django import template

register = template.Library()


def fix_num(obj):
    if obj.number.isdecimal():
        return obj.number.zfill(4)
    else:
        return obj.number.zfill(5)


@register.filter
def numsort(value):
    return sorted(value, key=fix_num)
