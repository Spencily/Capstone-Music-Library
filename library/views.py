from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import resolve, reverse

from .forms import PieceForm
from .models import Piece


# Create your views here.
@login_required
def library_view(request):
    if request.method == "POST":
        piece_form = PieceForm(request.POST)
        if piece_form.is_valid():
            piece_form.save()
            messages.success(request, "New Piece Added")
            return HttpResponseRedirect(reverse("library"))

    pieces = Piece.objects.all()
    piece_form = PieceForm()
    context = {
        "pieces": pieces,
        "piece_form": piece_form,
        "current_url": resolve(request.path_info).url_name,
    }
    return render(request, "library/library.html", context)


def piece_edit(request, pk):
    if request.method == "POST":
        piece = get_object_or_404(Piece, pk=pk)
        piece_form = PieceForm(request.POST, instance=piece)
        if piece_form.is_valid():
            piece_form.save()
            messages.success(request, "Update Successful")
            return HttpResponseRedirect(reverse("library"))

    piece = get_object_or_404(Piece, pk=pk)
    piece_form = PieceForm(instance=piece)
    pieces = Piece.objects.all()
    context = {
        "pieces": pieces,
        "piece_form": piece_form,
        "current_url": resolve(request.path_info).url_name,
    }
    return render(request, "library/library.html", context)


def piece_delete(request, pk):
    piece = get_object_or_404(Piece, pk=pk)
    if request.method == "POST":
        piece.delete()
        messages.success(request, "Deletion Successful")
    return HttpResponseRedirect(reverse("library"))
