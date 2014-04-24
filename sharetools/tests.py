from django.test import TestCase
import unittest
from sharetools.forms import *

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
			'user': 'testuser',
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

#class FormTests6(unittest.TestCase):
#	def test_validation(self):
#		form_data = {
#			''
#		}


#class Tests12(unittest.TestCase):
#	def setUp(self):
#