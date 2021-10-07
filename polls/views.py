from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse

def index(request):
    # Get the information from the database
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
   
    
    # The dictionary values used in the template
    context = {
        'latest_question_list' : latest_question_list,
    }

    # Render the webpage and return it
    return HttpResponse(render(request, 'polls/index.html', context))

def detail(request, question_id):

    # Looks for the specified object, gets a 404 if it does not exist
    question = get_object_or_404(Question, pk=question_id)

    # If you want a list rather than object use:
    # get_list_or_404()

    # Dictionary for render
    context = {
        'question': question,
    }
    return HttpResponse(render(request, 'polls/detail.html', context))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        # Sends the redirect after the post
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




