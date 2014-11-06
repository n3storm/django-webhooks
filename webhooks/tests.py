try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse

from django.test import Client, TestCase, RequestFactory
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from model_mommy import mommy

from .views import WebHookView
from .models import WebHook


class WebHookFilterTest(TestCase):

    def filter(self, payload, regex):
        ab = mommy.make_recipe('webhooks.web_hook')
        ab.filter = regex
        ab.action = 'R'
        ab.method = 'P'
        ab.save()
        return ab.match_filter(payload)

    def test_gh_true(self):
        payload = '{ "ref": "refs/heads/master" }'
        regex = '\"ref\":\s*\"refs/heads/master\"'
        self.assertTrue(self.filter(payload, regex))

    def test_gh_false(self):
        payload = '{ "ref": "refs/heads/master" }'
        regex = '\"ref\":\s*\"refs/heads/development\"'
        self.assertFalse(self.filter(payload, regex))

    def test_bb_true(self):
        payload = '{ "branch": "master" }'
        regex = '\"branch\":\s*\"master\"'
        self.assertTrue(self.filter(payload, regex))

    def test_bb_false(self):
        payload = '{ "branch": "master" }'
        regex = '\"branch\":\s*\"development\"'
        self.assertFalse(self.filter(payload, regex))

    def test_bb_actual(self):
        payload = 'payload=%7B%22repository%22%3A+%7B%22website%22%3A+%22%22%2C+%22fork%22%3A+false%2C+%22name%22%3A+%22ams%22%2C+%22scm%22%3A+%22git%22%2C+%22owner%22%3A+%22adlibre%22%2C+%22absolute_url%22%3A+%22%2Fadlibre%2Fams%2F%22%2C+%22slug%22%3A+%22ams%22%2C+%22is_private%22%3A+true%7D%2C+%22truncated%22%3A+false%2C+%22commits%22%3A+%5B%7B%22node%22%3A+%2257568e1fc9be%22%2C+%22files%22%3A+%5B%7B%22type%22%3A+%22modified%22%2C+%22file%22%3A+%22requirements.txt%22%7D%5D%2C+%22raw_author%22%3A+%22Andrew+Cutler+%3Cmacropin%40gmail.com%3E%22%2C+%22utctimestamp%22%3A+%222014-08-19+02%3A25%3A39%2B00%3A00%22%2C+%22author%22%3A+%22macropin%22%2C+%22timestamp%22%3A+%222014-08-19+04%3A25%3A39%22%2C+%22raw_node%22%3A+%2257568e1fc9beb8c15e15428109cf34ceba82f19b%22%2C+%22parents%22%3A+%5B%225ec8b933954d%22%5D%2C+%22branch%22%3A+%22master%22%2C+%22message%22%3A+%22Bump+gunicorn+19.1.1%5Cn%22%2C+%22revision%22%3A+null%2C+%22size%22%3A+-1%7D%5D%2C+%22canon_url%22%3A+%22https%3A%2F%2Fbitbucket.org%22%2C+%22user%22%3A+%22macropin%22%7D'
        regex = '\"branch\":\s*\"master\"'
        payload = str(urlparse.parse_qs(payload))
        self.assertTrue(self.filter(payload, regex))


class WebHookViewTest(TestCase):

    def setUp(self):
        # API User
        self.user = mommy.make_recipe('webhooks.user')
        self.user.super_user = True
        self.factory = RequestFactory()

    def test_gh_action(self):

        payload = '{ "ref": "refs/heads/master" }'
        regex = 'refs/heads/master'

        web_hook = mommy.make_recipe('webhooks.web_hook')
        web_hook.filter = regex
        web_hook.action = 'R'
        web_hook.method = 'P'
        # Assign webhhook to user object (need to point it somewhere)
        web_hook.object_id = self.user.pk
        web_hook.content_type = ContentType.objects.get_for_model(User)
        web_hook.save()

        url = web_hook.get_absolute_url()
        self.assertEqual(url, reverse_lazy('web-hook', kwargs={'pk': web_hook.pk}))

        data = dict()
        data['payload'] = payload

        request = self.factory.post(url, data=data)
        request.user = self.user

        # Actual request
        view = WebHookView.as_view()
        response = view(request, pk=web_hook.pk)
        self.assertEqual(response.status_code, 200)

        # reload from DB
        web_hook = WebHook.objects.get(pk=web_hook.pk)
        self.assertNotEqual(web_hook.triggered, None)  # check triggered updated

    def test_bb_action(self):

        payload = '{ "branch": "master" }'
        regex = '\"branch\":\s*\"master\"'

        web_hook = mommy.make_recipe('webhooks.web_hook')
        web_hook.filter = regex
        web_hook.action = 'R'
        web_hook.method = 'P'
        # Assign webhhook to user object (need to point it somewhere)
        web_hook.object_id = self.user.pk
        web_hook.content_type = ContentType.objects.get_for_model(User)
        web_hook.save()
        url = web_hook.get_absolute_url()
        self.assertEqual(url, reverse_lazy('web-hook', kwargs={'pk': web_hook.pk}))

        data = dict()
        data['payload'] = payload

        request = self.factory.post(url, data=data, content_type='application/x-www-form-urlencoded')
        request.user = self.user

        # Actual request
        view = WebHookView.as_view()
        response = view(request, pk=web_hook.pk)
        self.assertEqual(response.status_code, 200)

        # reload from DB
        web_hook = WebHook.objects.get(pk=web_hook.pk)
        self.assertNotEqual(web_hook.triggered, None)  # check triggered updated