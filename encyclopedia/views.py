from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from random import choice

 
from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control mb-3', 'placeholder' : 'Example: CSS'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control mb-3', 'placeholder' : 'Example: CSS is a language that can be used to add style to an HTML page.'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_title(request, title):
    markdowner = Markdown()
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/404.html", {
            "entriesTitle": title
        })
    else:
        return render(request, "encyclopedia/entries.html", {
            "entries": markdowner.convert(entry),
            "entriesTitle": title
        })

def search(request):
    data = request.GET.get('q','')
    if (util.get_entry(data) is None):
        stringEntries = []
        for entries in util.list_entries():
            if data.upper() in entries.upper():
                stringEntries.append(entries)
        return render(request, "encyclopedia/index.html", {
            "entries": stringEntries,
            "search": True,
            "data": data
        })
    else:
        return HttpResponseRedirect(reverse("wiki:get_title", kwargs={"title": data}))

def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:get_title", kwargs={"title": title}))
            else:
                return render(request, "encyclopedia/newPage.html", {
                "form": form,
                "entry": title,
                "exist": True
                })
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form": form,
                "exist": False                
            })
    else:
        return render(request, "encyclopedia/newPage.html", {
            "form": NewPageForm(),
            "exist": False
        })

def edit(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:get_title", kwargs={"title": title}))
    else:
        entry = util.get_entry(title)
        if entry is None:
            return render(request, "encyclopedia/404.html", {
                "entriesTitle": entry
            })
        else:
            form = NewPageForm()
            form.fields["title"].initial = title
            form.fields["content"].initial = entry
            return render(request, "encyclopedia/editPage.html", {
                "form": form,
                "entriesTitle": entry
            })

def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return HttpResponseRedirect(reverse("wiki:get_title", kwargs={"title": entry}))
    