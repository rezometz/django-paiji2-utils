from django.conf.urls import url  # , patterns
from paiji2_utils import testviews

urlpatterns = [
    url(
        r'^$',
        testviews.ObjectListView.as_view(),
        name="object-list",
    ),
    url(
        r'^add$',
        testviews.ObjectCreateView.as_view(),
        name="object-add",
    ),
    url(
        r'^edit/(?P<pk>[0-9]+)/$',
        testviews.ObjectEditView.as_view(),
        name="object-edit",
    ),
    url(
        r'^delete/(?P<pk>[0-9]+)/$',
        testviews.ObjectDeleteView.as_view(),
        name="object-delete",
    ),
]
