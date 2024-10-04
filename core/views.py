from django.shortcuts import render,HttpResponseRedirect,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,LogInForm,BlogPostForm,event1Form,event2Form,contactForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import BlogPost,event1,event2
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
import requests
from django.conf import settings

import html  # Import the html module for unescaping HTML entities
from django.shortcuts import render
from .models import Quiz, Question, Answer



def home(request):
    return render(request,"core/homepage.html")
def features(request):
    return render(request,"core/features.html")
def blog(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'core/blog.html', {'posts': posts})

def add_blog_post(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, display a message and keep them on the same page
        messages.error(request, "You need to log in first to add a blog post.")
        return redirect('login')  # Redirect them to the login page

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('blog')  # Redirect to the blog list after saving
    else:
        form = BlogPostForm()
    
    return render(request, 'core/add_editblog.html', {'form': form})

@login_required
def edit_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'core/add_editblog.html', {'form': form})

@login_required
def delete_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog')
    return redirect('blog')


def quiz(request):
    return render(request,"core/quiz.html")
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
         form=LogInForm(request=request,data=request.POST)
         if form.is_valid():
           uname=form.cleaned_data["username"]
           upass=form.cleaned_data["password"]
           user=authenticate(username=uname,password=upass)
           if user is not None:
               login(request,user)
               messages.success(request,"congratulations!!you succesfully logged in")
               return redirect("/")
          
         return render(request, "core/login.html", {"form": form})              
        else:
         form=LogInForm()           
    
         return render(request,"core/login.html",{"form":form})
    else:
       return redirect("/")
def user_signup(request):
    if request.method=="POST":
       form=SignUpForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request,"congratulations!! You have succesfully signed up")
           return redirect("/")
           
    else:
        form=SignUpForm()       
           
    
    return render(request,"core/signup.html",{"form":form})
def dashboard(request):
    if request.user.is_authenticated:
     return render(request,"core/dashboard.html")
    else:
       return HttpResponseRedirect('/login/')
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
            
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'core/edit_profile.html', {'form': form})    
def user_logout(request):
    logout(request)
    messages.success(request,"You have succesfully logged out")
    return HttpResponseRedirect("/")


def fetch_and_display_quiz(request):
    num_questions = int(request.GET.get('num_questions', 0))
    api_url = f"https://opentdb.com/api.php?amount={num_questions}&category=27&difficulty=medium&type=multiple"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        questions_data = response.json().get('results', [])
    except requests.RequestException as e:
        return render(request, 'core/error.html', {'message': 'Failed to fetch data from API'})
    
    quiz, created = Quiz.objects.get_or_create(
        title="Wildlife Trivia",
        defaults={'description': 'Test your wildlife knowledge'}
    )

    # Clear old questions and answers
    Question.objects.filter(quiz=quiz).delete()
    Answer.objects.filter(question__quiz=quiz).delete()

    for question_data in questions_data:
        # Unescape HTML entities in question text
        question_text = html.unescape(question_data.get('question', ''))

        question, created = Question.objects.get_or_create(
            quiz=quiz,
            text=question_text
        )

        answers = question_data.get('incorrect_answers', [])
        correct_answer = question_data.get('correct_answer', '')

        # Unescape HTML entities in answers
        answers = [html.unescape(answer) for answer in answers]
        correct_answer = html.unescape(correct_answer)

        answers.append(correct_answer)

        for answer_text in answers:
            Answer.objects.get_or_create(
                question=question,
                text=answer_text,
                is_correct=(answer_text == correct_answer)
            )

    return render(request, 'core/quiz_list.html', {'quiz': quiz})

def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = 0
    incorrect_answers = []

    for question in quiz.questions.all():
        selected_answer_id = request.POST.get(f'question_{question.id}')
        if selected_answer_id:
            try:
                selected_answer = Answer.objects.get(id=selected_answer_id, question=question)
                if selected_answer.is_correct:
                    score += 1
                else:
                    correct_answer = question.answers.filter(is_correct=True).first()
                    incorrect_answers.append({
                        'question': question,
                        'selected_answer': selected_answer,
                        'correct_answer': correct_answer
                    })
            except Answer.DoesNotExist:
                pass

    total_questions = quiz.questions.count()

    return render(request, 'core/quiz_submit.html', {
        'quiz': quiz,
        'score': score,
        'total_questions': total_questions,
        'incorrect_answers': incorrect_answers
    })
