from django.contrib import admin
from polls.models import Poll, Question, Choice
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Permission)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
class PollAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_date', 'end_date', 'del_flag']
    list_per_page = 10

    list_filter = ['start_date', 'end_date', 'del_flag']
    search_fields = ['title']

    # field = ['title', 'del_flag'] #จะเอา field ไหนบ้างที่แก้ไข
    # #exclude =  #จะไม่เอา field ไหน
    fieldsets = [#แบ่งกลุ่มหน้า UI
        (None, {'fields': ['title', 'del_flag']}),
        ("Active Duration", {'fields': ['start_date', 'end_date']})
    ]

    inlines = [QuestionInline]
admin.site.register(Poll, PollAdmin)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'poll', 'text']
    list_per_page = 15

    list_filter = ['poll']
    search_fields = ['text', 'poll']
    inlines = [ChoiceInline]
admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text', 'value']
    list_per_page = 15

    list_filter = ['question']
    search_fields = ['question', 'text']
admin.site.register(Choice, ChoiceAdmin)
