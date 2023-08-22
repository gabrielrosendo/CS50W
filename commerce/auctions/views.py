from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django import forms

from .models import Listing, User, Comment, Bid

CATEGORY_CHOICES = [
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Furniture', 'Furniture'),
    ('Home', 'Home'),
    ('Other', 'Other')
]


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    price = forms.CharField(label="Starting price")
    image = forms.URLField(label = "Image URL")
    category = forms.ChoiceField(label="Category", choices=CATEGORY_CHOICES)

    
def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
                  "listings" : listings,
                  "categories": CATEGORY_CHOICES
                }
            )


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            try:
                new_listing = Listing(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    image_url=form.cleaned_data['image'],
                    current_price=form.cleaned_data['price'],
                    seller=request.user,
                    category =form.cleaned_data['category']
                )    
                new_listing.save()
                return HttpResponseRedirect(reverse('index'))
            except Exception as e:
                return HttpResponse("Error")
        else:
            return HttpResponse(form.errors)  

    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })


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

def listing(request, title):
    listing = get_object_or_404(Listing, title=title)
    comments = Comment.objects.filter(listing=listing.pk)
    if listing.active is False:
        final_buyer = get_object_or_404(Bid, listing=listing)
        if final_buyer.buyer.id == request.user.id:
                message = "You have the final bid and this listing is closed"
                return render(request, "auctions/listing.html", {
                    "listing" : listing,
                    "message": message,
                    "comments": comments,
                    "message_color" : "message-green"
                })
    if request.user == listing.seller:
            return render(request, "auctions/listing.html", {
                    "listing" : listing,
                    "comments": comments,
                    "seller" : True
                })
    if request.method == "POST":
        if "bid" in request.POST:
            bid_str = request.POST["bid"]
            if bid_str and bid_str.strip():
                try:
                    bid = float(bid_str)
                    cur_bid = Bid.objects.get(listing=listing)
                    if bid > cur_bid.value:
                        cur_bid.value = bid
                        cur_bid.buyer = request.user
                        listing.current_price = cur_bid.value
                        listing.save()
                        cur_bid.save()
                    else:
                        return render(request, "auctions/listing.html", {
                            "listing" : listing,
                            "comments": comments,
                            "message" : "Your bid has to be higher than the current bid. Please try again.",
                            "message_color" : "message-red"
                        })
                except Bid.DoesNotExist:
                    cur_value = listing.current_price
                    if bid>=cur_value:
                        new_bid = Bid(listing=listing, value=bid, buyer = request.user)
                        listing.current_price = bid
                        listing.save()
                        new_bid.save()
                    else:
                        return render(request, "auctions/listing.html", {
                            "listing" : listing,
                            "comments": comments,
                            "message" : "Your bid has to be higher than the current bid. Please try again.",
                            "message_color" : "message-red"
                        })
            else:
                return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "message": "Bid value cannot be empty.",
                "message_color" : "message-red"
                })
        elif "comment" in request.POST:
            new_comment = Comment(
                text = request.POST["comment"],
                listing = listing,
                user = request.user
                )
            new_comment.save()


    #retrieve info from db and pass it to front end
    return render(request, "auctions/listing.html", {
                  "listing" : listing,
                  "comments": comments
                }
            )

def close_listing(request, title):
    listing = get_object_or_404(Listing, title=title)
    listing.active = False
    listing.save()
    return redirect('listing', title=title)


def category(request, name):
    listings = Listing.objects.filter(category=name.capitalize())
    return render(request, "auctions/category.html", {
            "listings": listings,
            "category": name
        }
    )

def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = get_object_or_404(Listing, id=listing_id)
        request.user.watchlist.add(listing)
    listings = request.user.watchlist.all()  
    return render(request, "auctions/watchlist.html", {"listings": listings})
