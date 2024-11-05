from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from .models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail
#class base
from django.views.generic import ListView


def post_list(request):
    
    posts=Post.published.all();
    # pagination with 3 posts per page
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    
    except PageNotAnInteger:
        # if page is not an integer deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )

# alternative way to implement post_list using class-based views
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    



def post_detail(request, year, month,day, post):

    post = get_object_or_404(
        Post, 
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
        )

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )


def post_share(request, post_id):
    post=get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']})"
                 f"recommends you reading {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(subject, 
                      message, 
                      from_email=None, 
                      recipient_list=[cd['to']]
                      )
            sent = True
    else:
        form = EmailPostForm()
    return render(
            request,
            'blog/post/share.html',
            {'post': post, 'form': form, 'sent': sent}
        )

