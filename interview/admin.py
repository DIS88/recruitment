from django.contrib import admin, messages
from django.http import HttpResponse
from django.db.models import Q
from django.utils.safestring import mark_safe

from interview.models import Candidate
import interview.condicate_fieldset as cf
from jobs.models import Resume


from interview import dingtalk #改为异步
from .tasks import send_dingtalk_message

# Register your models here.
import logging
import csv
from datetime import datetime

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result',
                     'first_interviewer_user', 'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')


##通知一面面试
def notify_interviewver(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""
    for obj in queryset:
        print("obj",obj)
        candidates = obj.username + ";" + candidates
        if obj.first_interviewer_user:
            interviewers = obj.first_interviewer_user.username + ";" + interviewers
    # dingtalk.send("候选人 %s 进入面试环节，请面试官准备好 %s" % (candidates, interviewers))
    send_dingtalk_message.delay("候选人 %s 进入面试环节，请面试官准备好 %s" % (candidates, interviewers)) #celery发送
    messages.add_message(request, messages.INFO, '成功发送面试通知' )


notify_interviewver.short_description = "发送面试通知"

def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv', charset='utf-8-sig') #windows
    field_list =exportable_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )
    
    writer = csv.writer(response)
    writer.writerow(
        [ queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )
    
    for obj in queryset:
        csv_line_values = []
        for field in field_list:
            field_obejct = queryset.model._meta.get_field(field)
            field_value = field_obejct.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
        
    logger.error("%s exported %s candidate records " % (request.user, len(queryset)))
    
    return response

# export_model_as_csv.__str__ = u"导出csv文件"
export_model_as_csv.short_description = "导出csv文件"
export_model_as_csv.allowed_permissions = ('export',)

def test():
    pass
    

class CandicateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')
    
    actions = [export_model_as_csv, notify_interviewver]
    
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))
    
    list_display = (
        "username", "city", "bachelor_school", "get_resume", "first_score", "first_result", "first_interviewer_user",
        "second_result", "second_interviewer_user", "hr_score", "hr_result", "last_editor"
    )
    
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user',)
    
    search_fields = ('username', 'city', 'phone', 'email', 'bachelor_school')
    
    ordering = ("hr_result", "second_result", "first_result")
    
    default_list_editable = ('first_interviewer_user', 'second_interviewer_user')
    
    # readonly_fields = ('first_interviewer_user', 'second_interviewer_user')
    # def _get_list_editable_queryset(self, request, prefix):
    #     group_names = self.get_group_names(request.user)
    #
    #     if request.user.is_superuser or 'hr' in group_names:
    #         return self.default_list_editable
    #     return ()
    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resume = Resume.objects.filter(phone=obj.phone)
        if resume and len(resume) > 0:
            return  mark_safe(u'<a href="/resume/%s" target="_blank">%s</a' % (resume[0].id, "查看简历"))
        return ""
    
    get_resume.short_description = "查看简历"
    get_resume.allow_tags = True
    
    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandicateAdmin, self).get_changelist_instance(request)
    
    def get_list_editable(self, request):
        
        group_names = self.get_group_names(request.user)
        
        if request.user.is_superuser or 'hr' in group_names:
            return self.default_list_editable
        return ()
    
    
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names
    
    def get_queryset(self, request):
        qs = super(CandicateAdmin, self).get_queryset(request)
        
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )
    
    def get_readonly_fields(self, request, obj=None):
        group_name = self.get_group_names(request.user)
        
        if 'interviewer' in group_name:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        
        return ()
    

    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        
        if "interviewer" in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if "interviewer" in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        
        return cf.default_fieldsets
    
admin.site.register(Candidate, CandicateAdmin)