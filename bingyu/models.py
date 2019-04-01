import time
import uuid
from django.db import models

# Create your models here.


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(models.Model):

    id = models.CharField(max_length=50, null=False, default=next_id, primary_key=True, verbose_name="用户id")
    email = models.CharField(max_length=50, verbose_name="用户邮箱")
    passwd = models.CharField(max_length=50, verbose_name="用户密码")
    admin = models.BooleanField(verbose_name="管理员标识")
    name = models.CharField(max_length=50, verbose_name="用户名称")
    image = models.CharField(max_length=500, verbose_name="用户图像")
    created_at = models.FloatField(default=time.time, verbose_name="创建时间")

    class Meta:
        db_table = "users"
        verbose_name = '用户信息表'
        verbose_name_plural = '用户信息表'

    def __str__(self):
        return self.name


class Blog(models.Model):

    id = models.CharField(max_length=50, null=False, default=next_id, primary_key=True, verbose_name="用户id")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='作者')
    name = models.CharField(max_length=50, verbose_name="标题")
    summary = models.CharField(max_length=2000, verbose_name="摘要")
    content = models.TextField(verbose_name="内容")
    created_at = models.FloatField(default=time.time, verbose_name="创建时间")

    class Meta:
        db_table = "blogs"
        verbose_name = '日志表'
        verbose_name_plural = '日志表'

    def __str__(self):
        return self.name


class TimeFragment(models.Model):

    id = models.CharField(max_length=50, null=False, default=next_id, primary_key=True, verbose_name="时光id")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='作者')
    introduction = models.CharField(max_length=50, verbose_name="简介")
    weather = models.CharField(max_length=200, verbose_name="天气")
    album_url = models.CharField(max_length=500, verbose_name="时光")
    created_at = models.FloatField(default=time.time, verbose_name="创建时间")

    class Meta:
        db_table = "time_fragment"
        verbose_name = '时光表'
        verbose_name_plural = '时光表'

    def __str__(self):
        return self.introduction


class Envelope(models.Model):

    id = models.CharField(max_length=50, null=False, default=next_id, primary_key=True, verbose_name="寄语id")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='作者')
    remarks = models.TextField(verbose_name="寄语")
    postcards = models.CharField(max_length=500, verbose_name="明信片")
    created_at = models.FloatField(default=time.time, verbose_name="创建时间")

    class Meta:
        db_table = "envelope"
        verbose_name = '寄语表'
        verbose_name_plural = '寄语表'

    def __str__(self):
        return self.remarks


class Comment(models.Model):

    id = models.CharField(max_length=50, null=False, default=next_id, primary_key=True, verbose_name="评论id")
    blog_id = models.ForeignKey("Blog", on_delete=models.CASCADE, verbose_name='日志')
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField(verbose_name="评论")
    created_at = models.FloatField(default=time.time, verbose_name="创建时间")

    class Meta:
        db_table = "comments"
        verbose_name = '评论表'
        verbose_name_plural = '评论表'

    def __str__(self):
        return self.content