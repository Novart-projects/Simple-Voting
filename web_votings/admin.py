from django.contrib import admin

from .models import AllVotings, Answers, UsersAnswers, Complaint

class AllVotingsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "type", "creator_id", "number_of_questions")
    search_fields = ("text",)
    #list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class AnswersAdmin(admin.ModelAdmin):
    list_display = ("id", "answer_variant", "question", "number_of_p_chosen")
    search_fields = ("title",)
    empty_value_display = "-пусто-"

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "theme", "desc", "stat", 'creator', 'vote', 'ans')
    search_fields = ("title",)
    empty_value_display = "-пусто-"

class UserAnswersAdmin(admin.ModelAdmin):
    list_display = ("id", "answer", "user")
    search_fields = ("text",)
    empty_value_display = "-пусто-"
admin.site.register(AllVotings, AllVotingsAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(UsersAnswers, UserAnswersAdmin)
admin.site.register(Complaint, ComplaintAdmin)
# Register your models here.
