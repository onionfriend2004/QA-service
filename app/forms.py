from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from app.models import Profile, Answer, Question, Tag, QuestionLike, AnswerLike

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Login',
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your login'})
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

class SignUpForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        label='Repeat password'
    )

    avatar = forms.ImageField(
        required=False,
        help_text='Optional.',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your login',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
            }),
        }

        labels = {
            'username': 'Login',
            'email': 'Email',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError('Passwords do not match!')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This login is already in use')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('This field is required.')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already in use')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = Profile.objects.create(user_id=user)
            if self.cleaned_data.get('avatar'):
                profile.avatar = self.cleaned_data['avatar']
            profile.save()
        return user
    
class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your login',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
        }

        labels = {
            'username': 'Login',
            'email': 'Email',
        }

    def __init__(self, user=None, **kwargs):
        self.user = user
        super(SettingsForm, self).__init__(**kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError('This login is already in use')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('This field is required.')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError('This email is already in use')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class ImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

        labels = {
            'avatar': 'Upload avatar',
        }

        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5',
                'placeholder': 'Enter your answer here.'
            }),
        }

    def __init__(self, profile_id=None, question_id=None, *args, **kwargs):
        self._profile_id = profile_id
        self._question_id = question_id
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = super(AnswerForm, self).save(commit=False)
        answer.profile_id = self._profile_id
        answer.question_id = self._question_id
        if commit:
            answer.save()
        return answer
    
class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your tags here',
        }),
        help_text="Enter tags separated by commas.",
    )

    class Meta:
        model = Question
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your title here',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your text here',
                'rows': 10,
            }),
        }

    def __init__(self, profile_id=None, **kwargs):
        self._profile_id = profile_id
        super(QuestionForm, self).__init__(**kwargs)

    def save(self, commit=True):
        tags_str = self.cleaned_data.pop('tags')
        tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

        question = super().save(commit=False)
        question.profile_id = self._profile_id 

        if commit:
            question.save()
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(tag=tag_name)
                question.tags.add(tag)

        return question
    
class QuestionLikeForm:
    def __init__(self, user, question, is_like):
        self.user = user
        self.question = Question.objects.get(id=question)
        self.is_like = is_like

    def save(self):
        if not QuestionLike.objects.filter(question_id=self.question, profile_id=self.user).exists():
            like = QuestionLike(question_id=self.question,
                                profile_id=self.user,
                                is_like=self.is_like)
            rating = like.save()
        else:
            like = QuestionLike.objects.get(question_id=self.question, profile_id=self.user)
            if self.is_like == like.is_like:
                rating = like.delete()
            else:
                rating = like.change_mind()

        return rating

class AnswerLikeForm:
    def __init__(self, user, answer, is_like):
        self.user = user
        self.answer = Answer.objects.get(id=answer)
        self.is_like = is_like

    def save(self):
        if not AnswerLike.objects.filter(answer_id=self.answer, profile_id=self.user).exists():
            like = AnswerLike(answer_id=self.answer,
                              profile_id=self.user,
                              is_like=self.is_like)
            rating = like.save()
        else:
            like = AnswerLike.objects.get(answer_id=self.answer, profile_id=self.user)
            if self.is_like == like.is_like:
                rating = like.delete()
            else:
                rating = like.change_mind()

        return rating