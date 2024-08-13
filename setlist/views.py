from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import resolve, reverse

from library.models import Piece
from dettingen.utilities import render_to_pdf

from .forms import SetForm
from .models import Setlist


# Create your views here.
@login_required
def setlist_list(request):
    """View for the setlist page"""
    setlists = Setlist.objects.order_by("title").filter(created_by=request.user)
    return render(request, "setlist/setlist.html", {"setlists": setlists})


def setlist_view(request, pk):
    """Display a single setlist"""
    setlists = Setlist.objects.filter(created_by=request.user)
    setlist = get_object_or_404(setlists, pk=pk)
    return render(
        request,
        "setlist/setlist.html",
        {"setlist": setlist, "setlists": setlists},
    )


def setlist_print_view(request, id):
    """View for the setlist print page, to print the setlist as a PDF"""
    setlists = Setlist.objects.filter(created_by=request.user)
    setlist = get_object_or_404(setlists, pk=id)
    context = {'setlist': setlist}
    pdf = render_to_pdf("setlist/setlist_print.html", context)
    return HttpResponse(pdf, content_type="application/pdf")


def setlist_add(request):
    """View to add a new setlist"""
    if request.method == "POST":
        setlist_form = SetForm(request.POST)
        if setlist_form.is_valid():
            setlist_form = setlist_form.save(commit=False)
            setlist_form.created_by = request.user
            setlist_form.save()
            messages.success(request, "New Setlist Added")
            return HttpResponseRedirect(reverse("setlist"))

    setlist_form = SetForm()
    context = {
        "setlist_form": setlist_form,
        "current_url": resolve(request.path_info).url_name,
    }
    return render(request, "setlist/setlist_form.html", context)


def setlist_edit(request, pk):
    """View to edit a setlist"""
    if request.method == "POST":
        setlist = get_object_or_404(Setlist, pk=pk)
        setlist_form = SetForm(request.POST, instance=setlist)
        if setlist_form.is_valid():
            setlist_form.save()
            messages.success(request, "Update Successful")
            return HttpResponseRedirect(reverse("setlist"))

    setlist = get_object_or_404(Setlist, pk=pk)
    setlist_form = SetForm(instance=setlist)
    setlists = Setlist.objects.all()
    context = {
        "setlists": setlists,
        "setlist_form": setlist_form,
        "current_url": resolve(request.path_info).url_name,
    }
    return render(request, "setlist/setlist_form.html", context)


def setlist_delete(request, pk):
    """View to delete a setlist"""
    setlists = Setlist.objects.filter(created_by=request.user)
    setlist = get_object_or_404(setlists, pk=pk)
    if request.method == "POST":
        setlist.delete()
        messages.success(request, "Deletion Successful")
    return HttpResponseRedirect(reverse("setlist"))
