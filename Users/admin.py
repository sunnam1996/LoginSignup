from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Question, Choice, Guess, QuizAppUser, Category, Quiz
from .forms import RegistrationForm


class CustomUserAdmin(UserAdmin):
    add_form = RegistrationForm
    model = QuizAppUser
    list_display = ['username', 'email', 'first_name', 'last_name','profile_image']


admin.site.register(QuizAppUser, CustomUserAdmin)


class ChoiceAdmin(admin.TabularInline):
    model = Choice
    classes = ('grp-collapse grp-open',)
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceAdmin]


admin.site.register(Guess)

admin.site.register(Category)

admin.site.register(Quiz)
