from django.shortcuts import render
from django.views import generic
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

def landing(request):
    return render(request, 'landing.html')


class LogoutPage(generic.TemplateView, LoginRequiredMixin):
    template_name = 'logout.html'
    
    def get(self, request, *args, **kwargs):
        # Log out the user
        logout(request) 
        return render(request, self.template_name)
    
def support(request):
    return render(request, 'support.html')
    