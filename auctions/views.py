from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Auction, Bid, Comment


def index(request):
    # unwrap all categories alphabetically in order to put them on top pages menu
    categories = Category.objects.order_by('category')
    # Count how many items there are in the watchlist
    if request.user.id:
        n_wl = User.objects.get(id=request.user.id).watchlist.count()
    else:
        n_wl = 0

    # unwrap all objects from Auctions
    auctions = Auction.objects.all()
    if request.user.username:
        user = User.objects.get(username=request.user.username)
    else:
        user = ""

    return render(request, "auctions/index.html", {
        "active_index": "active",
        "categories": categories,
        "title_page": "Active Listings",
        "auctions": auctions,
        "user": user,
        "n_wl": n_wl
    })


def login_view(request):
    # Jão jao123JAO!@#
    # Gertrudinha chadeboldo
    # Creosnice cre123CRE!@#
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    # unwrap all categories alphabetically in order to put them on top pages menu
    categories = Category.objects.order_by('category')
    # Count how many items there are in the watchlist
    if request.user.id:
        n_wl = User.objects.get(id=request.user.id).watchlist.count()
    else:
        n_wl = 0
    
    if request.method == "POST":
        # Get all field in order to feed Auction object
        new_item = {} 
        new_item["title"] = request.POST["title"]
        new_item["desc"] = request.POST["description"]
        new_item["bid"] = request.POST["bid"]
        new_item["img"] = request.POST["img"]
        new_item["cat"] = request.POST.getlist("cat")
        new_item["owner"] = request.user.username

        # Check if any field is blank
        if not request.POST["title"]:
            new_item["msg_title"] = "Please, type a title"
            return render(request, "auctions/createN.html", {
            "active_create": "active",
            "categories": categories,
            "new_item": new_item,
            "n_wl": n_wl
        })
        elif not request.POST["description"]:
            new_item["msg_desc"] = "Please, add some description"
            return render(request, "auctions/createN.html", {
            "active_create": "active",
            "categories": categories,
            "new_item": new_item,
            "n_wl": n_wl
        })
        elif not request.POST["bid"]:
            new_item["msg_bid"] = "Please, put a value for your product"
            return render(request, "auctions/createN.html", {
            "active_create": "active",
            "categories": categories,
            "new_item": new_item,
            "n_wl": n_wl
        })
        elif not request.POST["img"]:
            new_item["msg_img"] = "Please, add a image address"
            return render(request, "auctions/createN.html", {
            "active_create": "active",
            "categories": categories,
            "new_item": new_item,
            "n_wl": n_wl
        })
        elif not request.POST.getlist("cat"):
            new_item["msg_cat"] = "Please, pick at least one category"
            return render(request, "auctions/createN.html", {
            "active_create": "active",
            "categories": categories,
            "new_item": new_item,
            "n_wl": n_wl
        })

        # If all fields are fulfilled, then store the data
        else:
            # Create a new Auction object and save it
            new_auction = Auction(
                title = request.POST["title"],
                description = request.POST["description"],
                start_bid = request.POST["bid"],
                image_url = request.POST["img"],
                owner = User.objects.get(pk=int(request.POST["owner"]))
            )
            new_auction.save()

            # As category is ManyToMany fiel and it is a list, we iterate each element from this list
            list_cat = request.POST.getlist("cat")
            for i in list_cat:
                new_auction.category.add(i)
                this_cat = Category.objects.get(id=i)
                this_cat.quantity += 1
                this_cat.save()        
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createN.html", {
            "active_create": "active",
            "categories": categories,
            "n_wl": n_wl
        })
        


@login_required
def categories(request):
    # unwrap all categories alphabetically in order to put them on top pages menu
    categories = Category.objects.order_by('category')
    # Count how many items there are in the watchlist
    if request.user.id:
        n_wl = User.objects.get(id=request.user.id).watchlist.count()
    else:
        n_wl = 0
    return render(request, "auctions/categories.html", {
        "categories": categories,
        "n_wl": n_wl
    })


