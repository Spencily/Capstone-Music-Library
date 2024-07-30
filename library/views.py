from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import PieceForm
from .models import Piece


# Create your views here.
@login_required
def library_view(request):
    if request.method == "POST":
        piece_form = PieceForm(request.POST)
        if piece_form.is_valid():
            piece_form.save()
            return HttpResponseRedirect(reverse("library"))
        
    pieces = Piece.objects.all()
    piece_form = PieceForm()
    return render(
        request, "library/library.html", {"pieces": pieces, "piece_form": piece_form}
    )


def piece_edit(request, pk):
    if request.method == "POST":
        piece = get_object_or_404(Piece, pk=pk)
        piece_form = PieceForm(request.POST, instance=piece)
        if piece_form.is_valid():
            piece_form.save()
            return HttpResponseRedirect(reverse("library"))

    piece = get_object_or_404(Piece, pk=pk)
    piece_form = PieceForm(instance=piece)
    pieces = Piece.objects.all()
    return render(
        request, "library/library.html", {"pieces": pieces, "piece_form": piece_form}
    )


def piece_delete(request, pk):
    piece = get_object_or_404(Piece, pk=pk)
    piece.delete()
    return HttpResponseRedirect(reverse("library"))
