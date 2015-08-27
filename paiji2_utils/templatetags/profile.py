from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def profile_url(user):
    try:
        return settings.PROFILE_URL(user)
    except:
        return ''

@register.inclusion_tag('utils/mail_link.html')
def mail_link(user, text, subject):
    return {
        'user': user,
        'text': text,
        'subject': subject,
    }

@register.inclusion_tag('utils/profile_link.html')
def profile_link(user):
    return {
        'user': user,
    }
