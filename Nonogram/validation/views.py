from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .nonosolver import solve

@csrf_exempt
def validate(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        return JsonResponse(solve(data, True, True))
    return HttpResponseForbidden()