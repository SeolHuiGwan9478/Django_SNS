from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
# Create your views here.

class BasicView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data':data
            'message': message
        }
        return JsonResponse(result, status)
