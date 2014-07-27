import json

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_GET, require_POST

from confirmations import send_email_with_score
from users_.models import UserProfile, Tests, Questions, Answers

# Create your views here.

def admin_required(function):
    @login_required
    def wrapp(request, *args, **kw):
        if request.user.get_profile().userlvl == 0:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect('/')
    return wrapp

def user_required(function):
    @login_required
    def wrapp(request, *args, **kw):
        if request.user.get_profile().userlvl == 1:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect('/')
    return wrapp

def discriminate_user(function):
    @login_required
    def wrapp(request, *args, **kw):
        return function(request, request.user.get_profile().userlvl)
    return wrapp

@discriminate_user
def profile(request, userlvl):
    if userlvl == 0:
        template = 'admin.html'
        tests = Tests.objects.all()
    else:
        template = 'user.html'
        tests = [test for test in Tests.objects.all() if
                 len(test.dict()['questions']) > 0]
    ctx = {
        'tests':tests,
    }
    return render_to_response(template, ctx,
                              context_instance=RequestContext(request))

def welcome(request):
    c = Context()
    return render_to_response('welcome.html',c)

def register(request):
    success = None
    if request.method=='POST':
        password = make_password(request.POST['password'])
        try:
            user = User.objects.get(username=request.POST['username'])
            success = "User with this username already exist!"
        except User.DoesNotExist:
            user = User(username=request.POST['username'], password=password,
                        is_superuser=False, email=request.POST['email'])
            userprofile = UserProfile(user=user, userlvl=1)
            userprofile.save()
            success = "U can now log onto ur account"
    c = Context(dict({'success':success}))
    c.update(csrf(request))
    return render_to_response('register.html',c)

#------------------------------ Admin section --------------------------------
@require_POST
@admin_required
def new_test(request):
    data = json.loads(request.body)
    title = data['new_test'].strip()
    if len(title) == 0:
        message = "Please insert correct data"
        new_test_id = None
        success = False
    else:
        try:
            new_test = Tests.objects.get(title=title)
            message = "Test with this title already exist"
            success = False
        except Tests.DoesNotExist:
            new_test = Tests(title=data['new_test'])
            new_test.save()
            new_test_id = new_test.id
            message = "Test %s added"%title
            success = True
    return HttpResponse(json.dumps(dict({'success':success,
                                         'test_id':new_test_id,
                                         'message':message})),
                        mimetype="application/json")    

@require_POST
@admin_required
def delete_test(request):
    data = json.loads(request.body)
    title = data['delete_test']
    try:
        delete_test = Tests.objects.get(title=title)
        delete_test.delete()
        message = "Test %s deleted"%title
        success = True
    except Tests.DoesNotExist:
        message = "Test %s don't exist!"%title
        success = False
    return HttpResponse(json.dumps(dict({'message':message,
                                         'success':success})),
                        mimetype="application/json")

@admin_required
def admin_test(request, test_id):
    try:
        test = Tests.objects.get(id=test_id)
    except Tests.DoesNotExist:
        raise Http404
    questions = Questions.objects.filter(test=test)
    c = Context(dict({'test':test, 'questions':questions}))
    c.update(csrf(request))
    return render_to_response('admin_test.html', c)

@require_POST
@admin_required
def ajax_new_question(request, test_id):
    try:
        test = Tests.objects.get(id=test_id)
    except Tests.DoesNotExist:
        raise Http404
    data = json.loads(request.body)
    question = data['new_question'].strip()
    new_question_id = None
    if len(question) == 0:
        message = "Please insert correct data"
        success = False
    else:
        new_question = Questions(test=test, question=question)
        new_question.save()
        new_question_id = new_question.id
        message = "Question %s added."%new_question.question
        success = True
    return HttpResponse(json.dumps(dict({'message':message,
                                         'new_question_id':new_question_id,
                                         'success':success})),
                        mimetype="application/json")

