import re
from django import template


register = template.Library()


@register.filter
def urlize2(text):
    url_regex = re.compile(r'((ftp|https?)://\S*)')

    def replacement(matchobj):
        return ('<a href="{link}">[link]</a>').format(
            link=matchobj.group(0),
        )

    return re.sub(url_regex, replacement, text)
