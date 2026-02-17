from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ImageForm
from .models import Image

def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if form.is_valid():
                instance = form.save()
                return JsonResponse({
                    'success': True,
                    'image_url': instance.photo.url,
                    'date': instance.date.strftime('%Y-%m-%d %H:%M:%S')
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid form data'
                })
        else:
            # Normal form submission (fallback)
            if form.is_valid():
                form.save()
                return redirect('home')
    else:
        form = ImageForm()
    
    img = Image.objects.all().order_by('-date')
    return render(request, 'myapp/home.html', {'form': form, 'img': img})