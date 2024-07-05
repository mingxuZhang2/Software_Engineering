from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Submission(models.Model):
    code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class CodeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    code = models.TextField(verbose_name="提交的代码")
    test_code = models.TextField(verbose_name="测试代码")
    output = models.TextField(verbose_name="输出")
    submission_time = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")

    def __str__(self):
        return f"{self.user.username} - {self.submission_time.strftime('%Y-%m-%d %H:%M:%S')}"
