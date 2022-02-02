import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.db.models import F, Value
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Concat



from .models import *


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def post(request):

    if request.method == "POST":
        print("Post successfully")
        data = json.loads(request.body)
        print("data")
        print(data)
        content = data.get("content", "")
        print("content")
        print(content)

        post = Post(
            content = content,
            author = request.user,
            )
        post.save()
        return JsonResponse({"message": "Email sent successfully."}, status=201)

    if request.method == "GET":
        posts = Post.objects.all().order_by("-timestamp")
        print("posts")
        print(posts)
        # return JsonResponse([post.serialize() for post in posts], safe=False)
        return JsonResponse([post.serialize() for post in posts], safe=False)



    if request.method == "GET":
        print("GET successfully")
        HttpResponse("GET successfully")



@csrf_exempt
@login_required
def like(request):

    # username = request.POST["username"]
    logged_in_user = request.user
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id", "")
        print("post_id", post_id)
        post_object = Post.objects.get(pk=post_id)
        print("post_object", post_object)

        like_object = Like(
            post = post_object,
            like_user = logged_in_user
        )
        like_object.save()
        return JsonResponse({"message": "Liked successfully."}, status=201)



# Check what posts loggeed in users like
@csrf_exempt
@login_required
def check_like(request):

    # username = request.POST["username"]
    logged_in_user = request.user
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id", "")
        print("post_id", post_id)
        post_object = Post.objects.get(pk=post_id)
        print("post_object", post_object)

        is_liked = Like.objects.filter( post=post_object, like_user=logged_in_user).exists()

        return JsonResponse(is_liked, safe=False)

    # Shouldnn't be using GET but keep her to test
    if request.method == "GET":
        is_liked = Like.objects.filter(like_user=logged_in_user).exists()
        return JsonResponse(is_liked, safe=False)