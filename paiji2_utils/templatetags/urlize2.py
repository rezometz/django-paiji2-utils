import re
from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter
def urlize2(text):
    url_regex = re.compile(r'((ftp|https?)://\S*)')

    def replacement(matchobj):
        return (
            '<a target="_blank" title="{link}" href="{link}">['.format(
            link=matchobj.group(0),
        ) + _('link') + ']</a>')

    return re.sub(url_regex, replacement, text)
