import numpy as np
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import TextInputForm, BlankForm
from .text_processing import preprocess_text


class HomePageView(TemplateView):
    template_name = 'home.html'


class TextInputView(FormView):
    template_name = 'text.html'
    form_class = TextInputForm
    tokens = []
    prompts = []
    whitespace = []

    def post(self, request, *args, **kwargs):
        form = self.get_form(form_class=TextInputForm)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            tokens = preprocess_text(text)
            if tokens.empty:
                return False
            self.tokens = tokens.apply(lambda row: row.token.text, axis=1).tolist()
            self.prompts = tokens['prompt'].tolist()
            self.whitespace = tokens['ws'].tolist()
        else:
            form = self.get_form(form_class=BlankForm)
            if not form.is_valid():
                return False
            blank = form.cleaned_data.get('blank')
            self.tokens = form.cleaned_data.get('tokens')
            self.prompts = form.cleaned_data.get('prompts')
            self.whitespace = form.cleaned_data.get('whitespace')
            self.update(blank)
        index = self.get_prompt()
        print(f'index {index}')
        if index is None:
            # filling is complete
            output = ''
            for i in range(len(self.tokens)):
                output += self.tokens[i]
                output += self.whitespace[i]
            return render(
                self.request,
                'output.html',
                {'text': output},
            )
        prompt = self.prompts[index]
        blank_form = BlankForm(
            prompt=prompt,
            tokens=self.tokens,
            prompts=self.prompts,
            whitespace=self.whitespace,
        )
        return render(
            self.request,
            'blank.html',
            {'form': blank_form, 'tokens': self.tokens},
        )

    def update(self, blank):
        index = self.get_prompt()
        if index is not None:
            self.tokens[index] = blank
            self.prompts[index] = ''

    # def get_prompt(self):
    #     print(self.tokens)
    #     index = self.get_index()
    #     if index is not None:
    #         return self.prompts[index]

    def get_prompt(self):
        index = 0
        while index < len(self.prompts):
            print(type(self.prompts[index]))
            if self.prompts[index] != '' and isinstance(self.prompts[index], str):
                return index
            index += 1

    # def form_valid(self, form):
    #     """When valid form data has been POSTed, save input for next step"""
    #     print("FORM VALID")
    #     text = form.cleaned_data.get('text')
    #     if text != '':
    #         self.tokens = preprocess_text(text)
    #         if self.tokens.empty:
    #             return False
    #         blank_form = BlankForm(prompt='hi')
    #         print("HERE")
    #         print("HERE")
    #         # return HttpResponseRedirect(reve rse_lazy('blank'))
    #         return render(self.request, 'blank.html', {'form': blank_form})
    #     else:
    #         blank = form.cleaned_data.get('blank')
    #         print('THERE')
    #         print('THERE')
    #         blank_form = BlankForm(prompt='bye')
    #         return render(self.request, 'blank.html', {'form': blank_form})
        # return BlankView()

    # def get_success_url(self):
    #     return reverse_lazy('blank', kwargs={'tokens': self.tokens})


# class BlankView(FormView):
#     template_name = 'blank.html'
#     form_class = BlankForm
#     tokens = None
#
#     def __init__(self, *args, **kwargs):
#         if 'tokens' in kwargs:
#             tokens = kwargs['tokens']
#             kwargs.pop('tokens')
#         super().__init__(*args, **kwargs)
#         # self.tokens = tokens
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['prompt'] = 'adverbs always'
#         return kwargs


