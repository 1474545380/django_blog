from django.shortcuts import render
from django.views import View
# Create your views here.
class RegisterView(View):
    def get(selfself,request):
        return render(request,'register.html')