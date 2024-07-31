from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .forms import SetForm
from .models import Setlist


# Create your views here.
@login_required
def setlist_list(request):
    if request.method == "POST":
        set_form = SetForm(request.POST)
        if set_form.is_valid():
            set_form.save()
            return HttpResponseRedirect(reverse("setlist"))

    setlists = Setlist.objects.all()
    set_form = SetForm()
    return render(
        request, "setlist/setlist.html", {"setlists": setlists, "set_form": set_form}
    )


def setlist_view(request, pk):
    setlist = get_object_or_404(Setlist, pk=pk)
    setlists = Setlist.objects.all()
    return render(
        request, "setlist/setlist.html", {"setlist": setlist, "setlists": setlists}
    )


def setlist_edit(request, pk):
    if request.method == "POST":
        setlist = get_object_or_404(Setlist, pk=pk)
        set_form = SetForm(request.POST, instance=setlist)
        if set_form.is_valid():
            set_form.save()
            messages.success(request, "Update Successful")
            return HttpResponseRedirect(reverse("setlist"))

    setlist = get_object_or_404(Setlist, pk=pk)
    set_form = SetForm(instance=setlist)
    setlists = Setlist.objects.all()
    return render(
        request, "setlist/setlist.html", {"setlists": setlists, "set_form": set_form}
    )


def setlist_delete(request, pk):
    setlist = get_object_or_404(Setlist, pk=pk)
    if request.method == "POST":
        setlist.delete()
        messages.success(request, "Deletion Successful")
    return HttpResponseRedirect(reverse("setlist"))


def setlist_add(request):
    if request.method == "POST":
        set_form = SetForm(request.POST)
        if set_form.is_valid():
            set_form.save()
            return HttpResponseRedirect(reverse("setlist"))

    set_form = SetForm()
    return render(request, "setlist/setlist.html", {"set_form": set_form})
