from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponse
from app.models import card as Card
from app.card.forms import CardForm
from django.core.exceptions import ObjectDoesNotExist
import re

def card(request):
    id = re.sub(r'/',"",re.sub(r'/card/',"", request.path)) # 我就是要用骯髒解你管我
    try:
        card = Card.objects.get(cid=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("<h1>Wrong card</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">")
    get_url = "http://" + request.META['HTTP_HOST'] + "/card/get/" + card.cid
    return render(request, "card/card.html", locals())

def edit(request):
    id = re.sub(r'/',"",re.sub(r'/card/edit/',"", request.path)) # 我就是要用骯髒解你管我
    try:
        card = Card.objects.get(cid=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("<h1>Wrong card</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">")

    if not request.POST:
        form = CardForm({"name": card.name, "value": card.value, "long_desc": card.long_desc, "active": card.active, "retrieved": card.retrieved, "modified_reason": ""})
        return render(request, "card/edit.html", locals())
    else:
        form = CardForm(request.POST)
        if form.is_valid():
            card.name = form.cleaned_data["name"]
            card.value = form.cleaned_data["value"]
            card.long_desc = form.cleaned_data["long_desc"]
            card.active = form.cleaned_data["active"]
            card.modified_reason = form.cleaned_data["modified_reason"]
            card.save()
        return HttpResponse("<h1>Submitted.</h1><meta http-equiv=\"refresh\" content=\"3; url=/card/" + card.cid + "\">")

def get(request):
    pass

def gen(request):
    pass

