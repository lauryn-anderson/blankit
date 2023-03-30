from django.views.generic import TemplateView
from django.views.generic import FormView
from.text_processing import preprocess_text

from .forms import TextInputForm


class HomePageView(TemplateView):
    template_name = 'home.html'


class TextInputView(FormView):
    template_name = 'text.html'
    form_class = TextInputForm
