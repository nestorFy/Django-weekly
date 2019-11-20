from django import forms
from .models import UserProfile

class LoginForm(forms.Form):
    """ Login form Auth"""

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, max_length=3)

class RegisterForm(forms.Form):
    """
    注册验证表单
    """
    username = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    # password = forms.CharField(max_length='64', default='123450')
    # captcha = CaptchaField()

class UserForm(forms.ModelForm):
    department_list = (
        ('d00001', 'Development Department'),
        ('d00002', 'Operation and maintenance Department'),
        ('d00003', 'Product Department'),
        ('d00004', 'Testing Division')
    )

    position_list = (
        ('p00001', 'Boos'),
        ('p00002', 'Manager'),
        ('p00003', 'workers')
    )

    # style
    password = forms.CharField(
        # 密码为123456
        # initial=u'pbkdf2_sha256$150000$ROE3axgEjODB$UCNWPhTQACJBom+wtaqsABkOvP1LsHicQLlPCSfFUvA='
        # initial='123456',
    )

    department = forms.CharField(max_length=64, widget=forms.widgets.Select(choices=department_list),
                                 help_text="Select the department where the new user is located,which can be modified later",
                                 required=True)

    position = forms.CharField(max_length=64, widget=forms.widgets.Select(choices=position_list),
                                 help_text="Select the position where the new user is located,which can be modified later",
                               required=True)
    class Meta:
        model = UserProfile
        # fields = "__all__"
        fields = ['username', 'email', 'department', 'position', 'password']
        labels = {'username': 'username', 'email': 'email', 'department': 'department', 'position':'position'}
        error_messages = {
            'username': {'required': 'not null'},
            'email': {'required': 'not null'}
        }


