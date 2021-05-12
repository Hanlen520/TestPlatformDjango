from django.db import models


# Create your models here.
class UIProject(models.Model):
    """
    项目表
    """
    ui_project_name = models.CharField("UI项目名称", max_length=50, null=False)
    describe = models.TextField("描述", default="", max_length=2000, null=True)
    status = models.BooleanField("状态", default=1)
    updata_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.ui_project_name

