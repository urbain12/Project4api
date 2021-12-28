from django.urls import path,include
from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #website
    path('',login,name='login'),
    path('logout/',logout,name='logout'),
    path('user/',user,name='user'),
    path('operator/',operator,name='operator'),
    path('customer_login/',csrf_exempt(customer_login),name='customer_login'),
    path('installment/',installment,name='installment'),
    path('pay_install/',csrf_exempt(pay_install),name='pay_install'),
    path('Getpayment/<int:user_id>/',Getpayment.as_view()),
    path('requestedloan/',requestedloan,name='requestedloan'),
    path('paidloan/',paidloan,name='paidloan'),
    path('pay_loan/',csrf_exempt(pay_loan),name='pay_loan'),
    path('Getrequestedloan/<int:user_id>/',Getrequestedloan.as_view()),
    path('getuserbyid/<int:user_id>/',getuserbyid.as_view()),
    path('Getpaidloan/<int:user_id>/',Getpaidloan.as_view()),
    path('Notification/',NotificationListView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('Updateuser/<id>/', UserUpdateView.as_view()),
    path('updateUser/<int:updateID>',updateUser,name="updateUser"),
    path('delete_user/<int:userID>',delete_user,name="delete_user"),
    path('ApproveLoan/<int:approveID>',ApproveLoan,name="ApproveLoan"),
    path('RequestLoan/',RequestLoanCreateView.as_view()),
    path('register/',register.as_view()),











]