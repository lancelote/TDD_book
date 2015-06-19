"""
App views
"""

# from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    """
    Returns homepage
    """
    return HttpResponse(b'<html><title>To-Do lists</title></html>')
