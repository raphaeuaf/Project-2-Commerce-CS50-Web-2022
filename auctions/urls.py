from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("<int:category_id>", views.viewcategories, name="viewcategories"),
    path("viewitem/<int:item_id>", views.viewitem, name="viewitem"),
    path("bid", views.bid, name="bid"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("del_item/<int:item_id>", views.del_item, name="del_item"),
    path("watchlist", views.watchlist, name="watchlist")
]
