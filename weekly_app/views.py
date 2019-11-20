# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from .models import Employee as em, ConfigWeekly
from .models import Project, WeeklyRecords
from .expansions import mdpwd
from .expansions import WeeklySaveDate, PublicInformation
import datetime, time

class LoginView(View):
    title = "Weekly Login"
    loginStatus = ""
    content = {"title": title, "loginStatus": loginStatus}

    def get(self, request):
        return render(request, 'weekly/login.html', self.content)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            record = em.objects.filter(
                email=email, password=mdpwd(password)
            ).count()
            if record == 1:
                user = em.objects.get(email=email, password=mdpwd(password))
                request.session["loginModel"] = user
                return HttpResponseRedirect('/index')
            else:
                self.content["loginStatus"] = "用户名或密码错误."
                return render(request, 'weekly/login.html', self.content)


def index(request):
    # 首页显示
    content = PublicInformation.authenticate(request)
    if not content: return HttpResponseRedirect('/')

    content["total_people"] = em.objects.all().count()
    # the last configuration
    content["rec_weekly_condition"] = "第%s期周报" % (ConfigWeekly.objects.all().last().weeklyNumber)
    content["number_of_weekly_reports"] = WeeklyRecords.objects.filter(weeklyNumber=content["rec_weekly_condition"]).count()
    content["number_of_people_not_submitted"] = content["total_people"] - content["number_of_weekly_reports"]
    weekly_records = WeeklyRecords.objects.filter(weeklyNumber=content["rec_weekly_condition"]).order_by("-weekly_submit_time")

    content["index_content"] = {}
    for rec in weekly_records:
        work = []
        work_content = eval(rec.work_this_week)
        for i in range(0, len(work_content), 3):
            work.append(work_content[i] + " - " + work_content[i + 1] + " - (进度" + work_content[i + 2] + "%)")
        plan = []
        plan_next = eval(rec.next_week_plan)
        for i in range(0, len(plan_next), 2):
            plan.append(plan_next[i]+ " - " + plan_next[i+1])
        question = rec.problems_in_work
        content["index_content"][rec.username] = {"work": work, "plan": plan, "question": question}

    return render(request, 'weekly/index.html', content)


def weekly_index(request):
    content = PublicInformation.authenticate(request)
    if not content: return HttpResponseRedirect('/')

    # if type_id == "writting":
    #     # sumit weekly content, operater save method
    #     if request.method == "POST":
    #         WeeklySaveDate.save_weekly(request)
    #         return HttpResponseRedirect(reverse('weekly_app:weekly',
    #                                             kwargs={"type_id": "weeklyView"}))
    #     weekly_content = ConfigWeekly.objects.all().values().last()
    #     department_no = request.session["loginModel"].department
    #     # print request.META['HTTP_HOST']
    #     # print request.META['REMOTE_ADDR'].split(':')[0]
    #     for department in em.department_list:
    #         if department_no in department:
    #             department = department
    #             break
    #     content = {'type_id': type_id, "weekly_content": weekly_content,
    #                'department': department, "username": username}
    #     try:
    #         # Read whether weekly reports have been submitted this week,
    #         # and some are extracted to the front desk, and can only be
    #         # read and not vented, otherwise fill in.
    #         content["local_weeky"] = 'null'
    #         content["next_plan"] = "null"
    #         period_number = ConfigWeekly.objects.all().last().weeklyNumber
    #         weekly_number = u'第%s期周报' % period_number
    #         record_weekly = Weekly.objects.filter(username=username, weeklyNumber=weekly_number).values(
    #             'local_weeky', 'next_plan', 'exist_problem')
    #         if record_weekly.count() == 1:
    #             content["readonly"] = True
    #             for record in record_weekly:
    #                 content["local_weeky"] = record["local_weeky"]
    #                 content["next_plan"] = record["next_plan"]
    #                 content["exist_problem"] = record["exist_problem"]
    #         else:
    #
    #             weekly_number = u'第%s期周报' % (int(period_number) - 1)
    #             record_weekly = Weekly.objects.filter(username=username, weeklyNumber=weekly_number).values("next_plan")
    #             if record_weekly.count() == 1:
    #                 content["readonly1"] = True
    #                 for record in record_weekly:
    #                     content["last_record"] = record["next_plan"]
    #     except Exception as e:
    #         raise e
    #     return render(request, 'weekly/weekly.html', content)
    # elif type_id == 'explanation':
    #     content = {'type_id': type_id, "username": username,
    #                }
    #     return render(request, 'weekly/weekly.html', content)
    return render(request, 'weekly/weekly.html')


# Weekly Module
# Past weekly report records
def weekly_list(request):
    content = PublicInformation.authenticate(request)
    if not content: return HttpResponseRedirect('/')

    content["type_id"] = "weekList"
    content["weekly_records"] = WeeklyRecords.objects.filter(username=content["username"]).order_by("weeklyNumber").reverse()

    return render(request, 'weekly/weekly.html', content)


