from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

def signup(request):
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form=UserForm()
    return render(request, 'common/signup.html', {'form': form})


class ProfileView(DetailView):
    context_object_name='profile_user'
    model=User
    template_name='common/profile.html'

@login_required(login_url='common:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호가 변경되었습니다!')
        else:
            messages.error(request, '비밀번호를 확인해주세요!')
    else:
        form=PasswordChangeForm(request.user)
    context={'form': form}
    return render(request, 'common/profile.html', context)
    
