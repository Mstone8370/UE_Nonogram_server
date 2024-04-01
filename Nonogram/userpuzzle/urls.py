from django.urls import path
from . import views

app_name = "userpuzzle"
urlpatterns = [
    path("", views.upload_request, name="userpuzzle"),
    path("list/<int:num>/", views.get_list, name="get_list"),
    path("list/<int:num>/<int:last_id>/", views.get_list, name="get_list"),
]
