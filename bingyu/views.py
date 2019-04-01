import hashlib

from django.shortcuts import render, HttpResponse, redirect
from bingyu.models import User, Blog, TimeFragment, Envelope, Comment, next_id
from bingyu.apis import Page, APIValueError, APIResourceNotFoundError, APIPermissionError, APIError

import re
import json


# Create your views here.
def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


def index(request):

    num = User.objects.count()
    page = Page(num)
    if num == 0:
        blogs = []
    else:
        blogs = Blog.objects.values().order_by("-created_at")[page.offset: page.limit]

    return render(request, 'blogs.html', {'page': page, 'blogs': blogs})


def get_blog(request, id):
    blog = Blog.objects.filter(id=id).values()[0]
    return render(request, 'blog.html', {'blog': blog})


def get_time(request):
    times = list(TimeFragment.objects.filter().values())
    return render(request, 'times.html', {'times': times})


def register(request):
    return render(request, 'register.html')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    elif request.method == 'POST':
        body = json.loads(request.body)
        email = body.get('email')
        passwd = body.get('passwd')
        if not email:
            return HttpResponse('请输入邮箱')
        if not passwd:
            return HttpResponse('请输入密码')
        user = User.objects.get(email=email)
        sha1 = hashlib.sha1()
        sha1.update(user.id.encode('utf-8'))
        sha1.update(b':')
        sha1.update(passwd.encode('utf-8'))
        if user.passwd != sha1.hexdigest():
            return HttpResponse('密码错误')
        request.session['user_session'] = user.id
        user.passwd = '******'
        request.session['user'] = {'name': user.name, 'admin': user.admin}
        return HttpResponse("登录成功")



def signout(request):
    request.session.flush()
    return redirect('/')


def manage(request):
    return redirect('/bingyu/manage/comments')


def manage_comments(request, page='1'):
    return render(request, 'manage_comments.html', {'page_index': get_page_index(page)})


def manage_blogs(request, page='1'):
    return render(request, 'manage_blog.html', {'page_index': get_page_index(page)})


def manage_time(request, page='1'):
    return render(request, 'manage_time.html', {'page_index': get_page_index(page)})


def manage_envelope(request, page='1'):
    return render(request, 'manage_envelope.html', {'page_index': get_page_index(page)})


def manage_create_blog(request):
    return render(request, 'manage_blog_edit.html', {'id': '', 'action': '/bingyu/api/blogs/'})


def manage_create_time(request):
    return render(request, 'manage_time_edit.html', {'id': '', 'action': '/bingyu/api/time/'})


def manage_create_envelope(request):
    return render(request, 'manage_envelope_edit.html', {'id': '', 'action': '/bingyu/api/envelope/'})


