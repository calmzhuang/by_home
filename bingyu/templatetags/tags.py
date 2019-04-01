#__author:  Administrator
#date:  2017/1/5

from django import template
from django.utils.safestring import mark_safe
from datetime import datetime
import time
import re
register = template.Library()

@register.simple_tag
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


@register.filter
def type_filter(album_url):
    if re.findall('[mp4|avi]$', album_url):
        return True
    else:
        return False