def weekly_content_writting(request):
    content = PublicInformation.authenticate(request)
    if not content: return HttpResponseRedirect('/')

    # 页面显示标签设定
    content["type_id"], content["subtitle"]= "writting", "add"

    # 周报记录提交数据保存
    if request.POST:
        WeeklySaveDate.save_weekly_new(request)
        return redirect(reverse("weekly_app:weekly_list"))

    department_no = request.session["loginModel"].department
    for department in em.department_list:
        if department_no in department:
            content["department"] = department
            break
    content["record"] = ConfigWeekly.objects.all().values().last()

    # Determine if the weekly record has been submitted.
    weeklyNumber = "第%s期周报" % (content["record"]["weeklyNumber"])
    count = WeeklyRecords.objects.filter(weeklyNumber=weeklyNumber, username=content["username"]).count()
    if count == 1:
        return HttpResponseRedirect(reverse('weekly_app:weekly_content_view',
                kwargs={"weekly_id": weeklyNumber}))

    return render(request, 'weekly/weekly.html', content)


# 周报内容展示
def weekly_content_view(request, weekly_id):
    content = PublicInformation.authenticate(request)
    if not content: return HttpResponseRedirect('/')

    # 页面显示标签设定
    content["type_id"], content["subtitle"] = "writting", "view"

    # 周报内容提取[周报记录、本周工作、下周计划]
    content["weekly_content"], content["plan_content"]= [],[]
    content["record"] = WeeklyRecords.objects.get(username=content["username"], weeklyNumber=weekly_id)
    for i in range(0, len(eval(content["record"].work_this_week)), 3):
        content["weekly_content"].append(eval(content["record"].work_this_week)[i: i + 3])
    for i in range(0, len(eval(content["record"].next_week_plan)), 2):
        content["plan_content"].append(eval(content["record"].next_week_plan)[i: i + 2])

    return render(request, 'weekly/weekly.html', content)


# 系统配置
def settings(request, set_type=""):
    # 用户
    content = PublicInformation.authenticate(request)
    if not content: return HttpResponseRedirect('/')

    content["label"] = str(set_type)

    if content["label"] == "userview":
        content["employeeList"] = WeeklySaveDate.view_employee(request)

        return render(request, 'weekly/settings.html', content)

    elif content["label"] == "userEdit":
        content["companyList"] = em.company_list
        content["departmentList"] = em.department_list
        content["roleList"] = em.personnel_role
        content["s_label"] = "add"

        # 根据用户动作进行对应操作 [ save\ alter\ delete]
        if request.POST:
            if 'save' in request.POST:
                WeeklySaveDate.save_employee(request, 'save')
            elif 'alter' in request.POST:
                WeeklySaveDate.save_employee(request, 'alter')
            elif 'delete' in request.POST:
                try:
                    em.objects.get(email=request.POST.get("email")).delete()
                    print('delete successful.')
                except Exception as e:
                    print(e)
            elif 'cancel' in request.POST:
                return HttpResponseRedirect(reverse('weekly_app:settings',
                                                    kwargs={"set_type": "userview"}))

            return HttpResponseRedirect(reverse('weekly_app:settings',
                                                kwargs={"set_type": "userview"}))

        return render(request, 'weekly/settings.html', content)

    elif content["label"] == "config":
        # 周报 cycle 设置
        cur_time = datetime.datetime.now()
        day_num = cur_time.isoweekday()
        content["monday"] = (cur_time - datetime.timedelta(days=day_num - 1)).strftime('%Y%m%d')
        content["friday"] = (cur_time - datetime.timedelta(days=day_num - 5)).strftime('%Y%m%d')
        content["weekly_cycle"] = str(time.strftime("%W"))
        content["statusList"] = ConfigWeekly.status

        if request.method == "POST":
            WeeklySaveDate.save_config(request)

        return render(request, 'weekly/settings.html', content)

    return render(request, 'weekly/settings.html', content)


#
# Project Infomation maintain
# def project_view(request):
#     label = "projectview"
#     project_lists = Project.objects.all()
#     content = {"label": label, "project_lists": project_lists}
#     return render(request, 'weekly/settings.html', content)

class ProjectViewClass(View):

    def get(self, request):
        label = "projectview"
        project_lists = Project.objects.all()
        content = {"label": label, "project_lists": project_lists}
        return render(request, 'weekly/settings.html', content)



def project_edit(request, edit_type):
    """
    Edit project Inforation, include add a project information or delete
    a exist records.
    :param request:
    :param edit_type:
    :return:
    """
    label = "projectEdit"
    content = {"label": label, "s_label": "add"}
    if request.POST:
        if 'save' in request.POST:
            WeeklySaveDate.save_project(request, 'add')
        elif 'alter' in request.POST:
            WeeklySaveDate.save_project(request, 'alter')
        elif 'delete' in request.POST:
            Project.objects.get(project_number=request.POST.get("project_number")).delete()
            print("project delete success.")
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('weekly_app:project_view'))
        return HttpResponseRedirect(reverse('weekly_app:project_view'))
    return render(request, 'weekly/settings.html', content)


def alter(request, alter_type, alter_id):
    # 统一的修改在此处编写
    """
    All Information editing
    :param request:
    :param alter_type: user. project
    :param alter_id:
    :return: Corresponding edit view
    """
    if alter_type == "user":
        content = {"companyList": em.company_list, "departmentList": em.department_list,
                   "roleList": em.personnel_role, "label": "userEdit", "s_label": "alter",
                   }
        content["user"] = em.objects.get(email=alter_id)
        return render(request, 'weekly/settings.html', content)
    elif alter_type == "project":
        project = Project.objects.get(project_number=alter_id)
        content = {"project": project, "label": "projectEdit", "s_label": "alter", }
        return render(request, 'weekly/settings.html', content)

# September 6
def process_control(request):
    content = {}
    username = request.POST.get("username")
    content["username"] = username

    return render(request, 'weekly/settings.html', content)
