# from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Count

# Create your views here.
from polls.models import Poll, Question, Answer, Comment, Profile
from polls.forms import PollForm, CommentForm, ChangePasswordForm, RegisterForm

def index(request):
    print(request.user)
    print(request.user.email)
    # poll_list = Poll.objects.filter(del_flag=False, id__gt=2)
    poll_list = Poll.objects.all()

    for poll in poll_list:
        question_count = Question.objects.filter(poll_id=poll.id).count
        poll.question_count = question_count


    context = {
        'page_title': 'My Polls',
        'poll_list': poll_list
    }
    return render(request, template_name='polls/index.html', context=context)

@login_required
@permission_required('polls.view_poll') #ใส่ได้มากกว่า 1
def detail(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    # print(request.GET)
    if request.method == 'POST':
        for question in poll.question_set.all():
            name = 'choice' + str(question.id)
            choice_id = request.POST.get(name)
            if choice_id:
                try:
                    ans = Answer.objects.get(question_id=question.id)
                    ans.choice_id = choice_id
                    ans.save()
                except Answer.DoesNotExist:
                    Answer.objects.create(
                        choice_id = choice_id,
                        question_id = question.id
                    )
        # print(choice_id)
    return render(request, 'polls/detail.html', {'poll' : poll})

@login_required
@permission_required('polls.add_poll') #ใส่ได้มากกว่า 1
def create(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            poll = Poll.objects.create(
                title = form.cleaned_data.get('title'),
                start_date = form.cleaned_data.get('start_date'),
                end_date = form.cleaned_data.get('end_date'),
            )
            for i in range(1, form.cleaned_data.get('no_questions')+1):
                Question.objects.create(
                    text = 'QQQ'+str(i),
                    type = '01',
                    poll = poll
                )
    else:
        form = PollForm()
    context = {'form': form}
    return render(request, 'polls/create.html', context=context)

def comment(request, poll_id):
    if (request.method == "POST"):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                title = form.cleaned_data.get('title'),
                body = form.cleaned_data.get('body'),
                email = form.cleaned_data.get('email'),
                tel = form.cleaned_data.get('tel'),
                poll_id = poll_id
            )
            comment.save()
    else:
        form = CommentForm()
    context = {'form': form}
    context['poll_id'] = poll_id
    return render(request, template_name="polls/comment.html", context=context)

def my_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)#แค่เช็คแต่ไม่ได้สร้าง session
        if user:
            login(request, user) #สร้าง session
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            context['usernae'] = username
            context['password'] = password
            context['error'] = "Wrong username or Password !"
    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
    return render(request, template_name="polls/login.html", context=context)

def my_logout(request):
    logout(request)
    return redirect('login')

@login_required
def change_password(request):
    context = {}
    if (request.method == "POST"):
        form = ChangePasswordForm(request.POST)
        current_password = request.POST.get('old_password')
        user = authenticate(request, username=request.user.username, password=current_password)
        if user and form.is_valid():
            new_password = form.cleaned_data.get('new_password'),
            u = User.objects.get(username = request.user)
            u.set_password(new_password[0])
            u.save()
        elif not user:
            context['myerror'] = "Passwordเก่าไม่ถูกต้อง"

    else:
        form = ChangePasswordForm()
    context['form'] = form
    return render(request, template_name="polls/change_password.html", context=context)

def register(request):
    if (request.method == "POST"):
        form = RegisterForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(
                form.cleaned_data.get('username'),
                form.cleaned_data.get('email'),
                form.cleaned_data.get('password')
            )

            profile = Profile.objects.create(
                line_id = form.cleaned_data.get('line_id'),
                facebook = form.cleaned_data.get('facebook'),
                gender = form.cleaned_data.get('gender'),
                birthdate = form.cleaned_data.get('birthdate'),
                user_id = u.id
            )
            profile.save()
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, template_name="polls/register.html", context=context)