from django import forms

from .models import Resume, ResumeItem


class ResumeForm(forms.ModelForm):
    """
    A form for creating and renaming resumes. Note that 'user' is not
    included: it is always set to the requesting user.
    """
    class Meta:
        model = Resume
        fields = ['name']


class ResumeItemForm(forms.ModelForm):
    """
    A form for creating and editing resume items. Note that 'resume' is not
    included: it is always determined by the URL.
    """
    class Meta:
        model = ResumeItem
        fields = [
            'title',
            'company',
            'start_date',
            'end_date',
            'tags',
            'description'
        ]
