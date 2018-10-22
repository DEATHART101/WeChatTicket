from django.test import TestCase
from wechat.models import Activity
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
# Create your tests here.
from django.test.client import Client
from django.utils import timezone

# Create your tests here.


# WeChat测试
class WeChatGetTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='root', email='xz1526003@163.com', password='xqws2018')

    # get请求
    def test_login_get(self):
        response = self.client.get('/api/a/login')
        self.assertEqual(response.json()['code'], 0)

