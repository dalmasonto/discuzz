from urllib.parse import quote_plus

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import JsonResponse

from random import random, seed, randint
# Rest framework
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

import json

from .decorators import unauthenticated_user
from .forms import UserSignUp, PicForm
from my_app.models import Create, Discuzz, UserExtension, Comment, Topic, SendEmail

from my_app.rest_serializers import UserExtensionSerializer, UserSerializer


def page_not_found(request, exception):
    context = {
        'page': exception.path
    }
    return render(request, 'my_app/help/not-found.html', context)


def handler_500(request, exception):
    context = {
        'page': exception
    }
    return render(request, 'my_app/help/not-found.html', context)


def api_message_us(request):
    response_msg = ''
    response_type = ''
    if request.method == "POST":
        email = request.user
        update = request.POST.get('updatemsg')
        updatetime = timezone.now()
        if email == '' or email is None:
            response_msg = 'Email field is empty'
            response_type = 'danger'
        elif update is None or update == '':
            response_msg = 'The message field is empty'
            response_type = 'danger'
        else:
            send_email = SendEmail(email=email, update=update, updateTime=updatetime)
            send_email.save()
            response_msg = 'The email has been sent successfully'
            response_type = 'success'

        data = {
            'response_msg': response_msg,
            'response_type': response_type
        }
        return JsonResponse(data, status=201)


def api_home_topic_form(request):
    if request.method == "POST":
        user = request.user
        topic = request.POST.get('topic')
        subtopic = request.POST.get('subtopic')

        if topic == '' or topic is None:
            response_msg = 'Topic field is empty'
            response_type = 'danger'
        elif subtopic is None or subtopic == '':
            response_msg = 'subtopic field is empty'
            response_type = 'danger'
        else:
            add_topic = Topic(user=user, topic=topic, subtopic=subtopic)
            add_topic.save()
            response_msg = 'Topic successfully created'
            response_type = 'success'
        data = {
            'response_msg': response_msg,
            'response_type': response_type
        }
        return JsonResponse(data, status=201)


def api_all_queries(request, *args, **kwargs):
    objects = Create.objects.all()

    data_for_front_end = [{"id": obj.id,
                           "pic": UserExtension.objects.get(user=obj.admin).profile_pic.url,
                           "topic": obj.topic,
                           "admin": obj.admin.username,
                           "paymentMode": obj.paymentMode,
                           "paymentCode": obj.paymentCode,
                           "subtopic": obj.subtopic,
                           "description": obj.description,
                           "question": obj.question,
                           "discussionCode": obj.discussionCode,
                           "replies": Discuzz.objects.filter(discussion_code=obj).count(),
                           "createTime": obj.createTime} for obj in objects]

    data = {
        "response": data_for_front_end
    }

    return JsonResponse(data, status=200)


def base(request):
    pics = UserExtension.objects.all()
    my_pic = []
    for pic in pics:
        my_pic.append(pic.user)

    if request.user not in my_pic:
        pic = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRoHeooXTzmQjxc83ln5YOLHZlC5L8bUnFzAg&usqp=CAU'
    else:
        obj = UserExtension.objects.get(user=request.user)
        pic = obj.profile_pic.url
    context = {
        'my_pic': pic,
    }
    return render(request, "base.html", context)


@login_required(login_url='login')
def home(request):
    discussions = Create.objects.all().order_by("-createTime")
    all_replies = Discuzz.objects.all()
    my_questions = Create.objects.filter(admin=request.user).count()
    pics = UserExtension.objects.all()
    my_pic = []
    for pic in pics:
        my_pic.append(pic.user)

    if request.user not in my_pic:
        pic = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRoHeooXTzmQjxc83ln5YOLHZlC5L8bUnFzAg&usqp=CAU'
    else:
        obj = UserExtension.objects.get(user=request.user)
        pic = obj.profile_pic.url

    context = {
        "discussions": discussions,
        "all_replies": all_replies,
        "page": 'Home',
        'my_questions': my_questions,
        'my_pic': pic,
        'pics': pics
    }
    return render(request, "account/home.html", context)


