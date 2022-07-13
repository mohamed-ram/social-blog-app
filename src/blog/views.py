from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post, Comment
from django.core.paginator import Paginator
from .forms import ContactForm, CommentForm, PostForm, PostEditForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

import difflib
from functools import reduce
import operator


def home(request):
    return render(request, 'blog/home.html', {})


@login_required(login_url='account:login')
def postCreate(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            return redirect('blog:posts_list')
    return render(request, 'blog/post_form.html', {'form': form})


@login_required(login_url='account:login')
def post_edit(request, post_slug):
    # post = Post.objects.published().get(slug=post_slug)
    post = Post.objects.get(slug=post_slug)
    print(post)
    form = PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post edited successfully')
            return redirect('blog:post_detail', slug=post_slug)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required(login_url='account:login')
def post_list(request, tag_slug=None, cate=None):
    my_following = request.user.profile.following.all()
    print(my_following)
    posts = Post.objects.published().filter(Q(author__in=my_following) | Q(author=request.user))

    if tag_slug:
        posts = Post.objects.published().filter(tags__contains=tag_slug)

    if cate:
        posts = Post.objects.published().filter(category__title=cate)

    # if search:
    #     query = request.GET.get('q')
    #     posts = Post.objects.published().filter(title__icontains=query)

    # posts counter
    posts_count = posts

    # upcoming posts
    upcoming_posts = Post.objects.get_queryset().upcoming()

    # draft
    draft_posts = Post.objects.draft()

    # categories
    categories = Category.objects.all()
    cate_num = {}
    for category in categories:
        cate_num[category] = category.post_set.filter(publish=True).count()

    latest_posts = Post.objects.published().order_by('-publish_at')[:2]
    paginator = Paginator(posts, 8)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    # form
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            email = cd['email']
            message = cd['message']
            send_mail(f"message form blog app, user: {name}", message, 'coloncodes@gmail.com', [email, ])
            messages.success(request, 'successfully sent!')
            return redirect('blog:posts_list')
    else:
        form = ContactForm()

    context = {'posts': page_obj, 'categories': categories,
               'latest_posts': latest_posts, 'upcoming_posts': upcoming_posts,
               'form': form, 'tag_slug': tag_slug, 'cate': cate,
               'posts_count': posts_count, 'cate_num': cate_num, 'query': request.GET.get('q')}

    return render(request, 'blog/index.html', context)


@login_required(login_url='account:login')
def post_search(request):
    empty = True
    query = request.GET.get('q')
    words = []
    for post in Post.objects.published():
        words += post.title.split()
        words += post.text.split()
        words += post.tags.split('-')
        words += post.category.title
    # print(words)
    search_query = [q for q in difflib.get_close_matches(query, words, cutoff=0.6, n=1)]
    print(search_query)
    posts = Post.objects.none()
    test_posts = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    if test_posts.count() > 0:
        posts = test_posts
    else:
        for q in search_query:
            posts = Post.objects.published().filter(Q(title__icontains=q) | Q(text__icontains=q) |
                                                    Q(category__title__icontains=q) | Q(tags__icontains=q) |
                                                    Q(title__icontains=query) | Q(text__icontains=query))
        empty = False
    return render(request, 'blog/search.html', {'posts': posts, 'empty': empty, 'search_query': search_query})


@login_required(login_url='account:login')
def post_draft(request):
    posts = Post.objects.draft().filter(author=request.user)
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required(login_url='account:login')
def add_to_draft(request, post_id):
    post = Post.objects.published().get(id=post_id)
    post.publish = False
    post.save()
    messages.success(request, f'{post} | Added To Draft Posts Successfully!')
    return redirect('blog:post_draft')


@login_required(login_url='account:login')
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    messages.success(request, 'deleted successfully!')
    return redirect('blog:posts_list')


@login_required(login_url='account:login')
def post_publish(request, post_id):
    post = Post.objects.draft().get(id=post_id)
    post.publish = True
    post.save()
    messages.success(request, 'Published successfully')
    return redirect('blog:posts_list')


@login_required(login_url='account:login')
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post_tags = [tag.strip() for tag in post.tags.split('-')]

    # add comment..
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user
            comment.email = request.user.email
            comment.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()

    # related posts
    posts = Post.objects.published().exclude(pk=post.id)
    related_posts = posts.filter(category=post.category)[:2]

    context = {'post': post, 'tags': post_tags, 'form': form, 'comments': comments,
               'related_posts': related_posts, 'now': timezone.now()}
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='account:login')
def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('blog:post_detail', slug=comment.post.slug)


@login_required(login_url='account:login')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print('done')
    else:
        form = ContactForm()
    return render(request, 'blog/index.html', {'form': form})


@login_required(login_url='account:login')
def dashboard(request):
    return render(request, 'blog/dashboard.html', {})

