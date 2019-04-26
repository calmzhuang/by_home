from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from bingyu.models import User
import re


class Authentication(MiddlewareMixin):
    def process_request(self, request):
        request_path = request.path
        re_result = re.search('manage', request_path)
        uid = request.session.get('user_session', None)
        if re_result is not None and (uid is None or User.objects.get(id=uid).admin != 1):
            return redirect('/')
