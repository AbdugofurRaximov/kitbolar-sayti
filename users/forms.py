from django import forms
from users.models import CustomUser


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

        # fields=('__all__')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "profile_picture")

#  FORMANI QO'LDA YOZISH KODI BU
# class UserCreateForm(forms.Form):
#     username = forms.CharField(max_length=250)
#     email = forms.EmailField()
#     first_name = forms.CharField(max_length=250)
#     last_name = forms.CharField(max_length=250)
#     password = forms.CharField(max_length=20)
#
#
#     def save(self):
#         username = self.cleaned_data['username']
#         first_name = self.cleaned_data['first_name']
#         last_name = self.cleaned_data['last_name']
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']
#
#         user = User.objects.create(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             email=email
#
#         )
#         user.set_password(password)
#         user.save()
#
#         return user
#     # create user account

# class UserLoginForm(forms.Form):
#     username=forms.CharField(max_length=250)
#     password=forms.CharField(max_length=150)
