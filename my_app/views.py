from urllib.parse import quote_plus

from django.db import transaction
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone, dateformat
from rest_framework.views import APIView

from .models import *
from .decorators import *
from django.utils import safestring, html

from django.http import JsonResponse, Http404

from random import random, seed, randint

from django.views.decorators.cache import cache_page

import json

from .rest_serializers import DiscuzzReplySerializer, DiscuzzQuestionSerializer, UserExtensionSerializer,\
    CommentSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.views import make_notification


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


def my_admin(request):
    if request.user.is_superuser:

        all_discussions = Create.objects.all()
        all_emails = SendEmail.objects.all()
        all_replies = Discuzz.objects.all()
        all_topics = Topic.objects.all()
        all_comments = Comment.objects.all()

        total_users = User.objects.all().count()

        staff_users = User.objects.filter(is_staff=True).count()
        superuser_users = User.objects.filter(is_superuser=True).count()

        active_users = User.objects.filter(is_active=True).count()
        inactive_users = total_users - active_users

        total_emails = SendEmail.objects.all().count()
        read_emails = SendEmail.objects.filter(status='read').count()
        unread_emails = SendEmail.objects.filter(status='unread').count()

        total_topics = Topic.objects.all().count()
        visible_topics = Topic.objects.filter(status='visible').count()
        hidden_topics = Topic.objects.filter(status='hidden').count()

        total_questions = Create.objects.all().count()
        visible_questions = Create.objects.filter(status='visible').count()
        hidden_questions = Create.objects.filter(status='hidden').count()

        total_replies = Discuzz.objects.all().count()
        visible_replies = Discuzz.objects.filter(status='visible').count()
        hidden_replies = Discuzz.objects.filter(status='hidden').count()

        total_comments = Comment.objects.all().count()
        visible_comments = Comment.objects.filter(status='visible').count()
        hidden_comments = Comment.objects.filter(status='hidden').count()

        my_questions = Create.objects.filter(admin=request.user).count()

        replies_count_to_various_quizes = []
        comments_count_to_various_replies = []

        for o in all_discussions:
            replies = Discuzz.objects.filter(discussion_code=o).count()
            query_replies = {
                'id': o.discussionCode,
                'replies': replies
            }
            replies_count_to_various_quizes.append(query_replies)

        for o in all_replies:
            full_reply = Discuzz.objects.get(id=o.id)
            comments_count = Comment.objects.filter(commented_to=full_reply).count()
            query_replies = {
                'id': o.id,
                'comments': comments_count
            }
            comments_count_to_various_replies.append(query_replies)

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
            'total_users': total_users,
            'superuser_users': superuser_users,
            'staff_users': staff_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'all_discussions': all_discussions,
            'all_emails': all_emails,
            'all_replies': all_replies,
            'all_topics': all_topics,
            'all_comments': all_comments,
            'reply_count': replies_count_to_various_quizes,
            'comment_count': comments_count_to_various_replies,
            'total_emails': total_emails,
            'read_emails': read_emails,
            'unread_emails': unread_emails,
            'total_topics': total_topics,
            'visible_topics': visible_topics,
            'hidden_topics': hidden_topics,
            'total_questions': total_questions,
            'visible_questions': visible_questions,
            'hidden_questions': hidden_questions,
            'total_replies': total_replies,
            'visible_replies': visible_replies,
            'hidden_replies': hidden_replies,
            'total_comments': total_comments,
            'visible_comments': visible_comments,
            'hidden_comments': hidden_comments,
            'my_questions': my_questions,
            'page': 'Discuzz admin dashboard',
            'my_pic': pic,
        }
        return render(request, 'my_app/admin/discuzzadmin.html', context)

    else:
        return redirect('/')


