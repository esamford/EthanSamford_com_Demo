from django.shortcuts import render


# https://www.geeksforgeeks.org/built-in-error-views-in-django/

def error_404(request, *args, **kwargs):
    context = {
        'error_number': 404,
        'error_message': "We could not match that URL to a page on our server. "
                         "Whatever you are looking for may have been moved."
    }

    return render(request, 'error_page.html', context=context)


def error_500(request, *args, **kwargs):
    context = {
        'error_number': 500,
        'error_message': "An exception occurred within the server while processing "
                         "your request."
    }

    return render(request, 'error_page.html', context=context)


