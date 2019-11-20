from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Employee, ConfigWeekly, Project, WeeklyRecords
import hashlib
from datetime import datetime


def mdpwd(arg):
    md5_pwd = hashlib.md5(bytes("admin", encoding="utf-8"))
    md5_pwd.update(bytes(arg, encoding="utf-8"))
    return md5_pwd.hexdigest()


class WeeklySaveDate:
    # 该方法将要被删除
    # @staticmethod
    # def save_weekly(request):
    #     try:
    #         weekly = Weekly()
    #         weekly.weeklyNumber = request.POST.get("weeklyNumber")
    #         weekly.timeLimit = request.POST.get("timeLimit")
    #         weekly.department = request.POST.get("department")
    #         weekly.username = request.POST.get('username')
    #         weekly.local_weeky = request.POST.get('local_weeky')
    #         weekly.next_plan = request.POST.get('next_plan')
    #         weekly.exist_problem = request.POST.get('exist_problem')
    #         weekly.save()
    #         return 1
    #     except Exception as e:
    #         print(e)
    #         return 0

    # Employee Information maintenance data saving
    # View data
    @staticmethod
    def view_employee(request):
        return Employee.objects.all()

    # save and alter data
    @staticmethod
    def save_employee(request, operation_type):
        try:
            if operation_type == "save":
                em = Employee()
                em.email = request.POST.get("email")
                em.password = mdpwd(request.POST.get("password"))
            elif operation_type == "alter":
                email = request.POST.get("email")
                em = Employee.objects.get(email=email)
                # Determine whether the user's password is modified
                if em.password != request.POST.get("password"):
                    em.password = mdpwd(request.POST.get("password"))
                # Determine if an account exists
                if not Employee.objects.get(email=request.POST.get("email")):
                    return HttpResponse("<li>- User account exist, please check it.</li>"
                                        "<li>- Employee matching query does not exist.</li>")
            em.company_name = request.POST.get("company_name")
            em.department = request.POST.get("department")
            em.role = request.POST.get("role")
            em.username = request.POST.get("emplayeeName")
            em.save()
            return 1
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def save_weekly_new(request):
        try:
            record = WeeklyRecords()
            record.username = request.POST.get("username")
            record.weeklyNumber = request.POST.get("weeklyNumber")
            record.timeLimit = request.POST.get("timeLimit")
            record.department = request.POST.get("department")
            record.work_this_week = request.POST.getlist("work_content")
            record.next_week_plan = request.POST.getlist("next_plan")
            record.work_this_week = request.POST.getlist("work_content")
            record.next_week_plan = request.POST.getlist("next_plan")
            record.problems_in_work = request.POST.get("problems_in_work")
            record.save()
        except Exception as e:
            print(e)
            return HttpResponse("<li>- User account exist, please check it.</li>"
                                "<li>- Employee matching query does not exist.</li>")

    # Configuration information maintenance data saving
    @staticmethod
    def save_config(request):
        conf = ConfigWeekly()
        conf.weeklyNumber = request.POST.get("weeklyNo")
        conf.timeLimit = request.POST.get("timeLimit")
        conf.weeklySubmit = request.POST.get("status")
        conf.save()

    # Project information mantenance data saving
    @staticmethod
    def save_project(request, operation_type):
        if 'add' == operation_type:
            project = Project()
            project.project_number = request.POST.get("project_number")
            project.project_name = request.POST.get("project_name")
            project.project_start_time = datetime.strptime(request.POST.get("project_start_time"), "%Y-%m-%d")
        elif 'alter' == operation_type:
            try:
                project = Project.objects.get(project_number=request.POST.get("project_number"))
            except Exception as e:
                print(e)
                raise
        project.project_end_time = datetime.strptime(request.POST.get("project_end_time"), "%Y-%m-%d")
        project.save()
        print("project save/alter success.")
        return 0


class PublicInformation:
    @staticmethod
    def authenticate(request):
        try:
            # 通过验证session的email和密码，判断是否有过登陆;
            # 如果用户已经登陆，返回用户的登陆信息；
            if request.session.get("loginModel", False):
                base_informations = {}
                email = (request.session["loginModel"]).email
                password = (request.session["loginModel"]).password
                # user_info = Employee.objects.filter(email=email, password=password)
                user_info = Employee.objects.get(email=email, password=password)
                # 人员信息
                base_informations["username"] = user_info.username
                base_informations["role"] = user_info.role
                base_informations["title"] = "WEEKLY APP"
                # 项目信息
                base_informations["projects"] = Project.objects.all().values("project_name")
                return base_informations
            return False
        except Exception as e:
            print(e)
            return False

def logout(request):
    request.session.clear()
    request.session.flush()
    return HttpResponseRedirect('/')