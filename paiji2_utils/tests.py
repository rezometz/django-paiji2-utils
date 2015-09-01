from django.test import TestCase  # , Client
from htmlvalidator.client import ValidatingClient
from django.core.urlresolvers import reverse
from paiji2_utils.testmodels import TestObject as Object


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

    def test_simple_post_edition_redirection(self):

        response = self.client.get(self.edit_1_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.edit_1_url,
            {
                'name': 'first new name',
                'next': self.base_url + reverse('object-list')
            }
        )

        # success url : the last visited page (home page)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.get_path(response['Location']),
            reverse('object-list')
        )

    def test_simple_post_deletion_redirection(self):

        response = self.client.get(self.delete_1_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.delete_1_url,
            {
                'next': self.base_url + reverse('object-list')
            }
        )

        # success url : the last visited page (home page)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.get_path(response['Location']),
            reverse('object-list')
        )

    def test_invalid_next_redirection(self):

        for next_arg in (
            self.base_url + reverse('object-list') + 'unknown_address',
            self.base_url + 'arpisiueasrsui',
            'rauisreiuaesrsr/ruie',
            ' ',
            '',
        ):
            response = self.client.get(self.edit_1_url)
            self.assertEqual(response.status_code, 200)

            response = self.client.post(
                self.edit_1_url,
                {
                    'name': 'new name, next = ',
                    'next': next_arg,
                }
            )

            # success url : the home page ("next" is not valid)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                self.get_path(response['Location']),
                reverse('object-list')
            )

    def test_not_next_in_POST_redirection(self):

        response = self.client.get(self.edit_1_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.edit_1_url,
            {
                'name': 'new name, next = ',
            }
        )

        # success url : the home page (no "next" value)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.get_path(response['Location']),
            reverse('object-list')
        )

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

        response = self.client.get(
            self.edit_1_url,
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.edit_1_url,
            {
                'name': '',  # invalid form
                'next': self.base_url + self.delete_2_url
            }
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.edit_1_url,
            {
                'name': 'my best value',  # correction
                'next': self.base_url + self.edit_1_url,
            }
        )

        self.assertEqual(response.status_code, 302)
        # we don't want to be redirected to the edit form
        self.assertEqual(
            self.get_path(response['Location']),
            reverse('object-list')
        )

    def test_post_bad_creation_bad_redirection(self):

        response = self.client.get(
            reverse('object-add')
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('object-add'),
            {
                'name': '',  # invalid form
                'next': self.base_url + self.edit_1_url
            }
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('object-add'),
            {
                'name': 'my best value',  # correction
                'next': self.base_url + reverse('object-add')
            }
        )

        self.assertEqual(Object.objects.count(), 5)

        self.assertEqual(response.status_code, 302)
        # we don't want to be redirected to the creation form
        self.assertEqual(
            self.get_path(response['Location']),
            reverse('object-list')
        )
