import re

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render, get_object_or_404

from .models import Author, Tag, Quote
from .forms import AuthorForm, TagForm, QuoteForm


NUMBER_OF_QUOTES_PER_PAGE = 10
NUMBER_OF_TOP_TAGS = 10


def get_quote_tags_list_per_page_and_page_ids(quotes, page_id):
    quote_tags_list = []
    len_of_quotes = len(quotes)
    previous_page_id = page_id - 1
    OFFSET = NUMBER_OF_QUOTES_PER_PAGE * previous_page_id
    LIMIT = NUMBER_OF_QUOTES_PER_PAGE * page_id
    if LIMIT >= len_of_quotes:
        LIMIT = len_of_quotes
        next_page_id = 0
    else:
        next_page_id = page_id + 1
    quotes = quotes[OFFSET:LIMIT]
    for quote in quotes:
        tags = quote.tags.all()
        quote_tags_list.append((quote, tags))
    return quote_tags_list, previous_page_id, next_page_id


# Create your views here.
def main(request, page_id):
    quotes = Quote.objects.all()
    (
        quote_tags_list,
        previous_page_id,
        next_page_id,
    ) = get_quote_tags_list_per_page_and_page_ids(quotes, page_id)
    context = {
        "quote_tags_list": quote_tags_list,
        "previous_page_id": previous_page_id,
        "next_page_id": next_page_id,
    }
    return render(request, "quotes/index.html", context)


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.born_location = re.sub(
                "^in ", "", author.born_location, flags=re.IGNORECASE
            )
            author.added_by = request.user
            author.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/add_author.html", {"form": form})
    return render(request, "quotes/add_author.html", {"form": AuthorForm()})


@login_required
def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.added_by = request.user
            tag.title = tag.title.replace("#", "")
            tag.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/add_tag.html", {"form": form})
    return render(request, "quotes/add_tag.html", {"form": TagForm()})


@login_required
def add_quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.added_by = request.user
            new_quote.save()
            choice_tags = Tag.objects.filter(id__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            return redirect(to="quotes:main")
        else:
            return render(
                request,
                "quotes/add_quote.html",
                {"authors": authors, "tags": tags, "form": form},
            )
    return render(
        request,
        "quotes/add_quote.html",
        {"authors": authors, "tags": tags, "form": QuoteForm()},
    )


def author(request, author_full_name_url):
    author = Author.objects.filter(Author.full_name_url == author_full_name_url).first()
    return render(request, "quotes_app/author.html", {"author": author})


def tag(request, tag_title, page_id):
    tag = get_object_or_404(Tag, title=tag_title)
    quotes = Quote.objects.filter(tags__in=[tag])
    (
        quote_tags_list,
        previous_page_id,
        next_page_id,
    ) = get_quote_tags_list_per_page_and_page_ids(quotes, page_id)
    context = {
        "quote_tags_list": quote_tags_list,
        "previous_page_id": previous_page_id,
        "next_page_id": next_page_id,
        "tag_title": tag_title,
    }
    return render(request, "quotes_app/tag.html", context)


def top_tags(request):
    tags = Tag.objects.annotate(num_quote=Count("quote")).order_by("-num_quote")[
        :NUMBER_OF_TOP_TAGS
    ]
    return render(request, "quotes_app/top_tags.html", {"tags": tags})