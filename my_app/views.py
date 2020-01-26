from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Add
from .models import UserSignup
from django.http import HttpResponseRedirect


# Create your views here.

def home(request):
    todo_items = Add.objects.all().order_by("-added_date")
    return render(request, "base.html", {
        "todo_items": todo_items
    })


def about_page(request):
    todo_items = Add.objects.all().order_by("-added_date")
    return render(request, 'my_app/about.html',  {
        "todo_items": todo_items
    })


def new_search(request):
    return render(request, 'my_app/new_Search.html')


def add_todo_page(request):
    return render(request, 'my_app/add_todo.html')


def add_todo(request):
    current_date = timezone.now()
    content = request.POST.get("item", False)
    Add.objects.create(added_date=current_date, text=content)
    return HttpResponseRedirect("/")


def form_sign_up(request):
    username = request.POST.get("username", False)
    fname = request.POST.get("fname", False)
    lname = request.POST.get("lname", False)
    email = request.POST.get("email", False)
    phone_no = request.POST.get("phone_number", False)
    pwd = request.POST.get("pwd", False)
    pwd_repeat = request.POST.get("pwd-repeat", False)
    if pwd == pwd_repeat:
        UserSignup.objects.create(username=username, fname=fname, lname=lname, email=email, phone_number=phone_no, password=pwd)
    return HttpResponseRedirect("/")

def delete_todo(request, todo_id):
    Add.objects.get(id=todo_id).delete()
    return HttpResponseRedirect("/")
