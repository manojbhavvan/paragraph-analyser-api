# paragraphs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.UserLoginAPIView.as_view(), name="login"),
    path(
        "paragraphs/",
        views.ParagraphCreateAPIView.as_view(),
        name="paragraph-create",
    ),
    path("search/", views.SearchParagraphsAPIView.as_view(), name="search-paragraphs"),
]
