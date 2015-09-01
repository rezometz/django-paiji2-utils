from paiji2_utils.views import SuccessUrlMixin
from django.views import generic
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from .testmodels import TestObject as Object


class MySuccessUrl(SuccessUrlMixin):

    default_url_name = 'object-list'

    def get_forbidden_urls(self):
        if hasattr(self, 'object'):
            return (
                reverse('object-edit', args=[self.object.pk]),
                reverse('object-delete', args=[self.object.pk]),
            )
        else:
            return None


class ObjectListView(generic.ListView):
    model = Object
    context_object_name = 'objects'
    template_name = 'test/object/list.html'


class ObjectCreateView(MySuccessUrl, generic.CreateView):
    model = Object
    fields = ('name', )
    template_name = 'test/object/form.html'
    message_success = _("success !")
    forbidden_url_names = (
        'object-add',
    )


class ObjectEditView(MySuccessUrl, generic.UpdateView):
    model = Object
    fields = ('name', )
    template_name = 'test/object/form.html'
    message_success = _("success !")


class ObjectDeleteView(MySuccessUrl, generic.DeleteView):
    model = Object
    template_name = 'test/object/confirm_delete.html'
    message_success = _("success !")
