from django.shortcuts import render
from django.http import HttpResponse
import io
import sys
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import unittest
from django.http import HttpResponse
import io
import sys
import unittest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CodeSubmission
from django.utils import timezone

# set your key here
# openai.api_key = ''

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginView(LoginView):
    template_name = 'code_submission/login.html'  # 指定登录页面的模板
    redirect_authenticated_user = True
    next_page = reverse_lazy('submit_code')  # 登录成功后重定向的页面

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from collections import defaultdict
import json
from .models import CodeSubmission  # 确保引用了正确的模型

def home(request):
    # 清理过期会话数据
    from django.core.management import call_command
    call_command("clearsessions")

    # 获取当前在线用户数量
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    online_users = 0
    user_ids = []

    for session in sessions:
        data = session.get_decoded()
        if data.get("_auth_user_id"):
            user_ids.append(data.get("_auth_user_id"))

    # 确保在线用户唯一
    user_ids = list(set(user_ids))
    online_users = len(user_ids)

    # 获取总注册用户数
    total_users = User.objects.count()

    # 防止total_users小于online_users的情况
    registered_users = max(total_users - online_users, 0)

    # 获取提交次数和日期
    submissions = CodeSubmission.objects.values("submission_time")
    submission_count = submissions.count()

    # 按日期统计提交次数
    submission_dates = defaultdict(int)
    for submission in submissions:
        date = submission["submission_time"].date()
        submission_dates[date] += 1
    
    # 只保留最近七天的提交数据 未提交数据为0
    for i in range(1, 8):
        print(i)
        date = timezone.now().date() - timezone.timedelta(days=i)
        if date not in submission_dates:
            submission_dates[date] = 0

    # 转换为列表以便在模板中使用
    sorted_dates = sorted(submission_dates.items())
    dates = [date.strftime("%Y-%m-%d") for date, count in sorted_dates]
    counts = [count for date, count in sorted_dates]

    context = {
        "online_users": online_users,
        "total_users": total_users,
        "registered_users": registered_users,
        "submission_count": submission_count,
        "submission_dates": json.dumps(dates),  # 传递日期列表
        "submission_counts": json.dumps(counts),  # 传递提交次数列表
    }
    print(context)
    return render(request, "home.html", context)


class SignUpView(View):
    form_class = SignUpForm
    template_name = 'code_submission/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user
            return redirect('submit_code')  # Redirect to a success page
        return render(request, self.template_name, {'form': form})

@login_required
def submit_code(request):
    if request.method == 'POST':
        print("Received POST request")  # 检查是否打印
        code_content = request.POST.get('code', '')
        test_code = request.POST.get('test_code', '')

        if code_content and test_code:
            # 创建一个字符串流来捕获输出
            buffer = io.StringIO()
            sys.stdout = buffer  # 重定向标准输出到 buffer

            # 创建执行环境
            exec_environment = {}
            try:
                # 尝试执行用户的代码
                exec(code_content, exec_environment)
            except Exception as e:
                # 捕获执行用户代码时的任何异常（包括语法错误）
                return render(request, 'code_submission/submit_form.html', {
                    'output': f"An error occurred: {str(e)}",
                    'code': code_content,
                    'test_code': test_code,
                    'output_starts_with_failed': True
                })

            try:
                # 执行用户的测试代码
                exec(test_code, exec_environment)

                # 创建测试套件
                suite = unittest.TestSuite()
                # 加载测试用例
                for name, obj in exec_environment.items():
                    if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(obj))

                # 运行测试
                result = unittest.TextTestRunner(stream=buffer, verbosity=2).run(suite)

                # 检查测试结果并决定输出
                output = buffer.getvalue()
                output_starts_with_failed = not result.wasSuccessful()
                output = "Pass!" if result.wasSuccessful() else f"Failed!\n{output}"

                submission = CodeSubmission(user=request.user, code=code_content, test_code=test_code, output = output)
                submission.save()

            except Exception as e:
                output = f"An error occurred: {str(e)}"
                output_starts_with_failed = True

            finally:
                # 恢复标准输出
                sys.stdout = sys.__stdout__
            print(output)
            return render(request, 'code_submission/submit_form.html', {
                'output': output,
                'code': code_content,
                'test_code': test_code,
                'output_starts_with_failed': output_starts_with_failed
            })
        else:
            return HttpResponse("Please provide both code and test code.", status=400)
    else:
        # 如果是 GET 请求，渲染提交表单
        return render(request, 'code_submission/submit_form.html')

@login_required
@csrf_exempt
def generate_test_code(request):
    print("request received")
    if request.method == 'POST':
        body = json.loads(request.body)
        code_content = body.get('code', '')

        if not code_content:
            return JsonResponse({'error': 'No code provided'}, status=400)

        try:
            # 调用 OpenAI GPT API 生成测试代码
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  
                #messages=[
                #    {"role": "system", "content": "Please only provide the test code for the following function without any other words"},
                #    {"role": "user", "content": f" Give some testing code for the following function in python and output the response:\n\n{code_content}\n\n# Test code:"}
                #]
                messages=[
                {"role": "system", "content": "Please **only** provide the test code for the following function without any other words"},
                {"role": "user", "content": f"Generate Python unittest code for the following function:\n\n{code_content}\n\n# Test code:"}
            ]
            )

            test_code = response.choices[0].message.content.strip()
            # 过滤掉开头的''' Python 和结尾的'''
            test_code = test_code.replace("```python", "").replace("```", "").strip()
            # 过滤掉if __name__ == '__main__':以及后面的内容
            # test_code = test_code.split("if __name__ == '__main__':")[0].strip()
            print(test_code)
            return JsonResponse({'test_code': test_code})

        except Exception as e:
            # 捕获所有错误
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def auto_debug(request):
    print("Auto-debug endpoint hit")  # 确认端点被触达
    if request.method == 'POST':
        print("POST request received")  # 确认接收到POST请求
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            test_code = data.get('test_code', '')
            error_message = data.get('error_message', '')

            # 调用 OpenAI API 以修复代码
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  
                messages=[
                    {"role": "system", "content": "Please **only** provide a code fix based on the error message and test cases without any other words."},
                    {"role": "user", "content": f"Original Code:\n{code}\nTest Code:\n{test_code}\nError:\n{error_message} and only output the fixed original code."}
                ]
            )

            fixed_code = response.choices[0].message.content.strip()
            return JsonResponse({'debugged_code': fixed_code})

        except Exception as e:
            print(f"Error during processing: {e}")
            return JsonResponse({'error': 'Failed to process the request'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