def viewcategories(request, category_id):
    # unwrap all categories alphabetically in order to put them on top pages menu
    categories = Category.objects.order_by('category')
    # Count how many items there are in the watchlist
    if request.user.id:
        n_wl = User.objects.get(id=request.user.id).watchlist.count()
    else:
        n_wl = 0

    # unwrap all objects from Auctions
    auctions = Auction.objects.filter(category=category_id)    
    # Get the name of the required category
    category = Category.objects.filter(id=category_id)

    if request.user.username:
        user = User.objects.get(username=request.user.username)
    else:
        user = ""

    # Know if there are items in a requeried category
    if not auctions:
        title_page = f"There's no items for {category[0]} category yet, {user}"
        no_category = "nothing"
    else:
        title_page = f"Category: {category[0]}"
        no_category = ""

    return render(request, "auctions/index.html", {
        "categories": categories,
        "auctions": auctions,
        "title_page": title_page,
        "no_category": no_category,
        "n_wl": n_wl
    })


def viewitem(request, item_id):
    # unwrap all categories alphabetically in order to put them on top pages menu
    categories = Category.objects.order_by('category')
    # Count how many items there are in the watchlist
    if request.user.id:
        n_wl = User.objects.get(id=request.user.id).watchlist.count()
    else:
        n_wl = 0
    
    # As there is only one item, a simple dict is enough here
    dict = {}

    # To get the current user and id
    user = request.user.username
    user_id = request.user.id

    # unwrap only the object which was required from Auctions with requested item id
    auction = Auction.objects.get(id=item_id)

    # To get the user's object
    if user:
        user_object = User.objects.get(username=user)
        dict["user"] = User.objects.get(id=user_id)

        # To get the current Auction's owner without model parameters 
        u = User.objects.get(username=auction.owner)
        owner = u.username

        # To know if an item is in watchlist
        if auction in user_object.watchlist.all():
            dict["message_wl"] = "This item is on your watchlist"
            dict["btnid"] = "bttngreen"
        else:
            dict["message_wl"] = "Add this item to your watchlist"
            dict["btnid"] = "bttngray"
    else:
        owner = False

    # Know if there is any bid
    bids = Bid.objects.filter(auction=item_id)
    if bids:
        u_object = User.objects.get(username=bids[len(bids) - 1].owner)
        bid_owner = u_object.username
        if auction.is_active == True:
            dict["title_page"] = "View Item"
            dict["color_tp"] = "black"
            dict["color"] = "green"
            dict["msg_bid"] = "Current Bid:"
            dict["onoff_field"] = "nothing"
            dict["onoff_btn"] = "nothing" 
            if len(bids) == 1:
                if bid_owner != user:
                    dict["message_bid"] = "1 Bid has been placed"
                else:
                    dict["message_bid"] = "1 Bid has been placed - You hold the current bid"
            else:
                if bid_owner != user:
                    dict["message_bid"] = f"{len(bids)} Bids have been placed"
                else:
                    dict["message_bid"] = f"{len(bids)} Bids have been placed - You hold the current bid"
                
        else:
            dict["color"] = "green"
            dict["title_page"] = "Auction Closed"
            dict["titleimg"] = "Sold"
            dict["color_tp"] = "red"
            if len(bids) == 1:
                if user == owner:
                    dict["message_bid"] = "You closed this auction - 1 Bid was placed"
                else:
                    dict["message_bid"] = f"{ owner } closed this auction - 1 Bid was placed"
            else:
                if user == owner:
                    dict["message_bid"] = f"You closed this auction - {len(bids)} Bids were placed"
                else:
                    dict["message_bid"] = f"{ owner } closed this auction - {len(bids)} Bids were placed"
            dict["msg_bid"] = "Winning Bid:"
            dict["sold"] = "Sold"
            dict["onoff_btn"] = "disabled"
            dict["onoff_field"] = "disabled"
            if user == owner:
                dict["msg_win"] = f"{ bid_owner} has won the auction"
            elif user == bid_owner:
                dict["msg_win"] = "Congratulations! you have won the auction"
            else:
                dict["msg_win"] = "What a shame! You didn't win the auction."
    else:
        if auction.is_active == True:
            dict["title_page"] = "View Item"
            dict["color_tp"] = "black"
            dict["message_bid"] = "No Bids have been placed yet"
            dict["msg_bid"] = "Starting Bid:"
            dict["sold"] = ""
            dict["onoff_btn"] = "nothing"
            dict["onoff_field"] = "nothing"
            dict["color"] = ""
        else:
            dict["title_page"] = "Auction Closed"
            dict["titleimg"] = "Unavailable"
            dict["color_tp"] = "red"
            dict["message_bid"] = "No Bid was placed"
            dict["msg_bid"] = "Starting Bid"
            dict["sold"] = "Closed without being sold!"
            dict["onoff_btn"] = "disabled"
            dict["onoff_field"] = "disabled"
            dict["color"] = "red"

    # Know if there is any comment and get in reverse oreder to show the newer first
    comments = Comment.objects.filter(auction=item_id)
    rv_comments = []
    if comments:
        for i in range(len(comments), 0, -1):
            rv_comments.append(comments[i - 1])
        dict["theres_comment"] = "yes"
        if len(comments) == 1:
            dict["msg_comment"] = "1 Comment:"
        else:
            dict["msg_comment"] = f"{len(comments)} Comments:"
    else:
        dict["theres_comment"] = ""
        dict["msg_comment"] = "No Comments yet..."
    
    # Jinja doesn't work properly, then I will try some loops here

    # Different behaviors if the current user is the owner or not
    if user == owner:
        dict["owner"] = f"You, {auction.owner}"
        dict["btn_bid"] = "Close Auction"
        dict["btn_bid_id"] = "bttnred"
        dict["onoff_field"] = "disabled"        
        dict["same"] = "same"
        dict["required"] = ""
    else:
        dict["owner"] = auction.owner
        dict["btn_bid"] = "Place Bid"
        dict["btn_bid_id"] = "bttngreen"
        dict["same"] = ""
        dict["required"] = "required"
        
    dict["comments"] = rv_comments

    if request.method == "POST":
        if not user:
            dict["not_user"] = "You must be logged in if you want to have a watchlist"
            return render(request, "auctions/viewitem.html",{
            "categories": categories,
            "dict": dict,
            "auction": auction,
            "n_wl": n_wl
        })
        else:
            # For watchlist button work properly
            if auction in user_object.watchlist.all():
                user_object.watchlist.remove(auction)
                return HttpResponseRedirect(reverse("viewitem", args=[item_id]))
            else:           
                user_object.watchlist.add(auction)
                return HttpResponseRedirect(reverse("viewitem", args=[item_id]))        

    else:
        return render(request, "auctions/viewitem.html",{
            "categories": categories,
            "dict": dict,
            "auction": auction,
            "n_wl": n_wl
        })

