from django.shortcuts import render

# Create your views here.
def index(request):
    number = 6
    return render(request, 'index.html',{
        'number':number,
        'greeting':'Hi Mackenzie!',
    })

