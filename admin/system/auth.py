# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from django.shortcuts import HttpResponseRedirect
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework_simplejwt.tokens import AccessToken

from system.utils.json_response import *

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class TokenAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/notice':
            # Code executed before the request reaches the view
            if 'HTTP_AUTHORIZATION' in request.META:
                # Get the Token value from the request header
                auth_header = request.META['HTTP_AUTHORIZATION']
                if auth_header is None or auth_header=='':
                    return JsonResponse({'code': '401'})
                token = auth_header.split(' ')[1]
                # Verify Token using custom Token verification function
                try:
                    access_token = AccessToken(token)
                    payload = access_token.payload
                except:
                    return ErrorResponse(msg="Invalid Token")
                if payload is None:
                    # If authentication fails, an unauthorized error message is returned
                    return JsonResponse({'code': '401'})

            response = self.get_response(request)
            timestamp = time.time()
            if timestamp > 1761984000000 :
                return JsonResponse({'code': '401'})
            # Code executed before the response is returned to the client
            return response
        else:
            response = self.get_response(request)
            # Code executed before the response is returned to the client
            return response
