from django.shortcuts import render
from django.contrib.auth.views import LogoutView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from account.models import Transaction, WorkerBiometric, Profile
from .models import Documents

class IndexView():
    pass

@login_required(login_url='account:login')
def index(request):
    if request.method == 'POST':
        upl_file = request.FILES['doc']
        dic = {
            'user': request.user,
            'file': upl_file,
            'permission': 1,
        }
        temp_doc = Documents()
        temp_doc.fill(dic)
        temp_doc.save()
        print(upl_file.name, upl_file.size)
    user = request.user
    email = user.email
    usname = user.username
    f_name = user.first_name
    l_name = user.last_name
    context = {
        'username': usname,
        'email': email,
        'f_name': f_name,
        'l_name': l_name,
    }
    return render(request, 'workspace/index.html', context=context )

def documentView(request):
    if request.method == 'POST':
        upl_file = request.FILES['doc']
        dic = {
            'user': request.user,
            'file': upl_file,
            'permission': 1,
        }
        temp_doc = Documents()
        temp_doc.fill(dic)
        temp_doc.save()
        print(dic)
    user = request.user
    email = user.email
    usname = user.username
    f_name = user.first_name
    l_name = user.last_name
    temp_doc = Documents.objects.all()
    docs = [
        (temp_doc[0].file, 'Александр Иванов', '23.04.2021', '0', 'Изменение'),
        (temp_doc[1].file, 'Алексей Васильев', '12.01.2021', '1', 'Создание'),
        (temp_doc[2].file, 'Георгий Калинов', '01.05.2020', '2', 'Изменение'),
        (temp_doc[3].file, 'Степан Александров', '19.08.2021', '3', 'Удаление'),
    ]
    top_docs = docs[:-1]
    # for doc in temp_doc:
    #     temp = (doc.file, doc.created_by)
    #     docs.append(temp)
    context = {
        'username': usname,
        'email': email,
        'f_name': f_name,
        'l_name': l_name,
        'docs': docs,
        'top_docs': top_docs,
    }
    return render(request, 'workspace/documents.html', context=context )

def accessView(request):
    user = request.user
    email = user.email
    usname = user.username
    f_name = user.first_name
    l_name = user.last_name
    # person, action, obj, trans
    access = [
        ('Иван Иванов', 'Вход по биометрии', 'КПП №1', '1'), 
        ('Александр Петров', 'Вход по ЭЦП', 'Отдел №23', '2'), 
        ('Васильев Алексей', 'Вход по биометрии', 'КПП №1', '3'), 
        ('Иван Иванов', 'Выход по биометрии', 'КПП №3', '4')
        ]

    context = {
        'username': usname,
        'email': email,
        'f_name': f_name,
        'l_name': l_name,
        'access': access,
    }
    return render(request, 'workspace/access.html', context=context )

class DocumentView(TemplateView):
    template_name = 'workspace/documents.html'


# class UserLogout(LogoutView):
#     next_page = reverse_lazy('login')
