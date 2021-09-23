from django.contrib import admin
from .models import Problem, Rating, Comment

@admin.action(description='Archive selected problems')
def archive(modeladmin, request, queryset):
    queryset.update(is_archived=True)

@admin.action(description='Unarchive selected problems')
def unarchive(modeladmin, request, queryset):
    queryset.update(is_archived=False)

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'subject', 'is_archived')
    search_fields = ('id', 'title', 'author', 'problem_text', 'answer', 'solution')
    list_filter = ('subject', 'is_archived')
    actions = [archive, unarchive]

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Rating)
admin.site.register(Comment)
