from django.contrib import admin
from .models import Choice, Question, QuestionCopy, ChoiceCopy
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class ChoiceInlineCopy(admin.TabularInline):
    model = ChoiceCopy
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_editable = ('question_text',)
    list_display_links = ('pub_date',)  # Outros campos para links na listagem
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
    # Método para ação personalizada
    def change_to_others(self, request, queryset):
        for item in queryset:
            item.question_text = 'Others'  # Aumenta o preço em 10%
            item.save()
    # Adicione a ação ao admin
    actions = ['change_to_others']

class QuestionCopyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInlineCopy]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'edit_button')
    list_display_links = ('question_text','pub_date',)  # Outros campos para links na listagem
    list_filter = ['pub_date']  
    search_fields = ['question_text'] 
    def edit_button(self, obj):
        url = reverse('admin:polls_questioncopy_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Edit Button</a>', url)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context)



admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(QuestionCopy, QuestionCopyAdmin)