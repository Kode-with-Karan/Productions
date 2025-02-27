from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        message = request.POST["message"]
        send_mail(f"Support Request from {name}", message, email, [settings.SUPPORT_EMAIL])
    
    return render(request, "support/contact.html")
