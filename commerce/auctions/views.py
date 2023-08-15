from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django import forms

from .models import Listing, User

CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('home', 'Home'),
        ('other', 'Other')
    ]

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    price = forms.CharField(label="Starting price")
    image = forms.URLField(label = "Image URL")
    category = forms.ChoiceField(label="Category", choices=CATEGORY_CHOICES)

    
def index(request):
    listings = Listing.objects.all()
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
        ## create forms and add it to db
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
                print(new_listing)
                new_listing.save()
                return HttpResponseRedirect(reverse('index'))
            except Exception as e:
                return HttpResponse("Error")
        else:
            print(form.errors)  # Print the form validation errors

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
    if request.method == "POST":
        #check if bid is higher than current bid -> update bid
        pass
    listing = get_object_or_404(Listing, title=title)
    #retrieve info from db and pass it to front end
    return render(request, "auctions/listing.html", {
                  "listing" : listing
                }
            )

def category(request, name):
    listings = Listing.objects.filter(category=name.capitalize())
    return render(request, "auctions/category.html", {
            "listings": listings,
            "category": name
        }
    )