from django.shortcuts import render

def index(request):
    return render(request, 'reserve/index.html')

def confirm(request):
    return render(request, 'reserve/confirm.html')

def complete(request):
    return render(request, 'reserve/complete.html')

# Create your views here.
