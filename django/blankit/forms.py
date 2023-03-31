from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class TextInputForm(forms.Form):
    text = forms.CharField(
        label='enter the text you want to use',
        widget=forms.Textarea,
        max_length=1000
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
        self.add_help_text(prompt)

    def add_help_text(self, prompt):
        help_text = ''
        if prompt == 'noun':
            help_text = 'noun: a thing (like pineapple, wombat, refrigerator)'
        elif prompt == 'adjective':
            help_text = 'adjective: describes a thing (like yellow, gleeful, dangerous)'
        elif prompt == 'adverb':
            help_text = 'adverb: describes an action/another descriptor (like incredibly, eagerly, violently)'
        elif prompt == 'verb':
            help_text = 'verb: an action/event (like eat, explore, dream)'
        elif prompt == 'plural noun':
            help_text = 'plural noun: more than one thing (like cowboy hats, bicycles, guitars)'
        elif prompt == 'verb ending in "ing"':
            help_text = 'verb: an action/event (like wandering, snowboarding, singing)'
        print(help_text)
        self.fields['blank'].help_text = help_text
