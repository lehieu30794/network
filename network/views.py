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
from django.core import serializers
from django.core.paginator import Paginator




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
        return JsonResponse({"message": "Post successfully."}, status=201)


@csrf_exempt
@login_required
def all_posts(request):
    if request.method == "GET":
        posts = Post.objects.all().order_by("-timestamp")
        print("posts")
        print(posts)
        # return JsonResponse([post.serialize() for post in posts], safe=False)
        # Testing paginated post
        return paginate_posts(request, posts)

@csrf_exempt
@login_required
def following_posts(request):
    if request.method == "GET":
        posts = Post.objects.all().order_by("-timestamp")
        print("posts")
        print(posts)
        # return JsonResponse([post.serialize() for post in posts], safe=False)
        return JsonResponse([post.serialize() for post in posts], safe=False)



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

        like_num = Like.objects.filter(post=post_object).count()
        print("like_num")
        print(like_num)

        # post_likes = Like.objects.filter(post)
        # print("post_likes", post_likes)
        return JsonResponse({"message": "Liked successfully.", "like_num":like_num}, status=201)




@csrf_exempt
@login_required
def unlike(request):

    # username = request.POST["username"]
    logged_in_user = request.user
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id", "")
        print("post_id", post_id)
        post_object = Post.objects.get(pk=post_id)
        print("post_object", post_object)

        # Delete the like
        Like.objects.filter(post=post_object, like_user=logged_in_user).delete()

        like_num = Like.objects.filter(post=post_object).count()
        print("like_num")
        print(like_num)
        # post_likes = Like.objects.filter(post)
        # print("post_likes", post_likes)
        return JsonResponse({"message": "Unliked successfully.", "like_num":like_num}, status=201)



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

    # Shouldn't be using GET but keep her to test
    if request.method == "GET":
        is_liked = Like.objects.filter(like_user=logged_in_user).exists()
        return JsonResponse(is_liked, safe=False)


@csrf_exempt
@login_required
def like_num(request):
    # Get number of initial likes
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id", "")
        print("post_id", post_id)
        post_object = Post.objects.get(pk=post_id)
        print("post_object", post_object)
        like_num = Like.objects.filter(post=post_object).count()
        print("like_num")
        print(like_num)
        # like_num = Like.objects.filter(post=post_object).exists()
        return JsonResponse(like_num, safe=False)


@csrf_exempt
@login_required
def edit(request, post_id):
    post_object = Post.objects.get(pk=post_id)
    if request.method == "GET":
        return JsonResponse(post_object.serialize(), safe=False)
    if request.method == "POST":
        print("Post successfully")
        data = json.loads(request.body)
        print("data")
        print(data)
        content = data.get("content", "")
        print("content")
        print(content)
        post_object.content = content
        post_object.save() 
        return JsonResponse({"message": "Edit post successfully."}, status=201)


