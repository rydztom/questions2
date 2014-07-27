import json

from unittest import TestCase
from django.test import Client
from django.core import management

from models import *


class ModelsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.maxDiff = None
        management.call_command('loaddata', 'fixtures.json',
                                interactive=False)

    def tearDown(self):
        management.call_command('flush', interactive=False)

    def test_login_form(self):
        rv = self.client.get("/login/")
        self.assertEquals(200, rv.status_code)
        id_username = u'<input name="username" type="username" class="form-control" placeholder="Username" required autofocus>'.encode('utf-8')
        self.assertTrue(id_username in rv.content)
        id_password = u'<input name="password" type="password" class="form-control" placeholder="Password" required>'.encode('utf-8')
        self.assertTrue(id_password in rv.content)

    def test_login(self):
        rv = self.client.get("/login/")
        post = self.client.post('/non_exist/', {'username':'restaurant1'})
        self.assertEqual(post.status_code, 404)
        post = self.client.post('/login/', {'username':'marek',
                                          'password':'qwe123'})
        self.assertEqual(post.status_code, 302)
        self.assertEqual(post['Location'], 'http://testserver/profile/')

    def test_unautorized(self):
        rv = self.client.get("/profile/")
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv['Location'],
                         'http://testserver/login/?next=/profile/')
        rv = self.client.get("/profile/")

    def test_register(self):
        post = self.client.post('/register/', {'username': "test_oppa",
                                               'email': "mail@intera.pl",
                                               'password': "qwe123"})
        self.assertEqual(post.status_code, 200)
        self.assertTrue('U can now log onto ur account' in post.content)
        
        
        rv = self.client.get("/login/")
        post = self.client.post('/login/', {'username':'test_oppa',
                                            'password': "qwe123"})
        self.assertEqual(post.status_code, 302)
        self.assertEqual(post['Location'],
                         'http://testserver/profile/')

    def test_user_profile(self):
        post = self.client.post('/login/', {'username':'marek',
                                          'password':'qwe123'})
        self.assertEqual(post.status_code, 302)
        self.assertEqual(post['Location'], 'http://testserver/profile/')
        rv = self.client.get("/profile/")
        self.assertTrue(u'<li><span><a class="test" href="user/1">FIRST TEST</a></span></li>'.encode('utf-8') in
                         rv.content)
        self.assertTrue(u'<li><span><a class="test" href="user/2">SECOND TEST</a></span></li>'.encode('utf-8') in
                         rv.content)
        self.assertTrue(u'<li><span><a class="test" href="user/3">THIRD TEST</a></span></li>'.encode('utf-8') in
                         rv.content)

    def test_user_profile_test_page(self):
        post = self.client.post('/login/', {'username':'marek',
                                          'password':'qwe123'})
        self.assertEqual(post.status_code, 302)
        self.assertEqual(post['Location'], 'http://testserver/profile/')
        rv = self.client.get("/profile/user/1/")
        self.assertTrue('FIRST QUESTION' in rv.content)
        self.assertTrue('FIRST ANSWER' in rv.content)
        self.assertTrue('SECOND ANSWER' in rv.content)
        self.assertTrue('THIRD ANSWER' in rv.content)

    def test_user_send_answers(self):
        post = self.client.post('/login/', {'username':'marek',
                                          'password':'qwe123'})
        self.assertEqual(post.status_code, 302)
        self.assertEqual(post['Location'], 'http://testserver/profile/')
        post = self.client.post("/profile/user/1/ajax_send_result/",
                                json.dumps({'result':
                                                {"1":["1"],
                                                 "2":["4"],
                                                 "3":["7"]},
                                            'send_mail': False}),
                                content_type='json')
        self.assertEquals(post.content, '{"score": 2}')