@require_POST
@admin_required
def ajax_delete_question(request, test_id):
    try:
        test = Tests.objects.get(id=test_id)
    except Tests.DoesNotExist:
        raise Http404
    data = json.loads(request.body)
    id = int(data['delete_question'])
    try:
        delete_question = Questions.objects.get(test=test, id=id)
        question = delete_question.question
        delete_question.delete()
        message = "Question %s deleted"%question
    except Answers.DoesNotExist:
        message = "This question don't exist!"
    return HttpResponse(json.dumps(dict({'message':message})),
                        mimetype="application/json")

@admin_required
def admin_question(request, test_id, question_id):
    try:
        test = Tests.objects.get(id=test_id)
        question = Questions.objects.get(test=test, id=question_id)
    except (Tests.DoesNotExist, Questions.DoesNotExist):
        raise Http404
    answers = Answers.objects.filter(question=question)
    c = Context(dict({'test':test, 'question':question, 'answers':answers}))
    c.update(csrf(request))
    return render_to_response('admin_question.html', c)

@require_POST
@admin_required
def ajax_new_answer(request, test_id, question_id):
    try:
        test = Tests.objects.get(id=test_id)
        question = Questions.objects.get(test=test, id=question_id)
    except (Tests.DoesNotExist, Questions.DoesNotExist):
        raise Http404
    data = json.loads(request.body)
    answer = data['new_answer'].strip()
    correct = data['correct']
    try:
        new_answer = Answers(question=question, answer=answer, correct=correct)
        if len(answer) == 0:
            raise ValueError
        new_answer.save()
        message = "Answer %s added."%new_answer.answer
        correct = new_answer.correct
        success = True
    except ValueError:
        message = "Please insert correct data"
        success = False
    return HttpResponse(json.dumps(dict({'message':message,
                                         'new_answer_id':new_answer.id,
                                         'correct':correct,
                                         'success':success})),
                        mimetype="application/json")

@require_POST
@admin_required
def ajax_delete_answer(request, test_id, question_id):
    try:
        test = Tests.objects.get(id=test_id)
        question = Questions.objects.get(test=test, id=question_id)
    except (Tests.DoesNotExist, Questions.DoesNotExist):
        raise Http404
    data = json.loads(request.body)
    id = int(data['delete_answer'])
    try:
        delete_answer = Answers.objects.get(question=question, id=id)
        answer = delete_answer.answer
        delete_answer.delete()
        message = "Answer %s deleted"%answer
    except Answers.DoesNotExist:
        message = "This answer don't exist!"
    return HttpResponse(json.dumps(dict({'message':message})),
                        mimetype="application/json")
                        
#------------------------------ END Admin section ----------------------------


#------------------------------ Users section --------------------------------

@user_required
def user_test(request, test_id):
    try:
        test = Tests.objects.get(id=test_id)
        data = test.dict()
    except Tests.DoesNotExist:
        raise Http404
    if not data['questions']:
        raise Http404
    c = Context(dict({'test':data}))
    c.update(csrf(request))
    return render_to_response('user_test.html', c)

@require_POST
@user_required
def ajax_send_result(request, test_id):
    address = request.user.email
    print address
    try:
        test = Tests.objects.get(id=test_id)
    except Tests.DoesNotExist:
        raise Http404
    data = json.loads(request.body)
    result = data['result']
    score = 0
    for question_id in result:
        question_score = 1
        question = Questions.objects.get(test=test, id=question_id)
        correct_answers = [answer.id for answer in
                           Answers.objects.filter(question=question,
                                                  correct=True)]
        if len(result[question_id]) == len(correct_answers):
            for answer_id in result[question_id]:
                if int(answer_id) not in correct_answers:
                    question_score = 0
        else:
            question_score = 0
        score = score + question_score
    if data['send_mail']:
        send_email_with_score(score, test.title, address)
    return HttpResponse(json.dumps(dict({'score':score})),
                        mimetype="application/json")

#------------------------------ END Users section ----------------------------