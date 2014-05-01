from django.test import TestCase
import unittest
from sharetools.forms import *
from django.test import Client

# Create your tests here.


class Formtests(unittest.TestCase):
	def test_validation(self):
		form_data = {
			'name': 'x' * 300,
		}

		form = UserEditForm(data=form_data)
		self.assertFalse(form.is_valid())

class FormTests2(unittest.TestCase):
	def test_validation(self):
		form_data = {
			'name': 'x' * 300,
		}

		form = UserForm(data=form_data)
		self.assertFalse(form.is_valid())

class FormTests3(unittest.TestCase):
	def test_validation(self):
		form_data = {
			'loandate': datetime.datetime.today()
		}

		form = MakeShareForm(data=form_data)
		self.assertFalse(form.is_valid())

class FormTests4(unittest.TestCase):
	def test_validation(self):
		form_data = {
			'_user': 'testuser',
		}

		form = MakeToolForm(data=form_data)
		self.assertFalse(form.is_valid())

class FormTests5(unittest.TestCase):
	def test_validation(self):
		form_data = {
			'name': 'x' * 300,
		}

		form = AssetSearchForm(data=form_data)
		self.assertFalse(form.is_valid())

class FormTests6(unittest.TestCase):
	def test_validation(self):
		form_data = {
			'name': 'y',
			'description': 'z',
			'type': 'handtool',
			'location': 'testuser'
		}
"""
class FormTests7(unittest.TestCase):
	def test_validation(self):
		form_data = {
			'type': 'yard tools',
			'name': 'x' * 100,
		}

		form = AssetSearchForm(data=form_data)
		self.assertFalse(form.is_valid())
"""
class ViewTests1(unittest.TestCase):
	def test_call_view_denies_anonymous(self):
		response = self.client.get('/url/to/views/', follow=True)
		self.assertRedirects(response, '/login/')
		response = self.client.post('/url/to/views/', follow=True)
		self.assertRedirects(response, '/login/')

	def test_call_view_loads(self):
		self.client.login(username='testuser', password='testuser')
		response = self.client.get('/url/to/views/')
		self.assertEqual(response.status_code.
		self.assertTemplateUsed(response, 'conversation.html'))

	def test_call_view_fails_blank(self):
		self.client.login(username='testuser', password='testuser')
		response = self.client.post('/url/to/views/', {})
		self.assertFormError(response, 'form', 'some_field', 'This field is required.')
		response = self.client.get('/url/to/views/', {})

	def test_call_view_fails_invalid(self):
		self.client.login(username='testuser', password='testuser')
		response = self.client.post('/url/to/views/', {'invalid data'})
		self.assertFormError(response, 'form', 'some_field', 'Invalid information.')
		response = self.client.get('/url/to/views/', {'invalid data'})

	def test_call_view_fails_invalid(self):
		self.client.login(username='testuser', password='testuser')
		response = self.client.post('/url/to/views/', {'valid data'})
		self.assertFormError(response, 'form', 'some_field', 'Invalid information.')
		response = self.client.get('/url/to/views/', {'valid data'})
		self.assertRedirects(response, '/contact/1/calls/')

"""
class ViewTests2(unittestTestCase):
	def test_call_view_denies_anonymous(self):
		response = self.client.get('/url/to/')

"""
#class Tests12(unittest.TestCase):
#	def setUp(self):
#