def encyclopedia(request):
    return render(request,"core/map.html")

def aq(request):
    return render(request,"core/aqwildlife.html")
def pet(request):
    return render(request,"core/pet.html")
def tank(request):
    return render(request,"core/tank.html")

# core/views.py

def ap_view(request):
    return render(request, 'core/ap2.html')

def as_view(request):
    return render(request, 'core/as2.html')

def ar_view(request):
    return render(request, 'core/ar2.html')

def br_view(request):
    return render(request, 'core/br2.html')

def ct_view(request):
    return render(request, 'core/ct2.html')

def ga_view(request):
    return render(request, 'core/ga2.html')

def gj_view(request):
    return render(request, 'core/gj2.html')

def hp_view(request):
    return render(request, 'core/hp2.html')

def hr_view(request):
    return render(request, 'core/hr2.html')

def jh_view(request):
    return render(request, 'core/jh2.html')

def ka_view(request):
    return render(request, 'core/ka2.html')

def kl_view(request):
    return render(request, 'core/kl2.html')

def mh_view(request):
    return render(request, 'core/mh2.html')

def mn_view(request):
    return render(request, 'core/mn2.html')

def mp_view(request):
    return render(request, 'core/mp2.html')

def ml_view(request):
    return render(request, 'core/ml2.html')

def mz_view(request):
    return render(request, 'core/mz2.html')

def nl_view(request):
    return render(request, 'core/nl2.html')

def or_view(request):
    return render(request, 'core/or2.html')

def pb_view(request):
    return render(request, 'core/pb2.html')

def rj_view(request):
    return render(request, 'core/rj2.html')

def sk_view(request):
    return render(request, 'core/sk2.html')

def tn_view(request):
    return render(request, 'core/tn2.html')

def tg_view(request):
    return render(request, 'core/tg2.html')

def tr_view(request):
    return render(request, 'core/tr2.html')

def up_view(request):
    return render(request, 'core/up2.html')

def ut_view(request):
    return render(request, 'core/ut2.html')

def wb_view(request):
    return render(request, 'core/wb2.html')

def an_view(request):
    return render(request, 'core/an2.html')

def ch_view(request):
    return render(request, 'core/ch2.html')

def dl_view(request):
    return render(request, 'core/dl2.html')

def ld_view(request):
    return render(request, 'core/ld2.html')

def py_view(request):
    return render(request, 'core/py2.html')

def jk_view(request):
    return render(request, 'core/jk2.html')

def donate(request):
    return render(request, 'core/donate.html')
def event1(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, display a message and keep them on the same page
        messages.error(request, "You need to log in first to register in a event.")
        return redirect('login')  # Redirect them to the login page

    if request.method == 'POST':
        form = event1Form(request.POST, request.FILES)
        if form.is_valid():
            event_1 = form.save(commit=False)
            
            event_1.save()
            messages.success(request,"You have succesfully registered in event1")
            return HttpResponseRedirect("/") # Redirect to the blog list after saving
    else:
        form = event1Form()
    
    return render(request, 'core/event1reg.html', {'form': form})

def event2(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, display a message and keep them on the same page
        messages.error(request, "You need to log in first to register in a event.")
        return redirect('login')  # Redirect them to the login page

    if request.method == 'POST':
        form = event2Form(request.POST, request.FILES)
        if form.is_valid():
            event_2 = form.save(commit=False)
            
            event_2.save()
            messages.success(request,"You have succesfully registered in event2")
            return HttpResponseRedirect("/") # Redirect to the blog list after saving
    else:
        form = event2Form()
    
    return render(request, 'core/event2reg.html', {'form': form})


def contact(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, display a message and keep them on the same page
        messages.error(request, "You need to log in first to contact with us.")
        return redirect('login')  # Redirect them to the login page

    if request.method == 'POST':
        form = contactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.name=request.user
            contact.email = request.user.email 
            
            contact.save()
            messages.success(request,"You have succesfully sent message to us")
            return HttpResponseRedirect("/") # Redirect to the blog list after saving
    else:
        form = contactForm()
    
    return render(request, 'core/contact.html', {'form': form})



