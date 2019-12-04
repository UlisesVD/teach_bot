from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from .models import Course, Unity, Exam, Question, Answer
from django import forms
from django.urls import reverse_lazy
from .forms import CourseForm, UnityForm
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json


# Create your views here.
@method_decorator(login_required, name='dispatch')
class CreateCourse(CreateView):
    form_class = CourseForm
    template_name = "courses/courses.html"
    success_url = reverse_lazy("courses:createcourse")

    def get_context_data(self, **kwargs):
        context = super(CreateCourse, self).get_context_data(**kwargs)
        if self.request.user.type == 'teacher':
            context["courses_list"] = Course.objects.filter(id_user=self.request.user)
        else:
            context["courses_list"] = Course.objects.all()
        return context

    def form_valid(self, form):
        form.instance.id_user = self.request.user
        return super(CreateCourse, self).form_valid(form)


@login_required
def delete_course(request):
    course = Course.objects.filter(id = request.POST["id_course"])
    if request.method == "POST":
        course.delete()
        return redirect('courses:createcourse')


@login_required
def update_course(request, id_course):
    course = Course.objects.get(id = id_course)
    #print("----", course)
    if request.method == "GET":
        form = CourseForm(instance=course)
        #print("++++", form)
    else:
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
        return redirect('courses:createcourse')
    # print(form)
    return render(request, 'courses/update_course.html',{'form':form})

##########################################################################
#                          functions for Unities                         #
##########################################################################

@login_required
def delete_unity(request, id_unity, id_course, title):
    unity = Unity.objects.filter(id = id_unity)
    if request.method == "GET":
        form  = UnityForm()
        unity.delete()
        try:
            unities = Unity.objects.filter(id_course = id_course)
        except:
            unities = None
        #form.id_course = id
        return render(request, 'courses/unities.html', {'unities': unities, 'title': title, 'id_course': id_course, 'form': form})


@login_required
def detail(request, id, title):
    if request.method == "POST":
        form = UnityForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                pass

    form  = UnityForm()
    try:
        unities = Unity.objects.filter(id_course=id)
    except:
        unities = None
    #form.id_course = id
    return render(request, 'courses/unities.html', {'unities': unities, 'title': title, 'id_course': id, 'form': form})

@login_required
def update_unity(request, id_unity, id_course, title):
    unity = Unity.objects.get(id = id_unity)
    if request.method == "GET":
        form = UnityForm(instance=unity)
        # print("---------", form.date_start)
    else:
        form = UnityForm(request.POST, instance=unity)
        if form.is_valid():
            form.save()
        try:
            unities = Unity.objects.filter(id_course=id_course)
            form  = UnityForm()
        except:
            unities = None
        return render(request, 'courses/unities.html', {'unities': unities, 'title': title, 'id_course': id_course, 'form': form})
    return render(request, 'courses/update_unity.html',{'form':form, 'title': title, 'id_course': id_course,})

######################################################
#              functions for exams                   #
######################################################

@login_required
def create_exam(request):
    h1 = "<h1>Prueba</h1>"
    exam = ""
    try:
        exam = Exam.objects.get(id_unity = request.POST["unity_id"])
    except:
        pass
    if exam:
        # print("exam", exam)
        questions = Question.objects.filter(id_exam = exam.id)
        questions_answers = []
        for question in questions:
            answers = Answer.objects.filter(id_question = question.id)
            questions_answers.append({"question": question.question, "type": question.type, "answers": answers})
        # print("dic_questions", questions_answers)
        return render(request, "courses/form_exam.html", {"unity_id":request.POST["unity_id"], "exam": exam, "questions_answers": questions_answers})
    return render(request, "courses/form_exam.html", {"unity_id":request.POST["unity_id"]})


@login_required
def save_exam(request):
    data = request.body
    json_data = json.loads(data)
    unity = Unity.objects.get(id=int(json_data[0]["unity_id"]))
    try:
        instance_exam = Exam.objects.get(id_unity=unity)
        if instance_exam:
            instance_exam.delete()
    except:
        pass
    exam = Exam()
    exam.title = json_data[0]["tittle"]
    exam.date_application = json_data[0]["date"]
    exam.id_unity = unity
    exam.save()
    exam_id = exam.id
    for questions in json_data[1]:
        question = Question()
        question.question = questions["question"]
        question.id_exam = exam
        question.type = questions["type"]
        question.save()
        id_question = question
        for answers in questions["answers"]:
            answer = Answer()
            answer.answer = answers["answer"]
            answer.is_correct = True if (answers["is_correct"] == 'True') else False
            answer.id_question = id_question
            answer.save()
    print(questions)
