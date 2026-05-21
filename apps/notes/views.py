from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .forms import NoteForm
from .models import Note


@login_required
@require_GET
def note_list(request):
    notes = request.user.notes.all()
    return render(request, "notes/list.html", {"notes": notes})


@login_required
@require_http_methods(["GET", "POST"])
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect("notes:list")
    else:
        form = NoteForm()
    return render(request, "notes/create.html", {"form": form})


@login_required
@require_POST
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    return redirect("notes:list")
