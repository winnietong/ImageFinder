from django.core import serializers
from django.shortcuts import render, redirect
from forms import *
from django.core.mail import EmailMultiAlternatives
from project2 import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Count
from django.template import *

# Create your views here.

def home(request):
    images = Image.objects.all().annotate(num_count = Count('favorites')).order_by('num_count')[:3]
    return render(request, "index.html", {'current_path': request.get_full_path(), 'images': images})


def search(request):
    # query = request.GET['q']
    # print query
    return render(request, "search.html")


def license(request):
    return render(request, "license.html")


def featured(request):
    images = Image.objects.all().annotate(num_count = Count('favorites')).order_by('num_count')[:10]
    return render(request, "featured.html", {'images': images, 'current_path': request.get_full_path()})


def upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST)
        return render(request, "upload.html", {"form": form})
    else:
        form = ImageForm(initial={
            'ApiURL': "",
            'ApiID': "",
            'Author': request.user,
            'PageURL': "",
            'ImageURL': "",
            'ThumbnailURL': "",
            'Favorites': request.user,
            'Referrer': "Open Imager"
        })
    return render(request, "upload.html", {"form": form})

@csrf_exempt
def show_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        my_favorites = Image.objects.filter(favorites__username=request.user)
        for favorite in my_favorites:
            if favorite.pageURL == data['pageURL']:
                data['favorited'] = 'yes'
                print "Exists as a Favorite!"
        return render(request, 'includes/show_image.html', data)


@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print data
        image = Image.objects.filter(pageURL = data['pageURL'])
        # If image doesn't exist
        if len(image)<1:
            print "Image is being saved to database"
            image = Image.objects.create(
                title = data['title'],
                author = data['user'],
                pageURL = data['pageURL'],
                imageURL = data['webformatURL'],
                thumbnailURL = data['previewURL'],
                api_id = data['id'],
                apiURL = data['apiURL'],
                referrer = data['referrer']
            )
            tags = data['tags'].split(', ')
            for tag in tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                tag.image.add(image)


        # Add image to user's favorites
        # image = Image.objects.get(pageURL=data['pageURL'])

        user = User.objects.get(username = request.user)
        user.image.add(image)
        return render(request, 'includes/show_image.html')


# To Unfavorite an image:

@csrf_exempt
def unfavorite_image(request):
    if request.method == 'POST':
        print "Unfavorite Image Start"
        data = json.loads(request.body)
        image = Image.objects.get(pageURL = data['pageURL'])
        user = User.objects.get(username=request.user)
        user.image.remove(image)
        return render(request, 'includes/show_image.html')


@login_required
def profile(request):
    images = Image.objects.filter(favorites__username=request.user)
    if request.POST.get('profile'):
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/profile/")
    else:
        form = UserForm(instance=request.user)
    return render(request, "profile.html", {'form': form, 'images': images, 'current_path': request.get_full_path()})


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            text_content = 'Thank you for signing up for our website, {}'.format(user.username)
            html_content = '<h2>Hey {}, thanks for signing up!</h2> <div>I hope you enjoy using our site</div>'.format(user.username)
            msg = EmailMultiAlternatives("Welcome!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect("/")
    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })