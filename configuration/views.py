from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        context = {
            "user": request.user
        }
        return render(request, 'index.html', context)
    return redirect('login')
