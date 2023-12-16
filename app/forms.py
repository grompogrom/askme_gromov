from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import ImageField

from app.models import Profile, Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        exists = User.objects.filter(email=email).all().count()
        if exists:
            raise ValidationError('Email already registered')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username=username).all().count()
        if exists:
            raise ValidationError('Username already used')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')

        if password != password_check:
            raise ValidationError('Passwords do not match')

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        print(self.cleaned_data)
        user = User.objects.create_user(**self.cleaned_data)
        Profile.objects.create(user=user)
        return user


class ProfileForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    avatar = ImageField(required=False)

    def __init__(self, user, *args, **kwargs):
        self.user: User = user
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.user.username
        self.fields['email'].initial = self.user.email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).all().first()
        # fixme doesnt work
        if user and username != self.user.username:
            raise ValidationError('Username already used')
        return username

    def clean_email(self):
        form_email = self.cleaned_data.get('email').lower().strip()
        db_user = User.objects.filter(email=form_email).first()
        if not db_user or db_user.email == form_email:
            return form_email
        if db_user.email == "":
            return form_email
        raise ValidationError('Email already used')

    def save(self, **kwargs):
        new_username = self.cleaned_data.get('username')
        new_email = self.cleaned_data.get('email')
        image = self.cleaned_data.get('avatar')
        if new_username != self.user.username:
            self.user.username = new_username
        if new_email != self.user.email:
            self.user.email = new_email
        self.user.save()
        profile = self.user.profile
        print("image is", image)
        if image:
            profile.avatar = image
        profile.save()
        return profile


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(help_text="Enter tags separated by spaces. Maximum 3 tags")

    def __init__(self, user, *args, **kwargs):
        self.user: User = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title', 'text']

    def clean_tags(self):
        form_tags_str = self.cleaned_data.get('tags')
        from_tags_list = form_tags_str.strip().split(' ')
        if len(from_tags_list) > 3:
            raise ValidationError('Tags limit is exceeded')
        if len(from_tags_list) < 1:
            raise ValidationError('Question must have at least one tag')
        if len(from_tags_list) > len(set(from_tags_list)):
            raise ValidationError('Duplicate tags found')
        return form_tags_str

    def clean_title(self):
        form_title_str = self.cleaned_data.get('title').strip()
        if len(form_title_str) < 2:
            raise ValidationError('Too short title')
        if len(form_title_str) > 100:
            raise ValidationError('Too long title')
        return form_title_str

    def clean_text(self):
        form_text_str = self.cleaned_data.get('text').strip()
        if len(form_text_str) < 10:
            raise ValidationError('Too short text')
        if len(form_text_str) > 500:
            raise ValidationError('Too long text')
        return form_text_str

    def get_tags(self):
        form_tags_str = self.cleaned_data.get('tags')
        from_tags_list = form_tags_str.strip().split(' ')
        db_tags = []
        for tag in from_tags_list:
            db_tags.append(
                Tag.objects.get_or_create(
                    name=tag.strip()
                )
            )
        return list(map(lambda x: x[0], db_tags))

    def save(self, commit=True):
        profile = Profile.objects.get(user=self.user)
        question = Question(
            author=profile,
            title=self.cleaned_data['title'],
            text=self.cleaned_data['text']
        )
        question.save()
        question.tags.set(self.get_tags())
        return question


class AnswerForm(forms.ModelForm):
    def __init__(self, user, question_id, *args, **kwargs):
        self.user: User = user
        self.question_id = question_id
        super().__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['text']
        labels = {
            'text': 'Answer Text',
        }

    def save(self, commit=True):
        question = Question.objects.get(id=self.question_id)
        profile = Profile.objects.get(user=self.user)
        answer = Answer(
            author=profile,
            question=question,
            text=self.cleaned_data['text']
        )
        if commit:
            answer.save()
        return answer
