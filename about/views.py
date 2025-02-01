# 1. Django и сторонние библиотеки
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

# 2. Импорты из проекта
from about.models import About


@method_decorator(cache_page(60 * 15), name='dispatch')
class AboutListView(ListView):
    model = About
    template_name = 'about/index.html'
    context_object_name = 'abouts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context
