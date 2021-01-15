from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, name):
    return render(request, "encyclopedia/content.html", {
        "entries": util.list_entries(),
        "name": name,
        "text": util.get_entry(name)
    })