@unauthenticated_user
@transaction.atomic
def user_login(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST.get('uid')
        password = request.POST.get('pwd')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            if request.GET.get('next') is not None:
                return redirect(request.GET.get('next'))

            return redirect("home")
        else:
            messages.error(request, 'Username or password is incorrect')

    context = {
        'page': 'Login'
    }
    return render(request, "account/login.html", context)


@unauthenticated_user
@transaction.atomic
def signup(request):
    users = User.objects.all()
    form = UserSignUp()
    errors = []
    context = {
        "form": form,
        "page": "Sign up"
    }
    if request.method == "POST":
        form1 = UserSignUp(request.POST)
        if form1.is_valid():
            form1.date_joined = timezone.now()
            form1.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')

        elif not form1.is_valid():
            messages.error(request, errors)
            render(request, "account/signup.html", context)

    return render(request, "account/signup.html", context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    our_location = UserExtension.objects.get(user=request.user).location
    suggested_location = UserExtension.objects.get(user=request.user).friends.all()
    for loc in suggested_location:
        print(loc.userextension.location)

    your_discussions = Create.objects.all().order_by('-createTime')
    y_c = Discuzz.objects.all().order_by('-reply_time')
    t = []
    hidden_q = []
    hidden_r = []
    hidden_c = []
    hidden_t = []

    friends_query = UserExtension.objects.get(user=request.user).friends.all()
    friends_count = UserExtension.objects.get(user=request.user).friends.count()
    friends = []
    for friend in friends_query:
        friends.append(friend)

    langs = request.user.userextension.programming_languages
    lang_count = len(langs)

    profile_ = '%s profile' % request.user.username
    questions_count = Create.objects.filter(admin=request.user).count()
    hidden_questions = Create.objects.filter(admin=request.user)
    replies_count = Discuzz.objects.filter(username=request.user).count()
    hidden_replies = Discuzz.objects.filter(username=request.user)
    comments_count = Comment.objects.filter(commented_by=request.user).count()
    hidden_comments = Comment.objects.filter(status='hidden')
    topics_count = Topic.objects.filter(user=request.user).count()
    hidden_topics = Topic.objects.filter(user=request.user)

    my_quizes = Create.objects.filter(admin=request.user)

    pics = UserExtension.objects.all()
    my_pic = []
    for pic in pics:
        my_pic.append(pic.user)

    if request.user not in my_pic:
        pic = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRoHeooXTzmQjxc83ln5YOLHZlC5L8bUnFzAg&usqp=CAU'
    else:
        obj = UserExtension.objects.get(user=request.user)
        pic = obj.profile_pic.url

    for y in y_c:
        t.append(y)

    for q in hidden_questions:
        if q.status == 'hidden':
            hidden_q.append(q)
    hidden_questions_count = len(hidden_q)

    for r in hidden_replies:
        if r.status == 'hidden':
            hidden_r.append(r)
    hidden_replies_count = len(hidden_r)

    for c in hidden_comments:
        if c.status == 'hidden':
            hidden_c.append(c)
    hidden_comments_count = len(hidden_c)

    for x in hidden_topics:
        if x.status == 'hidden':
            hidden_t.append(x)

    hidden_topics_count = len(hidden_t)

    pic_form = PicForm(instance=request.user.userextension)

    context = {
        'your_discussions': your_discussions,
        't': t,
        'questions_count': questions_count,
        'hidden_questions_count': hidden_questions_count,
        'replies_count': replies_count,
        'hidden_replies_count': hidden_replies_count,
        'comments_count': comments_count,
        'hidden_comments_count': hidden_comments_count,
        'my_quizes': my_quizes,
        'topics_count': topics_count,
        'hidden_topics_count': hidden_topics_count,
        'page': profile_,
        'pic_form': pic_form,
        'my_pic': pic,
        'friends': friends,
        'friends_count': friends_count - 1,
        'languages': langs,
        'lang_count': lang_count
    }

    return render(request, 'account/profile.html', context)


def profile_pic_update(request):
    if request.method == 'POST':
        user_extension_form = PicForm(request.POST, request.FILES, instance=request.user.userextension)
        if user_extension_form.is_valid():
            print('UPDATED')
            user_extension_form.save()
        else:
            print('NOT UPDATED')

    return redirect('profile')


def get_user_info(request, username):
    user = User.objects.get(username=username)
    topics = Topic.objects.filter(user=user).count()
    quizes = Create.objects.filter(admin=user).count()
    replies = Discuzz.objects.filter(username=user).count();
    comments_c = Comment.objects.filter(commented_by=user).count()
    pic = UserExtension.objects.get(user=user)
    dat = {
        'first': user.first_name,
        'last': user.last_name,
        'email': user.email,
        'username': user.username,
        'pic': pic.profile_pic.url
    }

    data = {
        'user': dat,
        'topics': topics,
        'quizes': quizes,
        'replies': replies,
        'comments': comments_c
    }
    return JsonResponse(data, status=200)


def add_friends(request):
    all_users = User.objects.all()

    my_friends = request.user.userextension.friends.all()

    friend_requests = request.user.userextension.friend_requests.all()

    users = []
    friends = []
    requests = []

    users_who_are_friends_and_requests = []
    users_who_sent_friend_requests = []

    for user in all_users:
        users.append(user)

    for friend in my_friends:
        friends.append(friend)

    for friend_req in friend_requests:
        requests.append(friend_req)

    for user in users:
        user_friend_requests = user.userextension.friend_requests.all()
        user_friends = user.userextension.friends.all()

        if user in friends:
            user_case = 'friend'
            mutual = 0

            for u_friend in user_friends:
                if u_friend in friends:
                    mutual += 1

            what_to_append = {
                'person': user,
                'user_case': user_case,
                'mutual_friends': mutual
            }

        elif user in requests:
            user_case = 'request'
            mutual = 0

            for u_friend in user_friends:
                if u_friend in friends:
                    mutual += 1

            what_to_append = {
                'person': user,
                'user_case': user_case,
                'mutual_friends': mutual
            }

        elif user in requests:
            user_case = 'request'
            mutual = 0

            for u_friend in user_friends:
                if u_friend in friends:
                    mutual += 1

            what_to_append = {
                'person': user,
                'user_case': user_case,
                'mutual_friends': mutual
            }

        elif request.user in user_friend_requests:
            user_case = 'awaiting'
            mutual = 0

            for u_friend in user_friends:
                if u_friend in friends:
                    mutual += 1

            what_to_append = {
                'person': user,
                'user_case': user_case,
                'mutual_friends': mutual
            }

        else:
            user_case = 'new'
            user_friends = user.userextension.friends.all()
            mutual = 0

            for u_friend in user_friends:
                if u_friend in friends:
                    mutual += 1

            what_to_append = {
                'person': user,
                'user_case': user_case,
                'mutual_friends': mutual
            }

        users_who_are_friends_and_requests.append(what_to_append)
        print('Appended ' + user.username + ' with ' + user_case)

    context = {
        'users_who_are_friends_and_requests': users_who_are_friends_and_requests,
    }

    return render(request, 'account/friends/friends.html', context)


def api_add_friend_request(request, username):
    user = request.user
    user_to_send_to = User.objects.get(username=username)

    user_to_send_to_friend_requests = user_to_send_to.userextension.friend_requests.all()
    if user not in user_to_send_to_friend_requests:

        user_to_send_to.userextension.friend_requests.add(request.user)
        user_to_send_to.userextension.save()

        user_to_send_to_notifications = user_to_send_to.userextension.notifications

        type_of_notifications = type(user_to_send_to_notifications)

        if type_of_notifications == dict:
            identity = 2
        elif type_of_notifications == list:
            identity = user_to_send_to_notifications[-1]['id'] + 1
            print('ID', identity)
            print('THE TYPE AT THIS POINT one is', type(user_to_send_to_notifications))

        new_notification = {
            "id": identity,
            "type": "request",
            "by": UserExtensionSerializer(request.user.userextension, many=False).data,
            "date_sent": "today"
        }

        if type_of_notifications == dict:
            s = [user_to_send_to_notifications, new_notification]
            user_to_send_to.userextension.notifications = s
            user_to_send_to.userextension.save()

        elif type_of_notifications == list:
            s = user_to_send_to_notifications
            s.append(new_notification)
            user_to_send_to.userextension.notifications = s
            user_to_send_to.userextension.save()
        else:
            print('NEW TYPE IS: ', type(notifications()))

    data = {
        'response': 'Request sent'
    }
    return JsonResponse(data)


def api_add_remove_friend(request, option, username):
    print('AM TIRED DOING THIS')
    user = request.user.userextension
    user_to_add_remove = User.objects.get(username=username)
    friends = user.friends.all()

    response = ''
    if option == 'add':
        if user_to_add_remove not in friends:
            user.friends.add(user_to_add_remove)
            user.friend_requests.remove(user_to_add_remove)
            user_to_add_remove.userextension.friends.add(request.user)
            user_to_add_remove.userextension.friend_requests.remove(request.user)
            user.save()
            response = 'Added'
            make_notification(request.user, user_to_add_remove, 'now_friends')
            make_notification(user_to_add_remove, request.user, 'now_friends')

    if option == 'remove':
        if user_to_add_remove in friends:
            user.friends.remove(user_to_add_remove)
            user.save()
            response = 'Removed'

    data = {
        'response': response
    }
    return JsonResponse(data)


class Api_All_Users(APIView):

    def get(self, format=None):
        extensions = UserExtension.objects.all()
        serializer = UserExtensionSerializer(extensions, many=True)

        return Response(serializer.data)


# class Api_User_Details(APIView):
#
#     def get(self, format=None):
#         print('THE USERNAME IS ', self['kwargs']['username'])
#         # user = User.objects.get(username='dalmas')
#         extensions = UserExtension.objects.all()
#         serializer = UserExtensionSerializer(extensions, many=True)
#
#         return Response({'data': 'data'})


@api_view(['GET'])
def get_user(request, username):
    user = User.objects.get(username=username)
    extensions = UserExtension.objects.get(user=user)
    serializer = UserExtensionSerializer(extensions, many=False)

    return Response(serializer.data)


def notifications(request):
    notifications_ = request.user.userextension.notifications
    type_of_notification = type(notifications)

    friend_requests = request.user.userextension.friend_requests.all()
    requests = []
    for req in friend_requests:
        requests.append(req)

    if type_of_notification == list:
        notes = notifications_

        context = {
            'friend_requests': requests,
            'page': 'Notifications',
            'notifications': notes,
        }

        return render(request, 'account/notifications.html', context)

    elif type_of_notification == dict:
        notes = [notifications_]
        print('ELSE IF ', notes)

        context = {
            'friend_requests': requests,
            'page': 'Notifications',
            'notifications': notes,
        }

        return render(request, 'account/notifications.html', context)
    else:
        context = {
            'friend_requests': requests,
            'page': 'Notifications',
            'notifications': notifications_
        }
        return render(request, 'account/notifications.html', context)


def get_notifications(request):
    friend_requests = request.user.userextension.friend_requests.all()
    notifications_check = len(request.user.userextension.notifications)
    total_number = notifications_check

    data = {
        'notifications_count': total_number,
    }
    return JsonResponse(data)


def delete_notification(request, note_ID):
    my_notifications = request.user.userextension.notifications

    for note in my_notifications:
        if note['id'] == int(note_ID):
            send = note
            my_notifications.remove(note)
            request.user.userextension.notifications = my_notifications
            request.user.userextension.save()

    data = {
        'notification': send
    }
    return JsonResponse(data)


# from validate_email import validate_email
# Check whether the email is valid
# is_valid = validate_email('example@example.com')
# chaeck whether the email exists in the real world
# is_valid = validate_email('example@example.com',verify=True)

def make_notification(me, other_user, type_, quiz=None):
    user_me = User.objects.get(username=me.username)
    user_to_send_to = User.objects.get(username=other_user)

    user_to_send_to_notifications = user_to_send_to.userextension.notifications

    type_of_notifications = type(user_to_send_to_notifications)

    if type_of_notifications == dict:
        identity = 2
    elif type_of_notifications == list:
        identity = user_to_send_to_notifications.pop()['id'] + 1

    if type_ == 'request':
        new_notification = {
            'id': identity,
            'type': type_,
            'by': UserExtensionSerializer(user_me.userextension, many=False).data,
            'date_sent': 'today'
        }
    elif type_ == 'message':
        new_notification = {
            'id': identity,
            'type': type_,
            'by': UserExtensionSerializer(user_me.userextension, many=False).data,
            'date_sent': 'today'
        }
    elif type_ == 'question':
        new_notification = {
            'id': identity,
            'type': type_,
            'question': quiz,
            'by': UserExtensionSerializer(user_me.userextension, many=False).data,
            'date_sent': 'today'
        }
    elif type_ == 'now_friends':
        new_notification = {
            'id': identity,
            'type': type_,
            'by': UserExtensionSerializer(user_me.userextension, many=False).data,
            'date_sent': 'today'
        }
        print('ACCEPTED TTTT')

    if type_of_notifications == dict:
        s = [user_to_send_to_notifications, new_notification]
        user_to_send_to.userextension.notifications = s
        user_to_send_to.userextension.save()

    elif type_of_notifications == list:
        s = user_to_send_to_notifications
        s.append(new_notification)
        user_to_send_to.userextension.notifications = s
        user_to_send_to.userextension.save()
    else:
        print('NEW TYPE IS: ', type(type_of_notifications))
