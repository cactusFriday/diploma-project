from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
# Create your views here.

class IndexView():
    pass

def index(request):
    context = {
        'username': request.user,
    }
    return render(request, 'workspace/index.html', context=context )

# class UserLogout(LogoutView):
#     next_page = reverse_lazy('login')
