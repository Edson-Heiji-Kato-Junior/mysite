from django.contrib import admin
from .models import Choice, Question

from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']  
    search_fields = ['question_text'] 
    
    # Método para ação personalizada
    def new_page_view(self, request):
        url_referencia = request.META.get('HTTP_REFERER')
        return render(request, 'admin/new_page.html', {'url_referencia': url_referencia} )

    # Método para adicionar URL personalizada
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('new_page/', self.admin_site.admin_view(self.new_page_view), name='new_page'),
        ]
        return custom_urls + urls


    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)