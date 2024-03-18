from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
       tag = get_object_or_404(Tag, slug=tag_slug)
       post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)
    try:
      posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(1)

    return render(request,
                 'blog/post/list.html',
                 {'posts': posts})


def post_detail(request, year, month, day, post):
   post = get_object_or_404(Post,
                           status=Post.Status.PUBLISHED,
                           slug=post,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)

   form = CommentForm()
   comments = post.comments.filter(active=True)
  # Form for users to comment 
  
   return render(request, 'blog/post/detail.html', 
                {'post': post, 'comments': comments, 'form': form})


class PostListView(ListView):
   # custom QuerySet instead of retrieving all objects
   queryset = Post.published.all()
   context_object_name = 'posts'
   paginate_by = 4
   template_name = 'blog/post/list.html'


def post_share(request, post_id):
   
   post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
   sent = False
   form = EmailPostForm()  # Initialize the form here for GET requests

   if request.method == "POST":
      # form was submitted 
      form = EmailPostForm(request.POST)
      if form.is_valid():
         # Form fields validation
         cd = form.cleaned_data
         post_url = request.build_absolute_uri(post.get_absolute_url())
         subject = f"{cd['name']} recommends you read {post.title}"
         message = f"Read {post.title} at, {cd['name']} comments: {cd['comments']}" 
         send_mail(subject, message, 'prototyping.the.future.777@gmail.com', [cd['to']])
         sent = True

   return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
   post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
   comment = None 
   #comment was posted
   form = CommentForm(data=request.POST)
   if form.is_valid():
      # Create a comment object without saving it the db
      comment = form.save(commit=False)
      # assign the post to the comment
      comment.post = post
      # save to the db
      comment.save()
   return render(request, 'blog/post/comment.html', {'post':post, 'form':form, 'comment': comment})