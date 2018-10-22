from django.test import TestCase

# Create your tests here.
from django.test.client import Client
from django.utils import unittest
from django.utils import timezone
from django.contrib.auth.models import User
from wechat.models import *
from adminpage.views import *
import datetime
# Create your tests here.

# AdminPage单元测试
# login测试
ActivityDel = Activity(name='act_del', key ='delete', description='deleted activity', start_time=datetime.datetime(
    2018, 3, 1, 1, 20, 30, 10, tzinfo=timezone.utc), end_time=datetime.datetime(2018, 3, 2, 30, 30, 10, tzinfo=timezone.utc),
    place='place1', book_start=datetime.datetime(2018, 2, 1, 20, 30, 10,tzinfo=timezone.utc),
   book_end=datetime.datetime(2018, 2, 2, 20, 30, 10, tzinfo=timezone.utc), total_tickets=5000, status=0)

class LoginGetTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='root', email='xz1526003@163.com', password='xqws2018')

    # get请求
    def test_login_get(self):
        response = self.client.get('/api/a/login')
        self.assertEqual(response.json()['code'], 0)

class LoginPostTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='root', email='xz1526003@163.com', password='xqws2018')

    # post请求，用户名和密码多种测试用例
    def test_login_post(self):
        response = self.client.post('/api/a/login', {'username': 'root', 'password': 'xqws2018'})
        self.assertEqual(response.json()['code'], 0)

    def test_user1(self):
        response = self.client.post('/api/a/login', {'username': '', 'password': '2018'})
        self.assertEqual(response.json()['code'], 1)

    def test_user2(self):
        response = self.client.post('/api/a/login', {'username': 'root', 'password': ''})
        self.assertEqual(response.json()['code'], 1)

    def test_user3(self):
        response = self.client.post('/api/a/login', {'username': '', 'password': ''})
        self.assertEqual(response.json()['code'], 1)

    def test_user4(self):
        response = self.client.post('/api/a/login', {'username': 'root00', 'password': 'xqws2018'})
        self.assertEqual(response.json()['code'], 1)

    def test_user5(self):
        response = self.client.post('/api/a/login', {'username': 'root', 'password': '2018'})
        self.assertEqual(response.json()['code'], 1)

    def test_user6(self):
        response = self.client.post('/api/a/login', {'username': 'root11', 'password': 'x2018'})
        self.assertEqual(response.json()['code'], 1)


# logout测试
class LogoutTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='root', email='xz1526003@163.com', password='xqws2018')

    # post 请求（有登陆）
    def test_with_login_post(self):
        response = self.client.get('/api/a/login', {'username': 'root', 'password': 'xqws2018'})
        self.assertEqual(response.json()['code'], 0)

    # post请求（无登陆）
    def test_without_login_post(self):
        response = self.client.post('/api/a/login')
        self.assertEqual(response.json()['code'], 1)

# activity测试
class ActivityListTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='root', email='xz1526003@163.com', password='xqws2018')

    def test_list_get(self):
        self.client.post('/api/a/login', {'username': 'root', 'password': 'xqws2018'})
        response = self.client.get('/api/a/activity/list')
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], 1)

class ActivityCreateTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='root', email='xz1526003@163.com', password='xqws2018')

    def test_create_act_post(self):
        self.client.post('/api/a/login', {'username': 'root', 'password': 'xqws2018'})
        response = self.client.get('/api/a/activity/create', {'name': 'CreateAct', 'key': 'ca', 'place': 'place2',
        'description': 'create a activity', 'picUrl': '', 'startTime': '2018-2-2:00:00:00',
        'endTime': '2018-2-3:00:00:00', 'bookStart': '2018-1-2:00:00:00', 'bookEnd': '2018-1-3:00:00:00',
        'totalTickets': '5000', 'status': 0})
        self.assertEqual(response.json()['code'], 0)

class ActivityDeleteTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='root', email='xz1526003@163.com', password='xqws2018')

    def test_delete_post(self):
        self.client.post('/api/a/login', {'username': 'root', 'password': 'xqws2018'})
        response = self.client.get('/api/a/activity/delete', {'id': ActivityDel.id})
        self.assertEqual(response.json()['code'], 0)