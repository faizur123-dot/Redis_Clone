from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from . import utils

class SetGetData(View):
    
    def post(self, request):
        command = request.POST['command']
        key = request.POST['key']
        value = request.POST['value']
        if command == 'SET' and key and value:
            utils.add_key_value(key=key, value=value)
        else:
            HttpResponse("Error")
        return HttpResponse("OK")
    
    def get(self, request):
        command = request.GET.get('command')
        key = request.GET.get('key')
        value = 'nil'
        if command == 'GET' and key:
            value = utils.get_value_for_key(key=key)
        else:
            return HttpResponse('Error')
        return HttpResponse(value)

    
def set_expire(request):
    if request.method== 'POST':
        command = request.POST['command']
        key = request.POST['key']
        timeout = int(request.POST['timeout'])
        if command == 'EXPIRE' and key and timeout:
            utils.set_expiry_time(key=key, timeout=timeout)
        else:
            HttpResponse('Error')
        return HttpResponse('OK')


def add_zdata(request):
    if request.method == 'POST':
        command = request.POST['command']
        key = request.POST['key']
        value = request.POST['value']
        if command == 'ZADD' and key and value:
            values_list = value.split(' ')
            if len(values_list) % 2==0:
                count = utils.store_zdata(key=key, data=values_list)
            else:
                return HttpResponse("Error")
        else:
            HttpResponse("Error")
        return HttpResponse(count)

def get_zrank(request):
    if request.method == 'GET':
        command = request.GET.get('command')
        key = request.GET.get('key')
        value = request.GET.get('value')
        if command == 'ZRANK' and key and value:
            try:
                rank = utils.get_rank_for_value(key=key, value=value)
            except Exception as e:
                print("Error: ", str(e))
                return HttpResponse("Error")
        return HttpResponse(rank)

def get_zrange(request):
    if request.method == 'GET':
        command = request.GET.get('command')
        key = request.GET.get('key')
        start = int(request.GET.get('start'))
        stop = int(request.GET.get('stop'))
        withscores = request.GET.get('withscores')
        values = []
        if command == 'ZRANGE' and key:
            try:
                values = utils.get_values_for_range(key=key, start=start, stop=stop, is_withscores=withscores)
            except Exception as e:
                print("Error", str(e))
                return HttpResponse("Error")
        return HttpResponse(values)
    
def clear(request):
    try:
        utils.clear()
    except Exception as e:
        print("Error: "+str(e))
        return HttpResponse(e)
    return HttpResponse("CLEARED")