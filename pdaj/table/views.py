from django.shortcuts import render
from .models import Table
from .serializers import TableSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

import tracemalloc
from math import sqrt
import time
import multiprocessing as mp

# Create your views here.
# table = Table.objects.all()
# serializer = TableSerializer(table,many=True)
#
#return JsonResponse(serializer.data, safe=False,status=200)

points_mp = []

@csrf_exempt
@api_view(['POST'])
def sequentially(request):
    x = request.data["n"]
    y = request.data["m"]
    points = request.data["points"]
    result, time, max_memory = sequential(x,y,points)
    table = Table(result=result,time_in_sec=time,max_memory_in_MB=max_memory)
    serializer = TableSerializer(table)
    return JsonResponse(serializer.data, safe=False,status=200)

@csrf_exempt
@api_view(['POST'])
def list_comprehension(request):
    x = request.data["n"]
    y = request.data["m"]
    points = request.data["points"]
    result, time, max_memory = comprehension(x,y,points)
    table = Table(result=result,time_in_sec=time,max_memory_in_MB=max_memory)
    serializer = TableSerializer(table)
    return JsonResponse(serializer.data, safe=False,status=200)

@csrf_exempt
@api_view(['POST'])
def generator(request):
    x = request.data["n"]
    y = request.data["m"]
    points = request.data["points"]
    result, time, max_memory = generator2(x,y,points)
    table = Table(result=result,time_in_sec=time,max_memory_in_MB=max_memory)
    serializer = TableSerializer(table)
    return JsonResponse(serializer.data, safe=False,status=200)

@csrf_exempt
@api_view(['POST'])
def multiprocessing(request):
    x = request.data["n"]
    y = request.data["m"]
    points_mp.append(request.data["points"])
    result, time, max_memory = multi_processing(x,y)
    table = Table(result=result,time_in_sec=time,max_memory_in_MB=max_memory)
    serializer = TableSerializer(table)
    return JsonResponse(serializer.data, safe=False,status=200)


def sequential(x,y,points):
    start = time.time()
    res = seq(x,y,points)
    env = time.time()
    t = env - start
    tracemalloc.start()
    seq(x,y,points)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return res, t, peak/10**6
    
def seq(x,y,points):
    table = []
    for i in range(x):
        for j in range(y):
            table.append([i,j])
    
    result = distance_seq(table,points)
    return result
    
def distance_seq(table,points):
    res = []
    for t in table:
        result = []
        for idx,p in enumerate(points):
            element = [sqrt((abs(p[0] - t[0]))**2 + (abs(p[1] - t[1]))**2),idx]
            result.append(element)
        res.append((min(result))[1])
        
    return res

def comprehension(x,y,points):
    start = time.time()
    res = list_compr(x,y,points)
    env = time.time()
    t = env - start
    tracemalloc.start()
    list_compr(x,y,points)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return res, t, peak/10**6
    
def list_compr(x,y,points):
    table = [[i,j] for i in range(x) for j in range(y)]
    res = distance_comprehension(table,points)
    return res
    
def distance_comprehension(table,points):
    res = [min([[sqrt((abs(p[0] - t[0]))**2 + (abs(p[1] - t[1]))**2),idx] for idx,p in enumerate(points)])[1] for t in table]
    return res

def generator2(x,y,points):
    start = time.time()
    res = gen_iter(x,y,points)
    env = time.time()
    t = env - start
    tracemalloc.start()
    gen_iter(x,y,points)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return res, t, peak/10**6

def gen_iter(x,y,points):
    a = gen_fun(x,y)
    res=[]
    for el in a:
        d = distance_generator_iterator(el,points)
        for e in d:
            res.append((min(e))[1])
            
    return res
    
def gen_fun(x,y):
    for i in range(x):
        for j in range(y):
            yield [i,j]
            
def distance_generator_iterator(table,points):
    result = []
    for idx,p in enumerate(points):
        element = [sqrt((abs(p[0] - table[0]))**2 + (abs(p[1] - table[1]))**2),idx]
        result.append(element)
    yield result
    
def multi_processing(x,y):
    start = time.time()
    res = multi_p(x,y)
    env = time.time()
    t = env - start
    tracemalloc.start()
    multi_p(x,y)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return res, t, peak/10**6

def multi_p(x,y):
    pool = mp.Pool()
    table = pool.imap(gen_fun_mp,[[x,y]])
    table2 = next(table)
    results = pool.map(distance_mp,table2,chunksize=10000)
    res = []
    try:    
        for r in results:
            res.append(r)
    except StopIteration:
        print("Out of elements")
    pool.terminate()
    return res

def gen_fun_mp(params):
    res = []
    x = params[0]
    y = params[0]
    for i in range(x):
        for j in range(y):
            res.append([i,j])
    return res


def distance_mp(t):
    res = []
    result = []
    for idx,p in enumerate(points_mp[0]):
        element = [sqrt((abs(p[0] - t[0]))**2 + (abs(p[1] - t[1]))**2),idx]
        result.append(element)
    return ((min(result))[1])
    
    
    
