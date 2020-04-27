from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone, dateformat
from .models import *
from .decorators import *

from random import random, seed, randint
# Create your views here.
from .forms import UserSignUp, UserLogin


def base(request):
    return render(request, "base.html")


@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        email = request.POST.get('email')
        update = request.POST.get('updatemsg')
        updatetime = timezone.now()
        if email == '' or email is None:
            messages.error(request, 'Email field is empty')
        elif update is None or update == '':
            messages.error(request, 'Message field is required')
        else:
            send_email = SendEmail(email=email, update=update, updateTime=updatetime)
            send_email.save()
            return redirect('home')
    discussions = Create.objects.all().order_by("-createTime")
    context = {
        "discussions": discussions,
    }
    return render(request, "my_app/home.html", context)


@unauthenticated_user
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('uid')
        password = request.POST.get('pwd')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, "my_app/account/login.html")


@unauthenticated_user
def signup(request):
    if request.method == "POST":
        form = UserSignUp(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = UserSignUp()

    return render(request, "my_app/account/signup.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    your_discussions = Create.objects.all().order_by('-createTime')
    y_c = Discuzz.objects.all().order_by('-reply_time')
    # print(y_c)
    # y_r = y_c.username
    # print(y_c[0].username)
    t = []
    for y in y_c:
        t.append(y)

    return render(request, 'my_app/account/profile.html', {'your_discussions': your_discussions, 't': t})


def about(request):
    return render(request, 'my_app/help/about.html')


def contact(request):
    return render(request, 'my_app/help/contact.html')


@login_required(login_url='login')
def join(request):
    if request.method == "POST":
        join_disc_id = request.POST.get('discussionid')

        if join_disc_id is None or join_disc_id == '':
            messages.error(request, "Empty field")

        else:
            try:
                disc_name = Create.objects.get(discussionCode=join_disc_id)
            except Create.DoesNotExist:
                disc_name = None

            if disc_name is None:
                messages.error(request, "Discussion ID NOT FOUND")
            else:
                url = '/discuzz/%s' % join_disc_id
                return redirect(url)

    return render(request, 'my_app/motion/join.html')


@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        admin = request.POST.get('admin')
        payment_mode = request.POST.get('payment_mode')
        payment_code = request.POST.get('payment_code')
        subtopic = request.POST.get('subtopic')
        create_random(subtopic)
        discussion_code = create_random(subtopic)
        print(discussion_code)
        description = request.POST.get('description')
        question = request.POST.get('question')
        discussioncode = discussion_code
        create_time = timezone.now()

        if topic is None or topic == '':
            messages.error(request, 'Topic field is empty')

        elif admin is None or admin == '':
            messages.error(request, 'The admin field is empty')

        elif payment_mode is None or payment_mode == '':
            messages.error(request, 'The payment mode field is empty')

        elif payment_code is None or payment_code == '':
            messages.error(request, 'The payment code field is empty')

        elif subtopic is None or subtopic == '':
            messages.error(request, 'The Sub Topic field is empty')

        elif description is None or description == '':
            messages.error(request, 'The description field is empty')

        elif question is None or question == '':
            messages.error(request, 'The question field is empty')

        else:
            create_query = Create(topic=topic, admin=admin, paymentMode=payment_mode, paymentCode=payment_code,
                                  subtopic=subtopic, description=description, question=question,
                                  discussionCode=discussioncode, createTime=create_time)
            create_query.save()
            messages.success(request, "Successfully added")
            return redirect('join')

    return render(request, 'my_app/motion/create.html')


@login_required(login_url='login')
def discuzz(request, discussion_details):
    try:
        disc_name = Create.objects.get(discussionCode=discussion_details)
        if request.method == 'POST':
            discussioncode = disc_name.discussionCode
            reply = request.POST.get('reply')
            username = request.POST.get('username')
            replytime = timezone.now()
            reply_query = Discuzz(discussion_code=discussioncode, reply=reply, username=username, reply_time=replytime)
            reply_query.save()
            replies = Discuzz.objects.all()
            url = '/discuzz/%s' % discussioncode
            return redirect(url)
        try:
            replies = Discuzz.objects.all()
            return render(request, 'my_app/motion/discuzz.html', {'disc_name': disc_name, "replies": replies})
        except Discuzz.DoesNotExist:
            discuzz= None

    except Create.DoesNotExist:
        disc_name = None
        messages.error(request, "The Discussion ID does not exist, Please check and try again")
        return render(request, 'my_app/help/not-found.html')


@login_required(login_url='login')
def c19(request):
    return render(request, 'my_app/news/c19.html')


@login_required(login_url='login')
def wnews(request):
    return render(request, 'my_app/news/wnews.html')


def create_random(subtopic):
    num1 = randint(1, 9)
    num2 = randint(2, 8)
    num3 = randint(3, 7)
    num4 = randint(4, 6)
    num5 = randint(5, 11)
    num6 = randint(4, 6)
    num7 = randint(3, 7)
    num8 = randint(2, 8)
    num9 = randint(1, 9)
    num10 = randint(0, 3)

    sub = subtopic.split()
    print(sub)
    sub1 = sub[1].upper()

    code = '%d%d%s%dDISC%d%du%dz%dZ%d%dDi%d%d' % (num7, num8, sub1, num6, num7, num10, num1, num2, num3, num4, num5,
                                                  num9)
    return code
