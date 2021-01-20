from django.contrib import messages
from django import forms
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown
md = markdown.Markdown()


from . import util

class searchForm(forms.Form):
    searchInput = forms.CharField(
        label="Search",
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Encyclopedia'
            })
        )

class newPageForm(forms.Form):
    newTitle = forms.CharField(
        label="Title",
        widget=forms.TextInput(attrs={
            'placeholder': 'Title'
            })
    )
    newContent = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={
            'placeholder': 'content',
            'rows':20,
            'cols':120
        })
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchForm()
    })

def search(request):
    if request.method == "POST":
        form = searchForm(request.POST)
        results = []
        if form.is_valid():
            search = form.cleaned_data["searchInput"]
            entries = util.list_entries()
            for entry in entries:
                if entry.lower() == search.lower():
                    return HttpResponseRedirect(reverse('encyclopedia:content', args=[entry]))
                elif search.lower() in entry.lower():
                    results.append(entry)
        else:
            return render(request, "encyclopedia/search.html", {
                "form": form
            })

    return render(request, "encyclopedia/search.html", {
        "form": searchForm(),
        "results": results
    })

def content(request, name):
    if util.get_entry(name) == None:
        raise Http404("Page does not exist")
    else:
        return render(request, "encyclopedia/content.html", {
            "entries": util.list_entries(),
            "form": searchForm(),
            "name": name,
            "text": md.convert(util.get_entry(name))
        })

def newPage(request):
    if request.method == "POST":
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["newTitle"]
            content = form.cleaned_data['newContent']
            entries = util.list_entries()
            for entry in entries:
                if entry.lower() == title.lower():
                    messages.error(request, "Page already exists")
                    createKey = False
            if createKey:
                util.save_entry(title,content)
                messages.success(request, "New page created")

    return render(request, "encyclopedia/newpage.html", {
    "form": searchForm(),
    "newpageform": newPageForm()
    })