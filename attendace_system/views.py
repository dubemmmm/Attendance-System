from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.http import HttpResponse
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

def send_contact_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        from_email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Compose the mail
        subject = f'Support Request from {name}'
        message_body = f'Name: {name}\nEmail: {from_email}\n\nMessage:\n{message}'
        recipient_list = ['onwuchulubachidubem@gmail.com', 'lifeofchris14@gmail.com']
        try:
            send_mail(
                subject=subject,
                message=message_body,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            context = {'success_message': 'Your message has been sent successfully.'}
        except Exception as e:
            print(e)
            context = {'error_message': 'Failed to send email. Please try again later.'}
            
    return render(request, 'support.html', context=context)

    
        