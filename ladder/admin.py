from django.contrib import admin
from .models import User,Ladder,Unit,Link,LearningStatus,Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','icon','profile','password')


class LadderAdmin(admin.ModelAdmin):
    list_display = ('id','title','user','is_public','get_unit','get_recommended_next_ladder','get_recommended_prev_ladder','count_finish_number','count_learning_number')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('id','title','index','ladder','url','get_comments')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('latter','prior','user')


class LearningStatusAdmin(admin.ModelAdmin):
    list_display = ('user','unit','status','created_at','update_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','unit','user','text')

#admin.site.register(Tags)
admin.site.register(User,UserAdmin)
admin.site.register(Ladder,LadderAdmin)
admin.site.register(Unit,UnitAdmin)
admin.site.register(Link,LinkAdmin)
admin.site.register(LearningStatus,LearningStatusAdmin)
admin.site.register(Comment,CommentAdmin)
