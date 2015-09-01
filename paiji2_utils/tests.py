from django.test import TestCase  # , Client
from htmlvalidator.client import ValidatingClient
from django.core.urlresolvers import reverse
from paiji2_utils.models import TestObject as Object
from django.core.urlresolvers import reverse


class TagsTest(TestCase):
    pass
    # def test_urlize2(self):
    #     text = 'ftp://wedwd'
    #     open_tag = '<a target="_blank" title="{text}"\
    #           href="{text}">'.format(text=text)
    #     close_tag = '</a>'
    #     urlized = urlize2(text)
    #     print urlized
    #     self.assertTrue(open_tag in urlized)
    #     self.assertTrue(close_tag in urlized)

    #     text = 'http://wedwd'
    #     open_tag = '<a href="%s">' % text
    #     close_tag = '</a>'
    #     urlized = urlize2(text)
    #     self.assertTrue(open_tag in urlized)
    #     self.assertTrue(close_tag in urlized)

    #     text = 'https://wedwd'
    #     open_tag = '<a href="%s">' % text
    #     close_tag = '</a>'
    #     urlized = urlize2(text)
    #     self.assertTrue(open_tag in urlized)
    #     self.assertTrue(close_tag in urlized)


class UrlTests(TestCase):

    base_url = 'http://test.testserver.test'

    def get_path(self, url):
        return '/' + '/'.join(url.split('/')[3:])

    def setUp(self):
        self.client = ValidatingClient()
        self.first_object = Object.objects.create(name='first one')
        self.second_object = Object.objects.create(name='second one')
        self.third_object = Object.objects.create(name='third one')
        self.fourth_object = Object.objects.create(name='fourth one')
        self.edit_1_url = reverse(
            'object-edit',
            args=[self.first_object.pk]
        )
        self.delete_1_url = reverse(
            'object-delete',
            args=[self.first_object.pk]
        )
        self.delete_2_url = reverse(
            'object-delete',
            args=[self.second_object.pk]
        )

    def test_access(self):
        urls = (
            reverse('object-list'),
            reverse('object-add'),
         )
        for name in ('object-edit', 'object-delete'):
            for object in Object.objects.all():
                urls += (reverse(name, args=[object.pk]),)
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_post_edition_good_redirection(self):

        response = self.client.get(self.edit_1_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.edit_1_url,
            {
                'name': 'first new name',
                'next': self.base_url + self.delete_2_url
            }
        )

        # success url : the last visited page (delete_2_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.get_path(response['Location']),
            self.delete_2_url,
        )

    def test_post_deletion_bad_redirection(self):

        response = self.client.get(self.delete_1_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.delete_1_url,
            {
                'next': self.base_url + self.edit_1_url
            }
        )

        # success url : not the last visited page (edit_1_url)
        # because this object does not exist any more,
        # but the index page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.get_path(response['Location']),
            reverse('object-list')
        )

    def test_post_bad_edition_bad_redirection(self):
        pass


