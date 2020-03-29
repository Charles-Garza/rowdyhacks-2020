from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from .models import allCases, state, county
from .serializers import AllCaseSerializer, AllStatesSerializer, AllCountySerializer

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'all-cases': 'cases/',
        'country': '/country/<str:pk>/',
        'all-states': '/states/',
        'state': '/state/<str:pk>/',
        'all-county': '/state/<str:fk>/counties',
        'county': '/state/<str:fk>/county/<str:pk>/',
    }

    return Response(api_urls)

@api_view(['GET'])
def all_covid_cases(request):
    cases = allCases.objects.values().last()
    serializer = AllCaseSerializer(cases, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def all_state_cases(request):
    us_state_cases = state.objects.all()
    serializer = AllStatesSerializer(us_state_cases, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def state_cases(request, pk):
    all_state_cases = state.objects.all().filter(state_name=pk).values().last()
    serializer = AllStatesSerializer(all_state_cases, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def every_county_case(request, fk):
    all_county_cases = county.objects.filter(state_name=fk).all()
    serializer = AllCountySerializer(all_county_cases, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def state_county_cases(request, fk, pk):
    all_county_cases = county.objects.filter(state_name=fk).get(county_name=pk)
    serializer = AllCountySerializer(all_county_cases, many=False)
    return Response(serializer.data)
