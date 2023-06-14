from django.contrib import admin
from .models import Person, Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    exclude = ['slug']


admin.site.register(Person)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
