import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import Vacancy
from .forms import VacancyForm
from django.utils.html import strip_tags
from django.http import HttpResponse

def parse_jooble(request):
    api_key = "92acd723-db0d-460e-beb9-194e4e8462a3"
    url = f"https://ua.jooble.org/api/{api_key}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "keywords": "Python",
        "location": "Україна"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            vacancies_inserted = 0
            
            for item in data.get('jobs', []):
                vacancy, created = Vacancy.objects.get_or_create(
                    source_url=item.get('link'),
                    defaults={
                        'title': item.get('title'),
                        'company': item.get('company', 'Не вказано'),
                        'location': item.get('location', 'Дистанційно'),
                        'salary': item.get('salary', 'Не вказана'),
                        'description': strip_tags(item.get('snippet', 'Опис відсутній...')),
                    }
                )
                if created:
                    vacancies_inserted += 1
                    
            return HttpResponse(f"Успішно імпортовано {vacancies_inserted} нових вакансій!")
        else:
            return HttpResponse(f"Помилка API: статус {response.status_code}", status=400)
    except Exception as e:
        return HttpResponse(f"Сталася помилка при запиті: {e}", status=500)
    


def vacancy_list(request):
    qs = Vacancy.objects.all()
  
    search_query = request.GET.get('q', '')
    if search_query:
        qs = qs.filter(title__icontains=search_query) | qs.filter(description__icontains=search_query)
    
    paginator = Paginator(qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'vacancies/index.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def vacancy_detail(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'vacancies/detail.html', {'vacancy': vacancy})


def vacancy_create(request):
    if request.method == "POST":
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacancy_list')
    else:
        form = VacancyForm()
    return render(request, 'vacancies/form.html', {'form': form, 'title': 'Додати вакансію'})


class VacancyUpdateView(UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'vacancies/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редагувати вакансію"
        return context
        
    def get_success_url(self):
        return reverse_lazy('vacancy_detail', kwargs={'pk': self.object.pk})


class VacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = 'vacancies/delete.html'
    success_url = reverse_lazy('vacancy_list')