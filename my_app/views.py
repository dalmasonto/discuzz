from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Add
from django.http import HttpResponseRedirect


# Create your views here.

def home(request):
    todo_items = Add.objects.all().order_by("-added_date")
    return render(request, "/my_app/add_todo.html", {
        "todo_items": todo_items
    })


def add_html(request):
    return render(request, "/my_app/add_todo.html", )


def new_search(request):
    return render(request, 'my_app/new_Search.html')


def add_todo(request):
    current_date = timezone.now()
    content = request.POST.get("item", False)
    created_object = Add.objects.create(added_date=current_date, text=content)
    return HttpResponseRedirect("/#todos")


def delete_todo(request, todo_id):
    Add.objects.get(id=todo_id).delete()
    return HttpResponseRedirect("/#todos")
