from django.test import TestCase  # , Client
# from .templatetags.urlize2 import urlize2


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
