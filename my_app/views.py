from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone, dateformat

from Lib.hmac import new
from .models import *
from .decorators import *
from django.utils import safestring, html
from django.forms.utils import ErrorList


from django.http import JsonResponse

from random import random, seed, randint
# Create your views here.
from .forms import *


def api_discuzz_details(request, discussion_details, *args, **kwargs):
    #
    objects = Discuzz.objects.all()
    list_all_replies = []
    for o in objects:
        #  print('The obj at i is', o)
        if o.discussion_code == discussion_details:
            list_all_replies.append(o)

    # print('the length is', len(list_all_replies))

    staff_for_frontend = [{"id": obj.id,
                           "discussionCode": obj.discussion_code,
                           "username": obj.username,
                           "reply": obj.reply,
                           "likes": obj.likes.count(),
                           "dislikes": obj.dislikes.count(),
                           "comments": 0,
                           "reply_time": obj.reply_time
                           } for obj in list_all_replies]

    data = {
        "response": staff_for_frontend,
        "length": len(list_all_replies)
    }

    return JsonResponse(data, safe=False)


def api_message_us(request):

    response_msg = ''
    response_type = ''
    if request.method == "POST":
        email = request.POST.get('email')
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
        topic = request.POST.get('topic')
        subtopic = request.POST.get('subtopic')

        if topic == '' or topic is None:
            response_msg = 'Topic field is empty'
            response_type = 'danger'
        elif subtopic is None or subtopic == '':
            response_msg = 'subtopic field is empty'
            response_type = 'danger'
        else:
            add_topic = Topic(topic=topic, subtopic=subtopic)
            add_topic.save()
            response_msg = 'Topic successfully created'
            response_type = 'success'
        data = {
            'response_msg': response_msg,
            'response_type': response_type
        }
        return JsonResponse(data, status=201)


def api_create_topic(request):

    response_msg = ''
    if request.method == 'POST':
        topic = request.POST.get('topic')
        admin = request.user.username
        payment_mode = request.POST.get('payment_mode')
        payment_code = request.POST.get('payment_code')
        subtopic = request.POST.get('subtopic')
        discussion_code = create_random()
        description = request.POST.get('description')
        question = request.POST.get('question')
        discussioncode = discussion_code
        create_time = timezone.now()

        if topic is None or topic == '':
            response_msg = 'The topic field is empty'

        elif admin is None or admin == '':
            response_msg = 'The admin field is empty'

        elif payment_mode is None or payment_mode == '':
            response_msg = 'The mode of payment is not given'

        elif payment_code is None or payment_code == '':
            response_msg = 'You have not provide your payment code'

        elif subtopic is None or subtopic == '':
            response_msg = 'Select a subtopic please'

        elif description is None or description == '':
            response_msg = 'Enter a nice description for your query'

        elif question is None or question == '':
            response_msg = 'Every good topic has a question supporting it'

        else:
            create_query = Create(topic=topic, admin=admin, paymentMode=payment_mode, paymentCode=payment_code,
                                  subtopic=subtopic, description=description, question=question,
                                  discussionCode=discussioncode, createTime=create_time)
            create_query.save()
            str_ = '%s was successfully created' % discussion_code
            response_msg = str_
            # url = '/discuzz/%s' % discussion_code
            # return redirect(url)

        data = {
            'response': response_msg
        }
        return JsonResponse(data)


def api_all_queries(request, *args, **kwargs):
    objects = Create.objects.all()

    data_for_front_end = [{"id": obj.id,
                           "topic": obj.topic,
                           "admin": obj.admin,
                           "paymentMode": obj.paymentMode,
                           "paymentCode": obj.paymentCode,
                           "subtopic": obj.subtopic,
                           "description": obj.description,
                           "question": obj.question,
                           "discussionCode": obj.discussionCode,
                           "createTime": obj.createTime} for obj in objects]

    data = {
        "response": data_for_front_end
    }

    return JsonResponse(data, status=200)


def base(request):
    return render(request, "base.html")


