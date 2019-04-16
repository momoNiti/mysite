# from django.http import HttpResponse

from django.shortcuts import render


# Create your views here.
from polls.models import Poll, Question, Answer
from polls.forms import PollForm
def index(request):
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

        # title = request.POST.get('title')
        # question_list = request.POST.getlist('questions[]')
        pass

    else:
        # answer = request.GET.get('answer')
        # answer_list = request.GET.getlist('answer[]')
        form = PollForm()
    context = {'form': form}
    return render(request, 'polls/create.html', context=context)