@csrf_exempt
@login_required
def profile(request, username):

    # Type: object
    post_user_object = User.objects.get(username=username)
    # Type: string | Get username string, not object to return it as apart of a dictionary
    post_user = post_user_object.username
    # Get the id of post user to determine whether to display the follow button
    post_user_id = post_user_object.id
    print("post_user_id")
    print(post_user_id)
    # Type: object
    logged_in_user = request.user
    
    # Type: int
    follower_num = Follow.objects.filter(following=post_user_object).count()
    following_num = Follow.objects.filter(follower=post_user_object).count()
    post_num = Post.objects.filter(author=post_user_object).count()
    # Users that the logged in user are currently following
    followed_users = Follow.objects.filter(follower=logged_in_user)
    # Using related name defined in model
    followed_users2 = logged_in_user.follower.all().values('following')

    print(f"follower_num: {follower_num}")
    print(f"following_num: {following_num}")
    print(f"post_num: {post_num}")
    print(f"followed users: {followed_users2}")

    already_followed = False
    for followed_user in followed_users2:
        if followed_user['following'] == post_user_id:
            already_followed = True


    # CAN BE DELETED
    # # print result: <function post at 0x7f7d6b4825e0>
    # posts = Post.objects.filter(author=post_user_object).order_by("-timestamp")

    # response = {}
    # # result: Looks like {'posts': '[ list of posts ]'}
    # response['posts'] = serializers.serialize("json", posts)
    # print('response')
    # print(response)

    # response['post_user'] = post_user.capitalize()
    # response['follower_num'] = follower_num
    # response['following_num'] = following_num
    # response['post_num'] = post_num

    # print('response')
    # print(response)


    posts = Post.objects.filter(author=post_user_object).order_by("-timestamp")
    # Type: list
    response2 = [post.serialize() for post in posts]
    
    print('response2')
    print(response2)

    # Add other important data at the end of the returned dictionary
    profile_data = {}
    profile_data['post_user'] = post_user
    profile_data['follower_num'] = follower_num
    profile_data['following_num'] = following_num
    profile_data['post_num'] = post_num
    profile_data['already_followed'] = already_followed
    print("profile_data")
    print(profile_data)

    # Convert a dict to a list to pop it out as a whole in JS
    profile_data_list = []
    profile_data_list.append(profile_data.copy())
    print("profile_data_list")
    print(profile_data_list)

    response2.append(profile_data_list)
    print('response2')
    print(response2)



    # return JsonResponse([post.serialize() for post in posts], safe=False)


    return JsonResponse(response2, safe=False)


@csrf_exempt
@login_required
def follow(request, post_user_name):
    print("Hit FOLLOW API")

    logged_in_user = request.user
    post_user = User.objects.get(username=post_user_name)
    print("logged_in_user")
    print(logged_in_user)
    print("post_user")
    print(post_user)

    # Follow
    if request.method == "POST":
        follow_object = Follow(
            follower=logged_in_user,
            following=post_user
        )
        follow_object.save()
        return JsonResponse({"message":"Follow successfully"}, status=201)

    # Unfollow
    if request.method == "DELETE":
        Follow.objects.filter(follower=logged_in_user, following=post_user).delete()
        
        return JsonResponse({"message": "Unfollow successfully."}, status=201)



# def following(request):
#     if request.method == "GET":
#         user_followed_by_loggedinuser = Follow.objects.filter(follower = request.user)\
#                                           .values_list('following', flat=True)\
#                                           .distinct()
        
#         posts = Post.objects.filter(author__in=user_followed_by_loggedinuser)

#         print("user_followed_by_loggedinuser")
#         print(user_followed_by_loggedinuser)
#         print("posts")
#         print(posts)


#         # posts = Post.objects.all().order_by("-timestamp")
#         # posts = Post.objects.filter()
#         # print("posts")
#         # print(posts)
#         # # return JsonResponse([post.serialize() for post in posts], safe=False)
#         return JsonResponse([post.serialize() for post in posts], safe=False)
#     # return render(request, "network/following.html")


def following_posts(request):
    if request.method == "GET":
        user_followed_by_loggedinuser = Follow.objects.filter(follower = request.user)\
                                          .values_list('following', flat=True)\
                                          .distinct()
        
        posts = Post.objects.filter(author__in=user_followed_by_loggedinuser).order_by("-timestamp")

        print("user_followed_by_loggedinuser")
        print(user_followed_by_loggedinuser)
        print("posts")
        print(posts)

        # paginator = Paginator(posts, 10)
        # try:
        #     page_number = request.GET.get("page", "1")
        # except:
        #     page_number = 1

        # try:
        #     posts_in_one_page = paginator.page(page_number)
        # except (EmptyPage, InvalidPage):
        #     posts_in_one_page = paginator.page(paginator.num_pages)

        # Testing pagainted posts
        return paginate_posts(request, posts)

        # return JsonResponse([post.serialize() for post in posts_in_one_page], safe=False)
    # return render(request, "network/following.html")

@csrf_exempt
@login_required
def paginate_posts(request, posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", "1")
    posts_in_one_page = paginator.page(page_number)
    return JsonResponse({
        "posts": [post.serialize() for post in posts_in_one_page],
        "num_pages": paginator.num_pages}, safe=False)