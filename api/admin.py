from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Installment)
admin.site.register(requestLoan)
admin.site.register(loanPayment)