from django.shortcuts import render
from django.http import Http404
import markdown
md = markdown.Markdown()


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, name):
    if util.get_entry(name) == None:
        raise Http404("Page does not exist")
    else:
        return render(request, "encyclopedia/content.html", {
            "entries": util.list_entries(),
            "name": name,
            "text": md.convert(util.get_entry(name))
        })
