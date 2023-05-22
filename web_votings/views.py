from django.shortcuts import render
import sqlite3 as lite
import sys
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.decorators.csrf import csrf_exempt

from web_votings.models import AllVotings, Answers, UsersAnswers, Complaint
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def get_list_of_votings(request):
    context = {}
    context['votings'] = AllVotings.objects.all()
    return render(request, 'list.html', context)

@login_required
def show_voitings(request, id):
    #vote_id = id #request.GET.get('id')
    context = {}
    context['votings'] = AllVotings.objects.all()
    for i in context['votings']:
        if i.id == id:
            context['answers'] = Answers.objects.filter(question=i)
            context['voting'] = i
    for i in UsersAnswers.objects.filter(user=request.user):
        if i.answer in context['answers']:
            return HttpResponseRedirect(f"/rezults/{context['voting'].id}")
    return render(request, 'vote.html', context)

@login_required
def show_rezs(request, id):
    context = {}
    context['answers'] = list()
    sum = int(0)
    voting_answers = Answers.objects.filter(question=AllVotings.objects.filter(id=id)[0])
    for i in voting_answers:
        sum += i.number_of_p_chosen
    for i in voting_answers:
        context['answers'].append(str(i.answer_variant) + "    " + str(round(i.number_of_p_chosen / sum * 100, 1)))
    context['voting'] = AllVotings.objects.filter(id=id)[0]
    return render(request, 'results.html', context)


@login_required
def process_vote(request):
    check_for_voted = False
    context = {}
    context['answers'] = list()
    exact_answer = list()
    ans_ids = request.POST.getlist("answer")
    for i in ans_ids:
        exact_answer.append(Answers.objects.filter(id=int(i))[0])
    user_answer = list()
    for i in UsersAnswers.objects.filter(user=request.user):
        user_answer.append(i)

    for i in user_answer:
        if exact_answer[0].question == i.answer.question:
            check_for_voted = True
            break
    voting = exact_answer[0].question
    if not check_for_voted:
        for i in exact_answer:
            print(i.id)
            i.number_of_p_chosen += 1
            i.save()
            record = UsersAnswers(answer=i, user=request.user)
            record.save()
    # _______________________
    sum = int(0)
    voting_answers = Answers.objects.filter(question=voting)
    for i in voting_answers:
        sum += i.number_of_p_chosen
    for i in voting_answers:
        context['answers'].append(str(i.answer_variant) + "    " + str(round(i.number_of_p_chosen / sum * 100, 1)))
    context['voting'] = voting
    return render(request, 'results.html', context)
@login_required
def show_create_voting(request):
    return render(request, "create_voting_dinamic.html")

@login_required
def create_voting(request):
    name = request.POST["name"]
    description = request.POST["description"]
    type = request.POST["type"]
    if type == 'Выбор одного варианта':
        type = 1
    else:
        type = 2
    status = request.POST['mytext']
    answers = request.POST.getlist("answer")
    number_of_questions = len(answers)
    creator_id = request.user
    vote_create = AllVotings(name=name, description=description, type=type, creator_id=creator_id, number_of_questions=number_of_questions, status=status)
    vote_create.save()
    for i in answers:
        answer = Answers(answer_variant=i, question=vote_create, number_of_p_chosen=0)
        answer.save()

    return redirect('index')

@login_required
def show_edit_voting(request, id):
    context = {}
    if AllVotings.objects.filter(id=id)[0].creator_id == request.user and AllVotings.objects.filter(id=id)[0].status != 1:
        context['voting'] = AllVotings.objects.filter(id=id)[0]
        context['answersl'] = Answers.objects.filter(question=context['voting'])[0]
        context['answers'] = list()
        for i in Answers.objects.filter(question=context['voting']):
            if i != context['answersl']:
                context['answers'].append(i)
        return render(request, 'edit_voting.html', context)
    else:
        return redirect('index')

@login_required
def edit_voting(request, id):
    voting = AllVotings.objects.filter(id=id)[0]
    answers = Answers.objects.filter(question=voting)
    if voting.creator_id == request.user and voting.status != 1:
        voting.name = request.POST['name']
        voting.description = request.POST['description']
        type = request.POST["type"]
        if type == 'Выбор одного варианта':
            voting.type = 1
        else:
            voting.type = 2
        voting.number_of_questions = len(request.POST.getlist('answer'))
        voting.status = request.POST['mytext']
        voting.save()
        for i in answers:
            i.delete()
        for i in request.POST.getlist('answer'):
            answer = Answers(answer_variant=i, question=voting, number_of_p_chosen=0)
            answer.save()
    return redirect('index')




@login_required
def create_voting1(request):
    name = request.POST["name"]
    description = request.POST["description"]
    type = request.POST["type"]
    if type == 'Выбор одного варианта':
        type = 1
    else:
        type = 2

    number_of_questions = int(request.POST["number_of_questions"])
    creator_id = request.user
    vote_create = AllVotings(name=name, description=description, type=type, creator_id=creator_id, number_of_questions=number_of_questions)
    print(name, description, type, number_of_questions)
    vote_create.save()
    number = [i+1 for i in range(number_of_questions)]
    context = {'number': number, "voting_id": vote_create.id}
    return render(request, "creation_voting2.html", context)

@login_required
def create_voting2(request, id):
    answers = request.POST.getlist("answer")
    for i in answers:
        answer = Answers(answer_variant=i, question=AllVotings.objects.filter(id=id)[0], number_of_p_chosen=0)
        answer.save()
    return HttpResponseRedirect("/")


@login_required
def show_profile(request):
    context = {}
    context['user'] = request.user
    context['votings'] = AllVotings.objects.filter(creator_id=request.user)
    context['complaints'] = Complaint.objects.filter(creator=request.user)
    answers = set()
    for i in UsersAnswers.objects.filter(user=request.user):
        answers.add(i.answer.question)
    context['my_votings'] = list(answers)
    return render(request, "profile.html", context)

@login_required
def show_make_complaint(request, id):
    context = {'voting_id': id}
    return render(request, 'complaint.html', context)

def make_complaint(request, id):
    check_for_complained = False
    for i in Complaint.objects.filter(vote=AllVotings.objects.filter(id=id)[0]):
        if i.creator == request.user:
            check_for_complained = True
            break
    if not check_for_complained:
        theme = request.POST['name']
        descr = request.POST['description']
        voting = AllVotings.objects.filter(id=id)[0]
        complaint = Complaint(theme=theme, desc=descr, creator=request.user, vote=voting, stat=0)
        complaint.save()
    return redirect('index')

def show_complaint(request, id):
    if Complaint.objects.filter(id=id)[0].creator != request.user:
        return redirect('index')
    else:
        context = {'complaint': Complaint.objects.filter(id=id)[0]}
        return render(request, 'my_complaint.html', context)

@login_required
def show_change_profile(request):
    context = {'user':request.user}
    return render(request, "change_profile.html")

@login_required
def change_profile(request):
    profile = User.objects.get(username=request.user.username)
    profile.username = request.POST.get("nickname")
    profile.first_name = request.POST.get("firstname")
    profile.last_name = request.POST.get("lastname")
    profile.email = request.POST.get("mail")
    profile.save()
    return redirect("index")

@csrf_exempt
def saveandopen(request):
    print(request.POST)
    return redirect("index")

def get_main_page(request):
    return render(request, 'index.html')
