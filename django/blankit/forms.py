from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class TextInputForm(forms.Form):
    text = forms.CharField(
        label='what text do you want to blank?',
        widget=forms.Textarea,
        max_length=2000
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('next', 'next'))

