from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Question, Choice, QuizAppUser,Category,Quiz,Guess,Update
from django.contrib import messages
from django.views import generic
from django.urls import reverse


# Create your views here.

def index(request):
    return render(request, 'index.html')


def usercreation(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            request.session['user'] = username
            return redirect('userauthentication')

    else:
        form = RegistrationForm()

    return render(request, 'registration/register2.html', {'form': form})


def userpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = username
                return redirect('userauthentication')
            messages.add_message(request, messages.INFO, 'User is Not Active.')
            return redirect('userpage')
        messages.add_message(request, messages.INFO, 'Please Check Your Login Credentials.')
        return redirect('userpage')

    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def userauthentication(request):
    if request.session.has_key('user'):
        username = request.session['user']
        user = QuizAppUser.objects.get(username=username)
        if user.is_staff == True:
            return render(request, 'AdminPage.html')
        categories = Category.objects.all()
        return render(request, 'userpage.html', {'categories': categories})
    return redirect('userpage')


def postcategory(request):
    if request.session.has_key('user'):
        if request.method == 'POST':
            category = request.POST['category']
            new_category = Category(name=category)
            new_category.save()
            messages.add_message(request, messages.INFO, 'Category Added Successfully.')
            return redirect('postcategory')
        return render(request, 'PostCategory.html')
    return redirect('userpage')


def postquestion(request):
    if request.session.has_key('user'):
        if request.method == 'POST':
            que = request.POST['question']
            category = request.POST['category']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            category_id = Category.objects.get(name=category)
            question = Question.objects.create(category=category_id, question=que)
            try:
                option1_check = request.POST['check_option1']
                choice_1 = Choice.objects.create(question=question, answer=option1, correct=option1_check)
            except:
                choice_1 = Choice.objects.create(question=question, answer=option1)
            try:
                option2_check = request.POST['check_option2']
                choice_2 = Choice.objects.create(question=question, answer=option2, correct=option2_check)
            except:
                choice_2 = Choice.objects.create(question=question, answer=option2)
            try:
                option3_check = request.POST['check_option3']
                choice_3 = Choice.objects.create(question=question, answer=option3, correct=option3_check)
            except:
                choice_3 = Choice.objects.create(question=question, answer=option3)
            try:
                option4_check = request.POST['check_option4']
                choice_3 = Choice.objects.create(question=question, answer=option4, correct=option4_check)
            except:
                choice_3 = Choice.objects.create(question=question, answer=option4)

            messages.add_message(request, messages.INFO, 'Question Posted Successfully.')
            return redirect('postquestion')
        categories = Category.objects.all()
        return render(request, 'postquestion.html', {'categories': categories})
    return redirect('userpage')


def viewquestions(request):
    if request.session.has_key('user'):
        categories = Category.objects.all()
        return render(request, 'viewquestions.html', {'categories': categories})
    return redirect('userpage')


def viewhistory(request):
    if request.session.has_key('user'):
        if request.method == 'POST':
            pass
        quizs = Quiz.objects.all()
        return render(request, 'viewhistory.html', {'quizs': quizs})
    return redirect('usepage')


def userhistory(request,pk):
    if request.session.has_key('user'):
        if request.method == 'POST':
            pass
        quizs = Quiz.objects.filter(owner=pk)
        return render(request, 'userhistory.html', {'quizs': quizs})
    return redirect('usepage')


def viewcategory(request):
    if request.session.has_key('user'):
        if request.method == 'GET':
            categories = Category.objects.all()
            return render(request,'viewcategory.html',{'categories': categories})
    return redirect('usepage')

def takequiz(request, pk):
    if request.session.has_key('user'):
        category = Category.objects.get(pk=pk)
        questions = Question.objects.filter(category=category)
        return render(request, 'quiz.html', {'questions': questions, 'category': category})
    return redirect('userpage')


def result(request, pk):
    if request.session.has_key('user'):
        if request.method == 'POST':
            username = request.session['user']
            category = Category.objects.get(pk=pk)
            submitted_by = QuizAppUser.objects.get(username=username)
            quiztaken = Quiz(owner=submitted_by, category=category)
            quiztaken.save()
            question_count = Question.objects.filter(category=pk).count()
            for i in range(1, question_count + 1):
                question_id = request.POST['question' + str(i)]
                answered_question = Question.objects.get(id=question_id)
                choice_id = request.POST['check_option' + str(i)]
                answer_given = Choice.objects.get(id=choice_id)
                quiz = Guess(submitted_by=submitted_by, answer_given=answer_given, answered_question=answered_question,
                             quiz=quiztaken)
                quiz.save()

            score = 0
            guesses = Guess.objects.filter(submitted_by=submitted_by, quiz=quiztaken)
            for guess in guesses:
                if guess.answer_given.correct == True:
                    score += 1

            quiztaken.score = score
            quiztaken.save()

            return render(request, 'success.html', {'score': score, 'count': question_count})

    return redirect('userpage')


def success(request):
    pass


def editquestions(request, pk):
    if request.session.has_key('user'):
        if request.method == "POST":
            que = request.POST['question']

            question = Question.objects.get(id=pk)
            question.question = que
            question.save()

            choices = question.choice_set.all()

            for i in range(4):
                choice_id = choices[i].id
                obj = Choice.objects.get(pk=choice_id)
                obj.answer = request.POST['option' + str(i + 1)]
                try:
                    obj.correct = request.POST['check_option' + str(i + 1)]
                except:
                    obj.correct = False
                obj.save()

            return redirect('viewquestions')
        question = Question.objects.get(id=pk)
        choices = Choice.objects.filter(question=question)
        return render(request, 'editquestion.html', {'question': question, 'choices': choices})
    return redirect('userpage')


def editcategories(request,pk):
    if request.session.has_key('user'):
        if request.method == "POST":
            cat = request.POST['category']
            category = Category.objects.get(id=pk)
            category.name = cat
            category.save()
            return redirect('viewcategory')
        category = Category.objects.get(id=pk)
        return render(request, 'editcategory.html', {'category': category })
    return redirect('userpage')


def forgot(request):
    return render(request,'forgot.html')


def updateprofile(request):
    # if request.session.has_key('user'):
    #     if request.method == "POST":
    #         fname = request.POST['First name']
    #         lname = request.POST['Last name']
    #         uname = request.POST['User name']
    #         email = request.POST['Email Address']
    #         insert = models.QuizAppUser(First_Name=fname, Last_name=lname, User_name=uname, Email=email)
    #         insert.save()
    #         messages.add_message(request, messages.INFO,'Registration Successfully completed.')
    #         return redirect('login')
        return render(request, 'updateprofile.html')
    #return redirect('userpage')


def viewanswers(request):
    if request.session.has_key('user'):
        if request.method == "GET":
            return render(request,'viewanswers.html')
        return render(request,)
    return redirect('userpage')





class QuestionList(generic.ListView):
    template_name = 'questionlist.html'

    def get_queryset(self):
        return Question.objects.all()


class QuestionDetail(generic.DetailView):
    model = Question
    template_name = 'questiondetail.html'
    context_object_name = 'questiondetails'