def api_my_admin(request):
    all_discussions = Create.objects.all()
    all_emails = SendEmail.objects.all()
    all_replies = Discuzz.objects.all()
    all_topics = Topic.objects.all()
    all_comments = Comment.objects.all()

    total_users = User.objects.all().count()

    staff_users = User.objects.filter(is_staff=True).count()
    superuser_users = User.objects.filter(is_superuser=True).count()

    active_users = User.objects.filter(is_active=True).count()
    inactive_users = total_users - active_users

    total_emails = SendEmail.objects.all().count()
    read_emails = SendEmail.objects.filter(status='read').count()
    unread_emails = SendEmail.objects.filter(status='unread').count()

    total_topics = Topic.objects.all().count()
    visible_topics = Topic.objects.filter(status='visible').count()
    hidden_topics = Topic.objects.filter(status='hidden').count()

    total_questions = Create.objects.all().count()
    visible_questions = Create.objects.filter(status='visible').count()
    hidden_questions = Create.objects.filter(status='hidden').count()

    total_replies = Discuzz.objects.all().count()
    visible_replies = Discuzz.objects.filter(status='visible').count()
    hidden_replies = Discuzz.objects.filter(status='hidden').count()

    total_comments = Comment.objects.all().count()
    visible_comments = Comment.objects.filter(status='visible').count()
    hidden_comments = Comment.objects.filter(status='hidden').count()

    replies_count_to_various_quizes = []
    comments_count_to_various_replies = []

    for o in all_discussions:
        replies = Discuzz.objects.filter(discussion_code=o).count()
        query_replies = {
            'id': o.discussionCode,
            'replies': replies
        }
        replies_count_to_various_quizes.append(query_replies)

    for o in all_replies:
        full_reply = Discuzz.objects.get(id=o.id)
        comments_count = Comment.objects.filter(commented_to=full_reply).count()
        query_replies = {
            'id': o.id,
            'comments': comments_count
        }
        comments_count_to_various_replies.append(query_replies)

    context = {
        'total_users': total_users,
        'superuser_users': superuser_users,
        'staff_users': staff_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'reply_count': replies_count_to_various_quizes,
        'comment_count': comments_count_to_various_replies,
        'total_emails': total_emails,
        'read_emails': read_emails,
        'unread_emails': unread_emails,
        'total_topics': total_topics,
        'visible_topics': visible_topics,
        'hidden_topics': hidden_topics,
        'total_questions': total_questions,
        'visible_questions': visible_questions,
        'hidden_questions': hidden_questions,
        'total_replies': total_replies,
        'visible_replies': visible_replies,
        'hidden_replies': hidden_replies,
        'total_comments': total_comments,
        'visible_comments': visible_comments,
        'hidden_comments': hidden_comments
    }
    data = json.dumps(context)
    return JsonResponse(context, status=200)


def read_reply_email_message(request, _id):
    type_ = request.GET.get('type')
    email_ = SendEmail.objects.get(id=_id)
    if type_ == 'read':
        email_.status = 'read'
        email_.save()
    elif type_ == 'unread':
        email_.status = 'unread'
        email_.save()
    elif type_ == 'reply':
        email_.state = 'replied'
        email_.save()
        print('REPLIED SUCCESSFULLY')

    return HttpResponseRedirect('/myadmin')


def delete_reply_comment_topic_question(request, _id):
    type_ = request.GET.get('type')
    if type_ == 'topic':
        Topic.objects.get(id=_id).delete()
    elif type_ == 'reply':
        Discuzz.objects.get(id=_id).delete()
    elif type_ == 'comment':
        Comment.objects.get(id=_id).delete()
    elif type_ == 'question':
        Create.objects.get(id=_id).delete()
    return HttpResponseRedirect("/myadmin")


