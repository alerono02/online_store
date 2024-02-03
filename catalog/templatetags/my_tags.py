from django import template

register = template.Library()


@register.filter()  # используется в product_detail.html
def mediapath(value):
    if value:
        return f'/media/{value}'
    else:
        return ''


@register.simple_tag()  # используется в index.html
def mediapath(value):
    if value:
        return f'/media/{value}'
    else:
        return ''


@register.filter(name='has_group')
def has_group(user, pk):
    """Проверка на наличие пользователя user в группе group_name"""
    return user.groups.filter(pk=pk).exists()
