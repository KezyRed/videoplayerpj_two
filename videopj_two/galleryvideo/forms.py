from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student','Студент'),
        ('teacher','Преподаватель'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Роль',
        widget=forms.RadioSelect
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email','role')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Добавляем пользователя в группу в зависимости от выбранной роли
            group_name = "Преподаватели" if self.cleaned_data['role'] == 'teacher' else "Студенты"
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        return user