@login_required
def bid(request, methods=["POST"]):
    
    # To get some important data
    user = request.user.username
    user_id = request.user.id    
    item_id = request.POST["item_id"]
    auction = Auction.objects.get(id=item_id)
    u = User.objects.get(username=auction.owner)
    owner = u.username

    # if user and the ower are the same. The button is "close auction"
    if user == owner:
        auction.is_active = False
        auction.save()
        return HttpResponseRedirect(reverse("viewitem", args=[item_id]))

    # if user is not the ower, bid can be placed. The button is "place bid"
    else:
        amount = request.POST["bid"]
        new_bid = Bid(amount=amount, auction = Auction.objects.get(pk=item_id), owner = User.objects.get(pk=user_id))
        new_bid.save()
        auction = Auction.objects.get(id=item_id)
        auction.thereis_bid = True
        auction.current_bid = int(amount) + 1
        auction.save()
        return HttpResponseRedirect(reverse("viewitem", args=[item_id]))


@login_required
def add_comment(request, methods=["POST"]):
    # To get some important data
    user_id = request.user.id
    item_id = request.POST["item_id"]
    comment = request.POST["comment"]
    new_comment = Comment(auction=Auction.objects.get(pk=item_id), content=comment, author=User.objects.get(pk=user_id))
    new_comment.save()
    return HttpResponseRedirect(reverse("viewitem", args=[item_id]))


