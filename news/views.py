from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import News


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    fields = ('title', 'text', 'image', 'is_published')
    success_url = reverse_lazy('news:list')

    def form_valid(self, form):
        if form.is_valid():
            new_news = form.save()
            new_news.slug = slugify(new_news.title)
            new_news.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Добавление новости'
        return context_data

    def get_success_url(self):
        return reverse('news:list')


class NewsListView(ListView):
    model = News

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Новости'
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True).order_by('-data_created')
        return queryset


class NewsDetailView(DetailView):
    """Контроллер просмотра отдельной новости"""
    model = News

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object.title
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    fields = ('title', 'text', 'image', 'is_published')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование новости'
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_news = form.save()
            new_news.slug = slugify(new_news.title)
            new_news.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('news:view', args=[self.kwargs.get('pk')])


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('news:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление новости'
        return context_data
