
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path("following", views.following, name="following"),

    # API routes
    path("post", views.post, name="post"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("like", views.like, name="like"),
    path("unlike", views.unlike, name="unlike"),
    path("check_like", views.check_like, name="check_like"),
    path("like_num", views.like_num, name="like_num"),
    path("post/<int:post_id>", views.edit, name="edit"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:post_user_name>", views.follow, name="follow")
]