@login_required
def del_item(request, item_id):
    # unwrap all categories alphabetically in order to put them on top pages menu
    categories = Category.objects.order_by('category')
    # Count how many items there are in the watchlist
    if request.user.id:
        n_wl = User.objects.get(id=request.user.id).watchlist.count()
    else:
        n_wl = 0

    # As there is only one item, a simple dict is enough here
    dict = {}

    # To get the current user and id
    user = request.user.username
    user_id = request.user.id

    # unwrap only the object which was required from Auctions with requested item id
    auction = Auction.objects.get(id=item_id)

    # To get the current Auction's owner without model parameters 
    u = User.objects.get(username=auction.owner)
    owner = u.username

    # If the user is not the owner, then the del page can't be accessed
    if user != owner:
        dict["owner"] = auction.owner
        dict["same"] = ""
        return HttpResponseRedirect(reverse("viewitem", args=[item_id]))

    else:
        dict["owner"] = f"You, {auction.owner}"
        dict["same"] = "same"

        # Know if there is any bid
        bids = Bid.objects.filter(auction=item_id)
        dict["title_page"] = "Delete page"
        dict["msg_del"] = "Make sure you really want to delete this item"
        dict["color_tp"] = "red"
        if bids:
            if auction.is_active == True:
                if len(bids) == 1:
                    dict["stitle_page"] = "This Auction is still active with 1 bid"
                else:
                    dict["stitle_page"] = f"This Auction is still active with { len(bids) } bids"
                    
            else:
                dict["stitle_page"] = "This Auction is Closed"
                dict["titleimg"] = "Sold"
                dict["sold"] = "Sold"

        else:
            if auction.is_active == True:
                dict["stitle_page"] = "This Auction is still active with no bids"
            else:
                dict["stitle_page"] = "This Auction is Closed"
                dict["titleimg"] = "Unavailable"

        if request.method == "POST":
            # To get some important data
            pass_del = request.POST["pass_del"]

            if not pass_del:
                dict["msg_pas"] = "You must type your password"
                return render(request, "auctions/del_item.html",{
                "categgories": categories,
                "dict": dict,
                "auction": auction,
                "n_wl": n_wl
            })

            elif authenticate(request, username=user, password=pass_del) == None:
                dict["msg_pas"] = "Wrong password"
                return render(request, "auctions/del_item.html",{
                "categories": categories,
                "dict": dict,
                "auction": auction,
                "n_wl": n_wl
            })

            else:
                a = Auction.objects.get(id=item_id)
                cats = a.category.all()
                for i in cats:                    
                    this_cat = Category.objects.get(id=i.id)
                    this_cat.quantity -= 1
                    this_cat.save()  
                a.delete()
                return HttpResponseRedirect(reverse("index"))        

        else:
            return render(request, "auctions/del_item.html",{
                "categories": categories,
                "dict": dict,
                "auction": auction,
                "n_wl": n_wl
            })


@login_required
def watchlist(request):
    # unwrap all categories alphabetically in order to put them on top pages menu
    categories = Category.objects.order_by('category')
    # Count how many items there are in the watchlist
    if request.user.id:
        n_wl = User.objects.get(id=request.user.id).watchlist.count()
    else:
        n_wl = 0

    # To get the current user and create a dict
    user = request.user.username

    # To get the user's object
    user_object = User.objects.get(username=user)

    # unwrap only objects from Auctions that are on requested watchlist
    auctions = user_object.watchlist.all()

    # Know if there is a watchlist or not
    if not auctions:
        title_page = f"You don't have a watchlist yet, {user}"
        nothing = "nothing"
    else:
        title_page = f"Here's your watchlist, {user}"
        nothing = ""

    return render(request, "auctions/index.html", {
        "active_wl": "active",
        "categories": categories,
        "auctions": auctions,
        "title_page": title_page,
        "nothing": nothing,
        "n_wl": n_wl
    })