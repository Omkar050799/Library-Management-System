from django.http import HttpResponse
from django.conf import settings
import traceback
from rest_framework.renderers import JSONRenderer
from utility.response import ApiResponse


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def message_format(self, message):
        return message

    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if exception:
                # Format your message here
                try:
                    message = [str(exception.args[0])]
                except:
                    message = ''

            response = ApiResponse.response_internal_server_error(self, message=message, code=500)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response