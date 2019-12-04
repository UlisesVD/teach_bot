from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import MyCourses
from courses.models import Course
from courses.models import Unity
from courses.models import Exam
from courses.models import Question
from courses.models import Answer

import json
import nltk
from nltk.tokenize import TreebankWordTokenizer
from collections import Counter
from googletrans import Translator
from nltk.corpus import wordnet as wn
import math
translator = Translator()

# Create your views here.
class MyCoursesListView(ListView):
    template_name = "myCoursers/courses.html"
    model = MyCourses
    paginate_by = 20  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses_list"] = MyCourses.objects.filter(id_user=self.request.user)
        return context


@login_required
def detail(request, id, title):
    try:
        unities = Unity.objects.filter(id_course=id)
    except:
        unities = None
    #form.id_course = id
    return render(request, 'myCoursers/unities.html', {'unities': unities, 'title': title, 'id_course': id})

@login_required
def addToFaborites(request, id_course):
    myCourse = MyCourses()
    myCourse.id_course = Course.objects.get(id = id_course)
    myCourse.id_user = request.user
    msg = {}
    if myCourse.save():
        msg = {"status": True, "message": "Agregado con exito"}
    else:
        msg = {"status": False, "message": "Error al agregar el curso"}
    return redirect('courses:createcourse')

@login_required
def solve_exam(request):
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
        return render(request, "myCoursers/form_exam.html", {"unity_id":request.POST["unity_id"], "exam": exam, "questions_answers": questions_answers})
    return render(request, "myCoursers/form_exam.html", {"unity_id":request.POST["unity_id"]})

@login_required
def results_exam(request):
    calif_total=0
    variable = request.POST.dict()
    data=[]
    for answer_id in list(variable)[1:]:
        dictionary={}
        answer_correct = Answer.objects.get(id=answer_id)
        answer_student = request.POST[answer_id]
        dictionary["question"] = answer_correct.id_question.question
        
        
        if answer_student == 'check':
            dictionary["student_answer"]=answer_correct.answer
            if answer_correct.is_correct:
                calif_total+=1
                dictionary["teacher_answer"]=answer_correct.answer
                dictionary["qualification"]=1
            else:
                ca=Answer.objects.get(id_question=answer_correct.id_question, is_correct=True)
                dictionary["teacher_answer"]=ca.answer
                dictionary["qualification"]=0
        else:
            qualification= check_value(calculate_simility(answer_correct.answer, answer_student))
            calif_total+=qualification
            dictionary["teacher_answer"]=answer_correct.answer
            dictionary["student_answer"]=answer_student
            dictionary["qualification"]=qualification
        data.append(dictionary)
    print(data) 
    promedio=(calif_total/len(list(variable)[1:]))*100
    return render(request, "myCoursers/results.html", {"total_calif": promedio, "data": data}) 



def check_value(value):
    if value >= 0.5:
        return 1
    elif value < 0.5 and value >= 0.45:
        return 0.9
    elif value < 0.45 and value >= 0.40:
        return 0.8
    elif value < 0.40 and value >= 0.35:
        return 0.7
    elif value < 0.35 and value >= 0.30:
        return 0.6
    elif value < 0.30 and value >= 0.25:
        return 0.5
    elif value < 0.25 and value >= 0.20:
        return 0.4
    elif value < 0.20 and value >= 0.15:
        return 0.3
    elif value < 0.15 and value >= 0.10:
        return 0.2
    elif value < 0.10 and value >= 0.05:
        return 0.1
    elif value < 0.05:
        return 0

def cosine_similarity(v1, v2):
    sum_v1, sum_v2, sum_res = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sum_v1 += x*x
        sum_v2 += y*y
        sum_res += y*x
    return sum_res/math.sqrt(sum_v1 * sum_v2)

def calculate_simility(correct_answer, answer):
    tokenizer = TreebankWordTokenizer()
    tokens_correct_answer = tokenizer.tokenize(correct_answer.lower() or '')
    tokens_answer = tokenizer.tokenize(answer.lower() or '')
    print("********************Maestro", len(tokens_correct_answer))
    print("********************Chida", len(tokens_answer))
    #################################
    # limpiando los tokens stopwords #
    stop_words = nltk.corpus.stopwords.words("spanish")
    tokens_correct_answer = [x for x in tokens_correct_answer if x not in stop_words and x not in "./,:<>!$%&/()=?¡¿'@[]{}"]
    tokens_answer = [x for x in tokens_answer if x not in stop_words and x not in "./,:<>!$%&/()=?¡¿'@[]{}"]
    print("********************Reduccion", len(tokens_correct_answer))
    

    # print(stop_words)
    dictionary = set(tokens_correct_answer + tokens_answer)
    synonyms = []
    list_syn = []
    # for tk in tokens_correct_answer: 
    #     translation = translator.translate(tk, dest='es')
    #     for syn in wn.synsets(translation.text):
    #         for lm in syn.lemmas("spa"):
    #             #print(lm.name())
    #             lm_english = translator.translate(lm.name(), dest='en')
    #             # similitud de palabras
    #             # cuando la similitud se mayor a 4 acepta el sinonimo
    #             try:
    #                 w1 = wn.synset(translation.text + ".n.01")
    #                 w2 = wn.synset(lm_english.text + ".n.01")
    #                 if w1.wup_similarity(w2) > 0.4 :
    #                     list_syn.append(lm.name())
    #             except Exception as e:
    #                 print("No hay sinonimo")
    #print(list_syn)
    dictionary = set(list(dictionary) + list(list_syn))
    #print(len(dictionary))
    array_correct_answer = []
    array_answer = []
    #print(dictionary)

    for dc in dictionary:
        if dc in tokens_correct_answer:
            array_correct_answer.append(1)
        else:
            array_correct_answer.append(0)
        if dc in tokens_answer:
            array_answer.append(1)
        else:
            array_answer.append(0)

    return cosine_similarity(array_correct_answer, array_answer)
