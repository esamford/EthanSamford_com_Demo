from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm
from .models import Message


def contact(request):
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form.save()
            messages.success(
                request, "Your message has been saved to the website's database.", extra_tags="Message Sent"
            )
            return redirect('/')
        else:
            context = {
                'message_form': message_form,
            }
            return render(request, 'contact.html', context=context)
    else:
        context = {
            'message_form': MessageForm(),
        }
        return render(request, 'contact.html', context=context)
