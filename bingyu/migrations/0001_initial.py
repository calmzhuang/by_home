# Generated by Django 2.1.7 on 2019-03-20 04:25

import bingyu.models
from django.db import migrations, models
import django.db.models.deletion
import time


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.CharField(default=bingyu.models.next_id, max_length=50, primary_key=True, serialize=False, verbose_name='用户id')),
                ('name', models.CharField(max_length=50, verbose_name='标题')),
                ('summary', models.CharField(max_length=200, verbose_name='摘要')),
                ('content', models.TextField(verbose_name='内容')),
                ('created_at', models.FloatField(default=time.time, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '日志表',
                'verbose_name_plural': '日志表',
                'db_table': 'blogs',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(default=bingyu.models.next_id, max_length=50, primary_key=True, serialize=False, verbose_name='评论id')),
                ('content', models.TextField(verbose_name='评论')),
                ('created_at', models.FloatField(default=time.time, verbose_name='创建时间')),
                ('blog_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingyu.Blog', verbose_name='日志')),
            ],
            options={
                'verbose_name': '评论表',
                'verbose_name_plural': '评论表',
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Envelope',
            fields=[
                ('id', models.CharField(default=bingyu.models.next_id, max_length=50, primary_key=True, serialize=False, verbose_name='寄语id')),
                ('remarks', models.TextField(verbose_name='寄语')),
                ('postcards', models.CharField(max_length=500, verbose_name='明信片')),
                ('created_at', models.FloatField(default=time.time, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '寄语表',
                'verbose_name_plural': '寄语表',
                'db_table': 'envelope',
            },
        ),
        migrations.CreateModel(
            name='TimeFragment',
            fields=[
                ('id', models.CharField(default=bingyu.models.next_id, max_length=50, primary_key=True, serialize=False, verbose_name='时光id')),
                ('introduction', models.CharField(max_length=50, verbose_name='简介')),
                ('weather', models.CharField(max_length=200, verbose_name='天气')),
                ('album_url', models.CharField(max_length=500, verbose_name='时光')),
                ('created_at', models.FloatField(default=time.time, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '时光表',
                'verbose_name_plural': '时光表',
                'db_table': 'time_fragment',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(default=bingyu.models.next_id, max_length=50, primary_key=True, serialize=False, verbose_name='用户id')),
                ('email', models.CharField(max_length=50, verbose_name='用户邮箱')),
                ('passwd', models.CharField(max_length=50, verbose_name='用户密码')),
                ('admin', models.BooleanField(verbose_name='管理员标识')),
                ('name', models.CharField(max_length=50, verbose_name='用户名称')),
                ('image', models.CharField(max_length=50, verbose_name='用户图像')),
                ('created_at', models.FloatField(default=time.time, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '用户信息表',
                'verbose_name_plural': '用户信息表',
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='timefragment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingyu.User', verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='envelope',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingyu.User', verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingyu.User', verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingyu.User', verbose_name='作者'),
        ),
    ]