def hide_show_reply_comment_topic_question(request, _id):
    type_ = request.GET.get('type')
    status = request.GET.get('status')
    if type_ == 'topic':
        topic = Topic.objects.get(id=_id)
        if status == 'hide':
            topic.status = 'hidden'
            topic.save()
        elif status == 'show':
            topic.status = 'visible'
            topic.save()

    if type_ == 'question':
        question = Create.objects.get(id=_id)
        if status == 'hide':
            question.status = 'hidden'
            question.save()
        elif status == 'show':
            question.status = 'visible'
            question.save()

    if type_ == 'reply':
        reply = Discuzz.objects.get(id=_id)
        if status == 'hide':
            reply.status = 'hidden'
            reply.save()
        elif status == 'show':
            reply.status = 'visible'
            reply.save()
    elif type_ == 'comment':
        comment = Comment.objects.get(id=_id)
        if status == 'hide':
            comment.status = 'hidden'
            comment.save()
        elif status == 'show':
            comment.status = 'visible'
            comment.save()

    return HttpResponseRedirect("/myadmin")


def api_discuzz_details(request, discussion_details, *args, **kwargs):
    #
    objects = Discuzz.objects.all()
    list_all_replies = []
    for o in objects:
        if o.discussion_code.discussionCode == discussion_details:
            list_all_replies.append(o)

    staff_for_frontend = [{"id": obj.id,
                           "discussionCode": obj.discussion_code.discussionCode,
                           "username": obj.username.username,
                           "pic": obj.username.userextension.profile_pic.url,
                           "reply": obj.reply,
                           "likes": obj.likes.count(),
                           "dislikes": obj.dislikes.count(),
                           "comments": Comment.objects.filter(commented_to=obj).count(),
                           "reply_time": obj.reply_time
                           } for obj in list_all_replies]

    data = {
        "response": staff_for_frontend,
        "length": len(list_all_replies)
    }

    return JsonResponse(data, safe=False)


def api_create_quiz(request):
    response_msg = ''
    if request.method == 'POST':
        topic = request.POST.get('topic')
        admin = request.user
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


def base(request):
    return render(request, "base.html")


def about(request):
    context = {
        'page': 'About us',
    }
    return render(request, 'my_app/help/about.html', context)


def contact(request):
    context = {
        'page': 'Contact us',
    }

    return render(request, 'my_app/help/contact.html', context)


@login_required(login_url='login')
def join(request):
    context = {
        'page': 'Create or Join a group discussion',
    }
    return render(request, 'my_app/motion/join.html', context)


@login_required(login_url='login')
def join_via_code(request):
    if request.method == "POST":
        join_disc_id = request.POST.get('discussionId')

        if join_disc_id is None or join_disc_id == '':
            messages.error(request, "An error occurred here")

        else:
            try:
                disc_name = get_object_or_404(Create, discussionCode=join_disc_id)
            except Create.DoesNotExist:
                disc_name = None
                return render(request, 'my_app/help/not-found.html')

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
        'topics2': topics2,
        'page': 'Create a topic',
    }

    if request.method == 'POST':
        topic = request.POST.get('topic')
        admin = request.user
        subtopic = request.POST.get('subtopic')
        discussion_code = create_random()
        description = request.POST.get('description')
        question = request.POST.get('question')
        discussioncode = discussion_code
        create_time = timezone.now()

        if topic is None or topic == '':
            messages.error(request, 'Topic field is empty')

        elif subtopic is None or subtopic == '':
            messages.error(request, 'The Sub Topic field is empty')

        elif description is None or description == '':
            messages.error(request, 'The description field is empty')

        elif question is None or question == '':
            messages.error(request, 'The question field is empty')

        else:
            create_query = Create(topic=topic, admin=admin,
                                  subtopic=subtopic, description=description, question=question,
                                  discussionCode=discussioncode, createTime=create_time)
            create_query.save()

            my_friends = request.user.userextension.friends.all()

            for other_user in my_friends:
                make_notification(request.user, other_user, 'question', 'questions field', discussioncode, topic,
                                  question)
                other_user.save();

            str_ = '%s was successfully created' % discussion_code
            messages.success(request, str_)
            url = '/discuzz/%s' % discussion_code
            return redirect(url)

    return render(request, 'my_app/motion/create.html', context)


