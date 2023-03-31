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
        self.helper.add_input(Submit('blank it', 'blank it'))


class BlankForm(forms.Form):
    blank = forms.CharField(max_length=100)
    tokens = forms.JSONField(widget=forms.HiddenInput())
    prompts = forms.JSONField(widget=forms.HiddenInput())
    whitespace = forms.JSONField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        prompt = 'ERROR'
        tokens = []
        prompts = []
        whitespace = []
        if 'prompt' in kwargs:
            prompt = kwargs['prompt']
            kwargs.pop('prompt')
        if 'tokens' in kwargs:
            tokens = kwargs['tokens']
            kwargs.pop('tokens')
        if 'prompts' in kwargs:
            prompts = kwargs['prompts']
            kwargs.pop('prompts')
        if 'whitespace' in kwargs:
            whitespace = kwargs['whitespace']
            kwargs.pop('whitespace')
        super().__init__(*args, **kwargs)
        self.fields['blank'].label = prompt
        self.fields['tokens'].initial = tokens
        self.fields['prompts'].initial = prompts
        self.fields['whitespace'].initial = whitespace
        self.helper = FormHelper()
        self.helper.add_input(Submit('next', 'next'))

