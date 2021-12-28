from django.contrib.auth import get_user_model
from django.contrib.auth.models import *
import csv
# from .utils import cartData, check_transaction, check_instalment
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from .models import *
import requests
import secrets
import threading
import math
# from dateutil.relativedelta import *
import string
import random
import ast
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.shortcuts import render, redirect
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.core import serializers
from django.core.mail import send_mail
from datetime import datetime
from datetime import timedelta 
import json
from django.contrib import messages
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import requests
import os

# Create your views here.

def operator(request):
    if request.method == 'POST':
        try:
            user1 = User.objects.get(email=request.POST['email'])
            return render(request, 'operator.html', {'error': 'The Email  has already been taken'})
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.POST['phonenumber'])
                return render(request, 'operator.html', {'error': 'The phone number  has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    FirstName=request.POST['firstname'],
                    LastName=request.POST['lastname'],
                    email=request.POST['email'],
                    phone=request.POST['phonenumber'],
                    password=request.POST['password']
                    )
            return redirect('user')
    else:
        return render(request, 'operator.html')

def login(request):
    if request.method == "POST":
        customer = authenticate(
            email=request.POST['email'], password=request.POST['password'])
        if customer is not None:
            django_login(request, customer)
            return redirect('installment')
    else:
        return render(request, 'login.html')
    
def customer_login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        try:
            user = User.objects.get(phone=body['phone'])
            if user.check_password(body['password']):
                token = Token.objects.get_or_create(user=user)[0]
                data = {
                    'user_id': user.id,
                    'email': user.email,
                    'status': 'success',
                    'token': str(token),
                    'code': status.HTTP_200_OK,
                    'message': 'Login successfull',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
            else:
                data = {
                    'status': 'failure',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Phone or password incorrect!',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
        except User.DoesNotExist:
            data = {
                'status': 'failure',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Phone or password incorrect!',
                'data': []
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type='application/json')


@login_required(login_url='/login')
def logout(request):
    django_logout(request)
    return redirect('login')

@login_required(login_url='/login')
def user(request):
    users = User.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(Q(phone__icontains=search_query))
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users.html', {'users': users, 'page_obj': page_obj})


@login_required(login_url='/login')
def installment(request):
    inst = Installment.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        inst = Installment.objects.filter(Q(created_at__icontains=search_query))
    paginator = Paginator(inst, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'installment.html', {'inst': inst, 'page_obj': page_obj})


def pay_install(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        today = datetime.today()
        print(body)
        user_id = body['user_id']
        user = User.objects.get(id=user_id)
        amount = int(body['amount'])
        transaction=Installment()
        transaction.user=user
        transaction.Amount=amount
        transaction.save()
        data = {
            'result': 'Payment done successfully!!!',
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')

class Getpayment(ListAPIView):
    serializer_class = InstallmentSerializer

    def get_queryset(self):
        
        return Installment.objects.filter(user=self.kwargs['user_id'])



@login_required(login_url='/login')
def requestedloan(request):
    reqloan = requestLoan.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        reqloan = requestLoan.objects.filter(Q(Request_at__icontains=search_query))
    paginator = Paginator(reqloan, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'requestedloan.html', {'reqloan': reqloan, 'page_obj': page_obj})

@login_required(login_url='/login')
def paidloan(request):
    paidloan = loanPayment.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        paidloan = loanPayment.objects.filter(Q(Pay_at__icontains=search_query))
    paginator = Paginator(paidloan, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'paidloan.html', {'paidloan': paidloan, 'page_obj': page_obj})

def pay_loan(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        today = datetime.today()
        print(body)
        user_id = body['user_id']
        user = User.objects.get(id=user_id)
        amount = int(body['amount'])
        transaction=loanPayment()
        transaction.user=user
        transaction.Amount=amount
        transaction.save()
        data = {
            'result': 'Payment done successfully!!!',
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')

class getuserbyid(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):            
        return User.objects.filter(id=self.kwargs['user_id'])

class Getrequestedloan(ListAPIView):
    serializer_class = requestLoanSerializer

    def get_queryset(self):            
        return requestLoan.objects.filter(user=self.kwargs['user_id'])


class Getpaidloan(ListAPIView):
    serializer_class = loanPaymentSerializer

    def get_queryset(self):            
        return loanPayment.objects.filter(user=self.kwargs['user_id'])


class NotificationListView(ListAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer



class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.request.data['user_id'])
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password ChangePasswupdated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

@login_required(login_url='/login')
def updateUser(request, updateID):
    updateuser = User.objects.get(id=updateID)
    if request.method == 'POST':
        updateuser.FirstName = request.POST['firstname']
        updateuser.LastName = request.POST['lastname']
        updateuser.phone = request.POST['phonenumber']
        updateuser.email = request.POST['email']
        updateuser.save()
        # Addproduct = True
        return redirect('user')
    else:
        return render(request, 'updatemembers.html', {'updateuser': updateuser})


def delete_user(request, userID):
    user = User.objects.get(id=userID)
    user.delete()
    return redirect('user')

def ApproveLoan(request, approveID):
    approveloan = requestLoan.objects.get(id=approveID)
    approveloan.Approve = True
    approveloan.save()
    return redirect('requestedloan')


class RequestLoanCreateView(CreateAPIView):
    queryset = requestLoan.objects.all()
    serializer_class = requestLoanSerializer



