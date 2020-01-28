from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Add, Quizone, Quiztwo, Quizthree, Quizfour, Quizfive, Quizsix
from .models import UserSignup
from django.http import HttpResponseRedirect


# Create your views here.

def home(request):
    quizone_answers = Quizone.objects.all().order_by("-added_date")
    quiztwo_answers = Quiztwo.objects.all().order_by("-added_date")
    quizthree_answers = Quizthree.objects.all().order_by("-added_date")
    quizfour_answers = Quizfour.objects.all().order_by("-added_date")
    quizfive_answers = Quizfive.objects.all().order_by("-added_date")
    quizsix_answers = Quizsix.objects.all().order_by("-added_date")
    return render(request, "base.html", {
        "quizone_answers": quizone_answers,
        "quiztwo_answers": quiztwo_answers,
        "quizthree_answers": quizthree_answers,
        "quizfour_answers": quizfour_answers,
        "quizfive_answers": quizfive_answers,
        "quizsix_answers": quizsix_answers
    })


def about_page(request):
    todo_items = Add.objects.all().order_by("-added_date")
    return render(request, 'my_app/about.html', {
        "todo_items": todo_items
    })


def new_search(request):
    return render(request, 'my_app/new_Search.html')


def add_todo_page(request):
    return render(request, 'my_app/add_todo.html')


def signup_page(request):
    return render(request, 'my_app/signup.html')


def todos_page(request):
    todo_items = Add.objects.all().order_by("-added_date")
    return render(request, 'my_app/todos.html', {
        "todo_items": todo_items
    })


def contacts_page(request):
    member = UserSignup.objects.all()
    return render(request, 'my_app/contacts.html', {
        "member": member
    })


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
        UserSignup.objects.create(username=username, fname=fname, lname=lname, email=email, phone_number=phone_no,
                                  password=pwd)
    else:
        return render(request, 'my_app/signup.html')

    return HttpResponseRedirect("/")


def delete_todo(request, todo_id):
    Add.objects.get(id=todo_id).delete()
    return HttpResponseRedirect("/")


def delete_contact(request, contact_id):
    UserSignup.objects.get(id=contact_id).delete()
    return HttpResponseRedirect("/#quizes")


def quizone_answer(request):
    current_date = timezone.now()
    content = request.POST.get("quizone", False)
    Quizone.objects.create(added_date=current_date, text=content)
    return HttpResponseRedirect("/#quizes")


def quiztwo_answer(request):
    current_date = timezone.now()
    content = request.POST.get("quiztwo", False)
    Quiztwo.objects.create(added_date=current_date, text=content)
    return HttpResponseRedirect("/#quizes")


def quizthree_answer(request):
    current_date = timezone.now()
    content = request.POST.get("quizthree", False)
    Quizthree.objects.create(added_date=current_date, text=content)
    return HttpResponseRedirect("/#quizes")


def quizfour_answer(request):
    current_date = timezone.now()
    content = request.POST.get("quizfour", False)
    Quizfour.objects.create(added_date=current_date, text=content)
    return HttpResponseRedirect("/#quizes")


def quizfive_answer(request):
    current_date = timezone.now()
    content = request.POST.get("quizfive", False)
    Quizfive.objects.create(added_date=current_date, text=content)
    return HttpResponseRedirect("/#quizes")


def quizsix_answer(request):
    current_date = timezone.now()
    content = request.POST.get("quizsix", False)
    Quizsix.objects.create(added_date=current_date, text=content)
    return HttpResponseRedirect("/#quizes")