def manage_edit_blog(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        return render(request, 'manage_blog_edit.html', {'id': id, 'action': '/bingyu/api/blogs/%s/' % id})


def manage_edit_time(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        return render(request, 'manage_time_edit.html', {'id': id, 'action': '/bingyu/api/time/%s/' % id})


def manage_edit_envelope(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        return render(request, 'manage_envelope_edit.html', {'id': id, 'action': '/bingyu/api/envelope/%s/' % id})


def manage_users(request, page='1'):
    return render(request, 'manage_users.html', {'page_index': get_page_index(page)})


def api_comments(request, page='1'):
    page_index = get_page_index(page)
    num = Comment.objects.count()
    p = Page(num, page_index).page_dict()
    if num == 0:
        return HttpResponse(json.dumps(dict(page=p, comments=())))
    comments = list(Comment.objects.values().order_by('-created_at')[p.get('offset'): p.get('limit')])
    for comment in comments:
        comment['user_name'] = User.objects.get(id=comment['user_id_id']).name
    return HttpResponse(json.dumps(dict(page=p, comments=comments)))


def api_get_users(request,  page='1'):
    if request.method == 'GET':
        page_index = get_page_index(page)
        num = User.objects.count()
        p = Page(num, page_index)
        if num == 0:
            return HttpResponse(dict(page=p, users=()))
        users = User.objects.filter().order_by('-create_at')[p.get('offset'): p.get('limit')]
        for u in users:
            u.passwd = '******'
        return HttpResponse(dict(page=p, users=users))
    elif request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        email = body.get('email')
        passwd = body.get('passwd')
        if not name or not name.strip():
            return HttpResponse('名称不可为空')
        if not email or not _RE_EMAIL.match(email):
            return HttpResponse('邮箱不可为空')
        if not passwd or not _RE_SHA1.match(passwd):
            return HttpResponse('密码不可为空')
        users = User.objects.filter(email=email)
        if len(users) > 0:
            return HttpResponse('邮箱已注册')
        uid = next_id()
        sha1_passwd = '%s:%s' % (uid, passwd)
        dic = {
            'id': uid,
            'name': name.strip(),
            'email': email,
            'passwd': hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
            'image': 'http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest(),
            'admin': 0
        }
        user = User.objects.create(**dic)
        # make session cookie:
        request.session['user_session'] = uid
        user.passwd = '******'
        request.session['user'] = {'name': user.name, 'admin': user.admin}
        return HttpResponse(json.dumps(''))


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


def api_blogs(request, page='1'):
    if request.method == 'GET':
        page_index = get_page_index(page)
        num = Blog.objects.count()
        p = Page(num, page_index).page_dict()
        if num == 0:
            return HttpResponse(json.dumps(dict(page=p, blogs=())))
        blogs = list(Blog.objects.values().order_by('-created_at')[p.get('offset'): p.get('limit')])
        for blog in blogs:
            blog['user_name'] = User.objects.get(id=blog['user_id_id']).name
        return HttpResponse(json.dumps(dict(page=p, blogs=blogs)))
    elif request.method == 'POST':
        uid = request.session.get('user_session', None)
        if User.objects.get(id=uid).admin == 1:
            body = eval(request.body)
            name = body.get('name', None)
            summary = body.get('summary', None)
            content = body.get('content', None)
            if not name or not name.strip():
                return HttpResponse('标题不可为空')
            if not summary or not summary.strip():
                return HttpResponse('摘要不可为空')
            if not content or not content.strip():
                return HttpResponse('内容不可为空')
            dic = {
                'user_id': User.objects.get(id=uid),
                'name': name,
                'summary': summary,
                'content': content,
            }
            Blog.objects.create(**dic)
            return HttpResponse(json.dumps(''))
        else:
            return HttpResponse(json.dumps(''))



def api_time(request, page='1'):
    if request.method == 'GET':
        page_index = get_page_index(page)
        num = TimeFragment.objects.count()
        p = Page(num, page_index).page_dict()
        if num == 0:
            return HttpResponse(json.dumps(dict(page=p, time_fragment=())))
        time_fragment = list(TimeFragment.objects.values().order_by('-created_at')[p.get('offset'): p.get('limit')])
        for fragment in time_fragment:
            fragment['user_name'] = User.objects.get(id=fragment['user_id_id']).name
        return HttpResponse(json.dumps(dict(page=p, time_fragment=time_fragment)))
    elif request.method == 'POST':
        uid = request.session.get('user_session', None)
        if User.objects.get(id=uid).admin:
            body = json.loads(request.body)
            introduction = body.get('introduction', None)
            weather = body.get('weather', None)
            album_url = body.get('album_url', None)
            if not introduction or not introduction.strip():
                return HttpResponse('简介不可为空')
            if not weather or not weather.strip():
                return HttpResponse('天气不可为空')
            if not album_url or not album_url.strip():
                return HttpResponse('时光不可为空')
            dic = {
                'user_id': User.objects.get(id=uid),
                'introduction': introduction,
                'weather': weather,
                'album_url': album_url,
            }
            TimeFragment.objects.create(**dic)
            return HttpResponse(json.dumps(''))
        else:
            return HttpResponse(json.dumps(''))


def api_envelope(request, page='1'):
    if request.method == 'GET':
        page_index = get_page_index(page)
        num = Envelope.objects.count()
        p = Page(num, page_index).page_dict()
        if num == 0:
            return HttpResponse(json.dumps(dict(page=p, envelope=())))
        envelopes = list(Envelope.objects.values().order_by('-created_at')[p.get('offset'): p.get('limit')])
        for envelope in envelopes:
            envelope['user_name'] = User.objects.get(id=envelope['user_id_id']).name
        return HttpResponse(json.dumps(dict(page=p, envelope=envelopes)))
    elif request.method == 'POST':
        uid = request.session.get('user_session', None)
        if User.objects.get(id=uid).admin:
            remarks = request.POST.get('remarks', None)
            postcards = request.POST.get('postcards', None)
            if not remarks or not remarks.strip():
                return HttpResponse('寄语不可为空')
            if not postcards or not postcards.strip():
                return HttpResponse('明信片不可为空')
            dic = {
                'user_id': User.objects.get(id=uid),
                'remarks': remarks,
                'postcards': postcards,
            }
            Envelope.objects.create(**dic)
            return HttpResponse(json.dumps(''))
        else:
            return HttpResponse(json.dumps(''))


def api_get_blog(request, id):
    if request.method == 'GET':
        blog = Blog.objects.filter(id=id).values('name', 'summary', 'content')[0]
        return HttpResponse(json.dumps(blog))
    elif request.method == 'POST':
        uid = request.session.get('user_session', None)
        if User.objects.get(id=uid).admin:
            body = eval(request.body)
            name = body.get('name', None)
            summary = body.get('summary', None)
            content = body.get('content', None)
            if not name or not name.strip():
                return HttpResponse('标题不可为空')
            if not summary or not summary.strip():
                return HttpResponse('摘要不可为空')
            if not content or not content.strip():
                return HttpResponse('内容不可为空')
            Blog.objects.filter(id=id).update(user_id=User.objects.get(id=uid), name=name, summary=summary, content=content)
            return HttpResponse(json.dumps(''))
        else:
            return HttpResponse(json.dumps(''))


def api_get_time(request, id):
    if request.method == 'GET':
        times = TimeFragment.objects.filter(id=id).values('introduction', 'weather', 'album_url')[0]
        return HttpResponse(json.dumps(times))
    elif request.method == 'POST':
        uid = request.session.get('user_session', None)
        if User.objects.get(id=uid).admin:
            body = json.loads(request.body)
            introduction = body.get('introduction', None)
            weather = body.get('weather', None)
            album_url = body.get('album_url', None)
            if not introduction or not introduction.strip():
                return HttpResponse('简介不可为空')
            if not weather or not weather.strip():
                return HttpResponse('天气不可为空')
            if not album_url or not album_url.strip():
                return HttpResponse('时光不可为空')
            TimeFragment.objects.filter(id=id).update(user_id=User.objects.get(id=uid), introduction=introduction,
                                                                      weather=weather, album_url=album_url)
            return HttpResponse(json.dumps(''))
        else:
            return HttpResponse(json.dumps(''))


def api_get_envelope(request, id):
    if request.method == 'GET':
        envelope = Envelope.objects.filter(id=id)
        return HttpResponse(envelope)
    elif request.method == 'POST':
        uid = request.session.get('user_session', None)
        if User.objects.get(id=uid).admin:
            remarks = request.POST.get('remarks', None)
            postcards = request.POST.get('postcards', None)
            if not remarks or not remarks.strip():
                return HttpResponse('寄语不可为空')
            if not postcards or not postcards.strip():
                return HttpResponse('明信片不可为空')
            Envelope.objects.filter(id=id).update(user_id=User.objects.get(id=uid), remarks=remarks, postcards=postcards)
            return HttpResponse(json.dumps(''))
        else:
            return HttpResponse(json.dumps(''))


def api_delete_blog(request, id):
    uid = request.session.get('user_session', None)
    if User.objects.get(id=uid).admin:
        Blog.objects.filter(id=id).delete()
        return HttpResponse(json.dumps(''))
    else:
        return HttpResponse(json.dumps(''))


def api_delete_time(request, id):
    uid = request.session.get('user_session', None)
    if User.objects.get(id=uid).admin:
        TimeFragment.objects.filter(id=id).delete()
        return HttpResponse(json.dumps(''))
    else:
        return HttpResponse(json.dumps(''))


def api_delete_envelope(request, id):
    uid = request.session.get('user_session', None)
    if User.objects.get(id=uid).admin:
        Envelope.objects.filter(id=id).delete()
        return HttpResponse(json.dumps(''))
    else:
        return HttpResponse(json.dumps(''))


def upload_ajax(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        file_name = request.POST.get('file_name')
        import os
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'statics', 'pic', file_name), 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return HttpResponse(json.dumps(''))