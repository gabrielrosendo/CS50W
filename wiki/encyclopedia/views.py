import os
import re
from django import forms
from django.shortcuts import render
from markdown import Markdown
from django.http import HttpResponse
from django.urls import reverse
from random import choice
from django.http import HttpResponseRedirect


from . import util
markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return HttpResponse("Page not found")

    else:
        entry_html = markdowner.convert(entryPage)
        return render(request, "encyclopedia/entry.html", {
            "entryTitle" : entry,
            "entry" : entry_html
        })

def search(request):
    value = request.GET.get('q','')
    if util.get_entry(value) is not None:
       return HttpResponseRedirect(reverse('entry', kwargs={'entry': value}))
    else:
        entries = []
        for entry in util.list_entries(

        ):
            if value.upper() in entry.upper():
                entries.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entries":entries
        })

class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title'] 
            description = form.cleaned_data['description'] 
            if util.get_entry(title) is not None:
                error = "Page with this title already exists"
                return render(request, "encyclopedia/new_entry.html",  {"error": error})
            else:
                try:
                    with open(f"entries/{title}.md", 'w') as file:
                        file.write(description)
                    print(f"File '{title}' created successfully.")
                    return HttpResponseRedirect(reverse('entry', kwargs={'entry': title}))
                except IOError as e:
                    error = f"Error occurred while creating the file: {e}"
    else:
        form = NewEntryForm()

    return render(request, "encyclopedia/new_entry.html", {"form": form})

def edit(request, entry):
    if request.method == "POST":
        edited_description = request.POST.get('description')
        with open(f"entries/{entry}.md",'w') as file:
            file.write(edited_description)
        return HttpResponseRedirect(reverse('entry', kwargs={'entry': entry}))
    else:
        entryPage = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {
            "entryTitle" : entry,
            "entry" : entryPage
        })

def random(request):
    entries_list = os.listdir('entries')
    random_entry = choice(entries_list)
    return HttpResponseRedirect(reverse('entry', kwargs={'entry': re.sub(r"\.md$", "", random_entry)}))
