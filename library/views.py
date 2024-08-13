from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import resolve, reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.paginator import Paginator
from django.db.models import Q

from dettingen.utilities import render_to_pdf

from .forms import PartForm, PieceForm, SearchForm
from .models import Part, Piece


# Library Page
@login_required
def library_view(request):
    """View for the library page, including a search form and a form to add new pieces"""
    if request.method == "POST":
        piece_form = PieceForm(request.POST)
        if piece_form.is_valid():
            piece_form.save()
            messages.success(request, "New Piece Added")
            return HttpResponseRedirect(reverse("library"))

    queryset = Piece.objects.order_by("title").all()
    search_form = SearchForm(request.GET or None)
    if search_form.is_valid():
        query = search_form.cleaned_data.get("query")
        filter_value = search_form.cleaned_data.get("filter")

        if query:
            if filter_value == "":
                queryset = queryset.filter(
                    Q(title__icontains=query)
                    | Q(composer__icontains=query)
                    | Q(genre__icontains=query)
                    | Q(band_arrangement__icontains=query)
                )
            else:
                queryset = queryset.filter(**{filter_value + "__icontains": query})

    pieces = queryset
    piece_form = PieceForm()
    paginator = Paginator(pieces, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "pieces": page_obj,
        "piece_form": piece_form,
        "search_form": search_form,
        "current_url": resolve(request.path_info).url_name,
    }
    return render(request, "library/library.html", context)


def library_print_view(request):
    """View for the library print page, to print the library as a PDF"""
    pieces = Piece.objects.all()
    context = {"pieces": pieces}
    pdf = render_to_pdf("library/library_print.html", context)
    return HttpResponse(pdf, content_type="application/pdf")


def piece_edit(request, pk):
    """View for editing a piece using the piece form"""
    if request.method == "POST":
        piece = get_object_or_404(Piece, pk=pk)
        piece_form = PieceForm(request.POST, instance=piece)
        if piece_form.is_valid():
            piece_form.save()
            messages.success(request, "Update Successful")
            return HttpResponseRedirect(reverse("library"))

    queryset = Piece.objects.order_by("title").all()
    search_form = SearchForm(request.GET or None)
    if search_form.is_valid():
        query = search_form.cleaned_data.get("query")
        filter_value = search_form.cleaned_data.get("filter")

        if query:
            queryset = queryset.filter(**{filter_value + "__icontains": query})

    piece = get_object_or_404(Piece, pk=pk)
    piece_form = PieceForm(instance=piece)
    pieces = Piece.objects.all()
    context = {
        "pieces": pieces,
        "piece_form": piece_form,
        "search_form": search_form,
        "current_url": resolve(request.path_info).url_name,
    }
    return render(request, "library/library.html", context)


def piece_delete(request, pk):
    """View for deleting a piece"""
    piece = get_object_or_404(Piece, pk=pk)
    if request.method == "POST":
        piece.delete()
        messages.success(request, "Deletion Successful")
    return HttpResponseRedirect(reverse("library"))


# Piece View Page
def piece_view(request, pk):
    """Displays a piece's list of parts with a form to add new parts"""
    piece = get_object_or_404(Piece, pk=pk)
    part_form = PartForm()

    if request.method == "POST":
        part_form = PartForm(request.POST, request.FILES)
        part_form.instance.piece = piece
        if part_form.is_valid():
            part_form.save()
            messages.success(request, "New Part Added")
            return HttpResponseRedirect(reverse("piece_view", args=[pk]))

    context = {"piece": piece, "part_form": part_form}
    return render(request, "library/piece_view.html", context)


def part_view(request, pk):
    """Displays a part with a form to add new parts"""
    part = get_object_or_404(Part, pk=pk)
    part_form = PartForm()

    if request.method == "POST":
        part_form = PartForm(request.POST, request.FILES)
        part_form.instance.piece = part.piece
        if part_form.is_valid():
            part_form.save()
            messages.success(request, "New Part Added")
            return HttpResponseRedirect(reverse("part_view", args=[pk]))

    context = {"piece": part.piece, "part_form": part_form, "part": part}
    return render(request, "library/piece_view.html", context)


@xframe_options_exempt
def part_pdf_view(request, pk):
    """View for displaying a part's PDF file"""
    part = get_object_or_404(Part, pk=pk)
    return HttpResponse(part.pdf_file.file, content_type="application/pdf")


def part_edit(request, pk):
    """View for editing a part using the part form"""
    part = get_object_or_404(Part, pk=pk)
    part_form = PartForm(instance=part)

    if request.method == "POST":
        part = get_object_or_404(Part, pk=pk)
        part_form = PartForm(request.POST, instance=part)
        if part_form.is_valid():
            part_form.save()
            messages.success(request, "Update Successful")
            return HttpResponseRedirect(reverse("piece_view", args=[part.piece.pk]))

    context = {
        "piece": part.piece,
        "part_form": part_form,
        "current_url": resolve(request.path_info).url_name,
    }
    return render(request, "library/piece_view.html", context)


def part_delete(request, pk):
    """View for deleting a part"""
    part = get_object_or_404(Part, pk=pk)
    if request.method == "POST":
        part.delete()
        messages.success(request, "Deletion Successful")
    return HttpResponseRedirect(reverse("piece_view", args=[part.piece.pk]))
