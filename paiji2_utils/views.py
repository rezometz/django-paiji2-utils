# -*- encoding: utf-8 -*-
from django.core.urlresolvers import (
    reverse, resolve, Resolver404, NoReverseMatch
)
from django.contrib import messages


class SuccessUrlMixin(object):
    """ A create/update/delete view that manages a
    form which sends {{ request.META.HTTP_REFERER }} as
    the POST "next" value, must inherit from
    this class before the "generic.{Create/Update...}View"
    in order to forbid a redirection to a list of chosen
    urls. A default url will be used if necessary.
    """

    default_url_name = 'home'

    forbidden_url_names = tuple()

    forbidden_urls = tuple()

    def get_forbidden_url_names(self):
        return self.forbidden_url_names

    def get_forbidden_urls(self):
        return self.forbidden_urls

    def get_default_url(self):
        return reverse(self.default_url_name)

    def get_success_url(self):

        if hasattr(self, 'message_success'):
            messages.success(self.request, self.message_success)

        # the next POST value must be
        # "{{ request.META.HTTP_REFERER }}"
        try:
            HTTP_REFERER = self.request.POST['next']
            # we delete the « http://www.website.domain/ » part
            path = '/' + '/'.join(
                HTTP_REFERER.split('/')[3:]
            )
            # we keep the «/en/myapp/action/pk/» part
            match = resolve(path)
        except (KeyError, Resolver404, NoReverseMatch):
            return self.get_default_url()

        if (
            match.url_name not in (
                self.get_forbidden_url_names() or tuple()
            ) and
            path not in (
                self.get_forbidden_urls() or tuple()
            )
        ):
            return path
        else:
            return self.get_default_url()
