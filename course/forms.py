from django import forms
from django.forms.models import inlineformset_factory
from course.models import *
from classroom.models import (
    User
)

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)

class CourseCreateForm(forms.ModelForm):
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
    titre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'cols': 40, 'rows': 15}))

    class Meta:
        model = Course
        fields = ['classe', 'titre', 'description',]


class ModuleForm(forms.ModelForm):
    titre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'cols': 40, 'rows': 8}))

    class Meta:
        model = Module
        exclude = ()

ModuleFormSet = inlineformset_factory(Course, Module, form=ModuleForm, fields=['titre', 'description',], extra=2, can_delete=True)


# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ('rating', 'comment',)
#         widgets = {
#             'comment': forms.Textarea(attrs={'cols': 40, 'rows': 15, 'class':'no-resize appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500 h-48 resize-none'})
#         }