def api_like(request, reply_id):
    reply = get_object_or_404(Discuzz, id=reply_id)

    id_ = reply_id
    if request.method == 'POST':
        if reply.dislikes.filter(username=request.user).exists():
            reply.likes.add(request.user)
            reply.dislikes.remove(request.user)
            liked = 'liked'
            class_ = 'thumbs-up'
            stroked = 'false'

        elif reply.likes.filter(username=request.user).exists():
            reply.likes.remove(request.user)
            liked = 'unliked'
            class_ = 'thumbs-up'
            stroked = 'true'
        else:
            reply.likes.add(request.user)
            liked = 'liked'
            class_ = 'thumbs-up'
            stroked = 'false'

        data = {
            'response': liked,
            'class_': class_,
            'stroked': stroked,
            'id': id_
        }
        return JsonResponse(data, status=201)


def api_dislike(request, reply_id):

    reply = get_object_or_404(Discuzz, id=reply_id)

    id_ = reply_id
    if request.method == 'POST':
        if reply.likes.filter(username=request.user).exists():
            reply.dislikes.add(request.user)
            reply.likes.remove(request.user)
            disliked = 'disliked'
            class_ = 'thumbs-up'
            stroked = 'false'

        elif reply.dislikes.filter(username=request.user).exists():
            reply.dislikes.remove(request.user)
            disliked = 'undisliked'
            class_ = 'thumbs-up'
            stroked = 'true'
        else:
            reply.dislikes.add(request.user)
            disliked = 'disliked'
            class_ = 'thumbs-up'
            stroked = 'false'

        data = {
            'response': disliked,
            'class_': class_,
            'stroked': stroked,
            'id': id_
        }
        return JsonResponse(data, status=201)


@login_required(login_url='login')
def home(request):
    # if request.method == "POST":
    #     email = request.POST.get('email')
    #     update = request.POST.get('updatemsg')
    #     updatetime = timezone.now()
    #     if email == '' or email is None:
    #         messages.error(request, 'Email field is empty')
    #     elif update is None or update == '':
    #         messages.error(request, 'Message field is required')
    #     else:
    #         send_email = SendEmail(email=email, update=update, updateTime=updatetime)
    #         send_email.save()
    #         return redirect('home')

    # if request.method == "POST":
    #     topic = request.POST.get('topic')
    #     subtopic = request.POST.get('subtopic')
    #
    #     if topic == '' or topic is None:
    #         messages.error(request, 'topic field is empty')
    #     elif subtopic is None or subtopic == '':
    #         messages.error(request, 'Subtopic field is required')
    #     else:
    #         add_topic = Topic(topic=topic, subtopic=subtopic)
    #         add_topic.save()
    #         messages.success(request, 'Topic added successfully')
    #         return redirect('home')

    discussions = Create.objects.all().order_by("-createTime")
    all_replies = Discuzz.objects.all()
    context = {
        "discussions": discussions,
        "all_replies": all_replies,
    }
    return render(request, "my_app/home.html", context)


@unauthenticated_user
def user_login(request, *args, **kwargs):
    print('SOME MORE DATA IS', request.GET.get('next'))
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

    return render(request, "my_app/account/login.html")


