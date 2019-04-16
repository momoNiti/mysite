# from django.http import HttpResponse

from django.shortcuts import render


# Create your views here.
from polls.models import Poll, Question, Answer
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
    ans = {}
    if request.method == "GET":
        answer = request.GET
        for key, value in answer.items():
            temp = value.split('_')
            ans[temp[0]] = temp[1]
        # print(ans)
        for question, choice in ans.items():
            ans_model = Answer(choice_id=choice, question_id=question)
            ans_model.save()
    return render(request, 'polls/detail.html', {'poll' : poll})

