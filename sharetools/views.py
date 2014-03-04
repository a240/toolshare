from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
	return HttpResponse("Hello World, your at the share index.")

def shed(request, id):
	return HttpResponse("Shed page.  Shed id:" + id)

def tool(request, id):
	return HttpResponse("Tool page." + id)