@unauthenticated_user
def signup(request):
    form = UserSignUp()
    errors = []
    if request.method == "POST":
        form = UserSignUp(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')

        elif not form.is_valid():
            errors.append(form.error_messages)
            messages.error(request, errors)

    return render(request, "my_app/account/signup.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    your_discussions = Create.objects.all().order_by('-createTime')
    y_c = Discuzz.objects.all().order_by('-reply_time')
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


def api_topic_subtopic_render(request):
    topics1 = Create.objects.all()
    topics2 = Topic.objects.all()

    topics_dic = ['Engineering', 'Education']
    subtopics_dic = ['E eng', 'SomeSub']

    for topic in topics1:
        topics_dic.append(topic.topic)
        subtopics_dic.append(topic.subtopic)

    for topic in topics2:
        topics_dic.append(topic.topic)
        subtopics_dic.append(topic.subtopic)

    print('THE TOPICS ARE', topics_dic)
    print('THE SUB-TOPICS ARE', topics_dic)

    data = {
        'response': 'fetched the topics and subtopics',
        'topics': topics_dic,
        'subtopics': subtopics_dic
    }
    return JsonResponse(data)


@login_required(login_url='login')
def create(request):
    topics1 = Create.objects.all()
    topics2 = Topic.objects.all()
    context = {
        'topics1': topics1,
        'topics2': topics2

    }

    if request.method == 'POST':
        topic = request.POST.get('topic')
        admin = request.user.username
        payment_mode = request.POST.get('payment_mode')
        payment_code = request.POST.get('payment_code')
        subtopic = request.POST.get('subtopic')
        discussion_code = create_random()
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
            str_ = '%s was successfully created' % discussion_code
            messages.success(request, str_)
            url = '/discuzz/%s' % discussion_code
            return redirect(url)

    return render(request, 'my_app/motion/create.html', context)


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
            discuzz = None

    except Create.DoesNotExist:
        disc_name = None
        messages.error(request, "The Discussion ID does not exist, Please check and try again")
        return render(request, 'my_app/help/not-found.html')


def reply_api(request, discussion_details, *args, **kwargs):
    disc_name = Create.objects.get(discussionCode=discussion_details)
    print('THE KWARGS ARE', kwargs)
    username = request.user.username
    discussioncode = disc_name.discussionCode

    response_msg = ''
    response_type = ''

    if request.method == 'POST':
        reply = html.escape(request.POST.get('reply'))
        if reply == '' or reply is None:
            response_msg = 'reply field is empty'
            response_type = 'danger'
        else:
            replytime = timezone.now()
            reply_query = Discuzz(discussion_code=discussioncode, reply=reply, username=username, reply_time=replytime)
            reply_query.save()
            response_msg = 'reply successful'
            response_type = 'success'

        data = {
            'response_msg': response_msg,
            'response_type': response_type
        }
        return JsonResponse(data, status=201)


def progpage(request):
    return render(request, 'my_app/motion/prog.html')


# pk = primary key, so as to identify the primary key that is the ID to add a like to it
def like(request):
    reply = get_object_or_404(Discuzz, id=request.POST.get('like'))
    url_ = '/discuzz/%s#%s' % (reply, reply.id)

    if reply.dislikes.filter(username=request.user).exists():
        reply.likes.add(request.user)
        reply.dislikes.remove(request.user)

    elif reply.likes.filter(username=request.user).exists():
        reply.likes.remove(request.user)
    else:
        reply.likes.add(request.user)
    data = {
        'response': 'success'
    }
    # return JsonResponse(data, status=200)


def dislike(request):
    reply = get_object_or_404(Discuzz, id=request.POST.get('dislike'))
    url_ = '/discuzz/%s#%s' % (reply, reply.id)
    print("THis is the reply code", reply.reply)
    if reply.likes.filter(username=request.user).exists():
        reply.dislikes.add(request.user)
        reply.likes.remove(request.user)
    elif reply.dislikes.filter(username=request.user).exists():
        reply.dislikes.remove(request.user)

    else:
        reply.dislikes.add(request.user)
    return redirect(url_)


def comments(request):
    reply = get_object_or_404(Discuzz, id=request.POST.get('comment'))
    url_ = '/discuzz/%s' % reply
    print("THis is the reply code", reply.reply)
    comment_to_reply = 'I love coding'
    comment = '%s,%s' % (request.user, comment_to_reply)
    reply.comments.add(request.user)
    return redirect(url_)


@login_required(login_url='login')
def c19(request):
    return render(request, 'my_app/news/c19.html')


@login_required(login_url='login')
def wnews(request):
    return render(request, 'my_app/news/wnews.html')


def create_random():
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

    code = '%dY%d%s%d%dand%du%dz%dZ%d%dDiscuzz%d%da' % (
        num7, num8, 'TALK', num6, num7, num10, num1, num2, num3, num4, num5,
        num9)
    return code
