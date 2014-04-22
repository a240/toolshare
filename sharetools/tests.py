from django.test import TestCase
import unittest
from sharetools.forms import *

# Create your tests here.
"""
class Tests1(TestCase):
	def test_forms(self):
		response = self.client.post("/sharetools/templates/base_login/", {'something':'something'})
		self.assertFormError(response, 'form', 'something', 'This field is required.')

class Tests2(TestCase):
	def test_forms(self):
		response = self.client.post("/sharetools/templates/base_makeShare/", {'something':'something'})
		self.assertFormError(response, 'form', 'something', 'This field is required.')

class Tests3(TestCase):
	def test_forms(self):
		response = self.client.post("/sharetools/templates/base_makeTool", {'something':'something'})
		self.assertFormError(response, 'form', 'something', 'This field is required.')

class Tests4(TestCase):
	def test_forms(self):
		response = self.client.post("/sharetools/templates/base_editProfile/", {'something':'something'})
		self.assertFormError(response, 'form', 'something', 'This field is required.')

class Tests5(TestCase):
	def test_forms(self):
		response = self.client.post("/sharetools/forms.py", {'something':'something'})
		self.assertFormError(response, 'form', 'UserEditForm', 'This field is required.')

class Tests6(TestCase):
	def test_forms(self):
		response = self.client.post("/sharetools/forms.py", {'something':'something'})
		self.assertFormError(response, 'form', 'something', 'This field is required.')

class Tests7(TestCase):
	def test_forms(self):
		response = self.client.post("/sharetools/forms.py", {'something':'something'})
		self.assertFormError(response, 'form', 'something', 'This field is required.')

class Tests8(TestCase):
	def test_forms(self):
		response = self.client.post("/sharetools/views.py", {'something':'something'})
		self.assertFormError(response, 'form', 'something', 'This field is required.')

class Tests9(TestCase):
	def test_forms(self):
		response = self.client.post("/sharetools/views.py", {'MakeToolForm':'email'})
		self.assertFormError(response, 'form', 'MakeToolForm', 'This field is required.')
"""

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
			'name': 'x' * 300,
		}

		form = MakeShareForm(data=form_data)
		self.assertFalse(form.is_valid())

class FormTests4(unittest.TestCase):
	def test_validation(self):
		form_data = {
			'loandate': 'x' * 300,
		}

		form = MakeToolForm(data=form_data)
		self.assertFalse(form.is_valid())

"""
class Tests10(unittest.TestCase):
	def setUp(self):
		self.User1 = UserForm.email
		self.User2 = UserForm.email

class Tests11(unittest.TestCase):
	def setUp(self):
		a = ['larry', 'curly', 'moe']
		self.assertEqual(UserForm(a, 0), 'larry')
		self.assertEqual(UserForm(a, 1), 'curly')
"""

#class Tests12(unittest.TestCase):
#	def setUp(self):
#