from django.contrib import admin

from .models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User

# class ProfileInline(admin.TabularInline):
#     model = Profile


# class UserAdmin(DjangoUserAdmin):
#     inlines = [ ProfileInline,]

# admin.site.register(User, UserAdmin)
admin.site.register(User)


admin.site.register(Profile)

admin.site.register(Classes)
admin.site.register(Quiz)
admin.site.register(Tutor)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Student)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author',
		'status')
	list_filter = ('status', 'created_on', 'author')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('author',)
	ordering = ['status', '-created_on']

class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'body')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
