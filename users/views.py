from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from users.forms import UserCreateForm, UpdateUserForm
# ,UserLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


class RegisterView(View):
    def get(self, request):

        create_form = UserCreateForm()
        # bu yerda contextni yaratilishiga sabab htmlda yoligan kodlarni qisqartish yani djangoni ozida yaratailgan formdan foydalanish
        context = {
            'form': create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):

        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')

        else:
            context = {
                'form': create_form
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()

        # login_form=UserLoginForm()
        return render(request, 'users/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in !!!")
            return redirect('books:list')
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "users/profile.html", {"user": request.user})
        # if not request.user.is_authenticated:
        #     return redirect('users:login')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out !!!")
        return redirect("landing_page")


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        user_update = UpdateUserForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {"user_update": user_update})

    def post(self, request):
        user_update = UpdateUserForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES)

        if user_update.is_valid():
            user_update.save()
            messages.success(request, "You have successfully update profile!!!")
            return redirect('users:profile')

        return render(request, 'users/profile_edit.html',{"user_update": user_update})
