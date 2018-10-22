from django.test import TestCase
from django.contrib.auth.models import User
from adminpage.views import *
from django.test.client import Client
# Create your tests here.


#   UserPage单元测试
class UserBindTest(TestCase):
    # 验证
    def setUp(self):
        User.objects.create(open_id='0000', student_id='2016080000')

    # get请求
    def test_bind_get(self):
        student = User.objects.get(open_id='student')
        response = self.client.get('/api/u/user/bind', {'openid': student.open_id})
        self.assertEqual(response.json()['data'], '2016080000')

    def test_no_bind_get(self):
        response = self.client.get('/api/u/user/bind', {'openid': ''})
        self.assertEqual(response.json()['data'], '')

    # post请求
    def test_ok_bind_post(self):
        response = self.client.post('/api/u/user/bind', {'openid': 'bind', 'student_id': '2016080000', 'password': '1'})
        self.assertEqual(response.json()['code'], 0)

    def test_no_bind_post(self):
        response = self.client.post('/api/u/user/bind', {'openid': 'no_bind'})
        self.assertEqual(response.json()['code'], 1)

    def test_nopassword_bind_post(self):
        response = self.client.post('/api/u/user/bind', {'openid': 'nopassword_bind', 'student_id': '2016080000'})
        self.assertEqual(response.json()['code'], 1)

    def test_no_student_id_bind_post(self):
        response = self.client.post('/api/u/user/bind', {'openid': 'no_student_id_bind', 'password': '1111'})
        self.assertEqual(response.json()['code'], 1)