@cache_page(60 * 15)
@login_required(login_url='login')
def discuzz(request, discussion_details):
    disc_name = get_object_or_404(Create, discussionCode=discussion_details)
    if disc_name:
        question_serializer = DiscuzzQuestionSerializer(disc_name, many=False)
        question_data = question_serializer.data

        syntax_topics = Syntax.objects.all()
        software_topics = []
        for topic in syntax_topics:
            software_topics.append(topic.topic)

        context = {
            'my_friends': request.user.userextension.friends.all(),
            'page': discussion_details,
            'question_data': question_data
        }

        if question_data['topic'] in software_topics:
            return render(request, 'my_app/motion/prog.html', context)
        else:
            return render(request, 'my_app/motion/discuzz.html', context)
    else:
        return render(request, 'my_app/help/not-found.html')


def participants(request, discussion_code):
    disc_code = Create.objects.get(discussionCode=discussion_code)
    all_replies = Discuzz.objects.filter(discussion_code=disc_code)
    part = []
    for reply in all_replies:
        if reply.username is None:
            pass
        else:
            if reply.username.username not in part:
                part.append(reply.username.username)
            else:
                pass

    data = {
        'data': part
    }
    return JsonResponse(data, status=200)


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


def trial_loader(request):
    return render(request, 'my_app/motion/trial.html')


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


def comments_api(request, reply_id):
    print('THE DISCUSSION DETAILS ARE and the id is ' + reply_id)

    reply = Discuzz.objects.get(id=reply_id)
    id_ = reply_id
    discussioncode = reply.discussion_code

    if request.method == 'POST':
        commented_by = request.user
        commented_to = reply
        comment = request.POST.get('comment')
        commented_on = timezone.now()
        comment_query = Comment(
            commented_to=commented_to,
            commented_by=commented_by,
            comment=comment,
            commented_on=commented_on
        )
        comment_query.save()
        url = '/discuzz/%s' % discussioncode
        data = {
            'user': commented_by.username,
            'comment': comment
        }
        return JsonResponse(data, status=200)


def all_comments_api(request):
    disc_code = request.GET.get('code')
    disc_id = request.GET.get('id')
    query = Discuzz.objects.get(id=disc_id)
    print('THE QUERY IS ', query)
    comms = Comment.objects.filter(commented_to=query)
    print('THE COMMENTS FOR THIS QUERY IS ', comms)

    all_comments = Comment.objects.all()
    # print(all_comments)
    data_for_front_end = [{"id": comment.id,
                           "commented_by": comment.commented_by.username,
                           "commented_to": comment.commented_to.id,
                           "comment": comment.comment,
                           "commented_on": comment.commented_on} for comment in all_comments]

    data = {
        'all_comments': data_for_front_end,
        'status': 201
    }
    return JsonResponse(data)


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


def email(request):
    all_emails = SendEmail.objects.all()

    context = {
        'all_emails': all_emails,
        'page': 'Emails'
    }

    return render(request, 'my_app/news/emails.html', context)


class quiz_api(APIView):

    def get(self, format=None):
        quizes = Create.objects.all()  # .order_by('createTime')
        serializer = DiscuzzQuestionSerializer(quizes, many=True)

        return Response(serializer.data)


@api_view(['GET'])
def quiz_api_single(request, id_):
    disc_name = get_object_or_404(Create, id=id_)
    question_serializer = DiscuzzQuestionSerializer(disc_name, many=False)
    question_data = question_serializer.data

    return Response(question_data)


@api_view(['GET'])
def reply_api(request):
    replies = Discuzz.objects.all()
    serializer = DiscuzzReplySerializer(replies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def comment_api(request):
    comments_ = Comment.objects.all()
    serializer = CommentSerializer(comments_, many=True)
    return Response(serializer.data)
