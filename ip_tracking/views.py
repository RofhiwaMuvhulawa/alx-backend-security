from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

# Example of a rate-limited function-based view
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def sensitive_view(request):
    return HttpResponse("This is a rate-limited view")

# Example of a rate-limited class-based view (login)
@method_decorator(ratelimit(key='ip', rate='10/m', method='GET', block=True), name='get')
@method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True), name='post')
@method_decorator(ratelimit(key='post:username', rate='5/m', method='POST', block=True), name='post')
class RateLimitedLoginView(LoginView):
    """Login view with rate limiting"""
    template_name = 'login.html'