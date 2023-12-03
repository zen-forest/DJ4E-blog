from django.shortcuts import render, get_object_or_404
from .models import Post 
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm

def post_list(request):
    post_list = Post.published.all()
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
  
  return render(request, 'blog/post/detail.html', 
                {'post': post})


class PostListView(ListView):
   # custom QuerySet instead of retrieving all objects
   queryset = Post.published.all()
   context_object_name = 'posts'
   paginate_by = 4
   template_name = 'blog/post/list.html'

def post_share(request, post_id):
   # retrieve post by id 
   post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
   if request.method == "POST":
      # form was submitted 
      form = EmailPostForm(request.POST)
      if form.is_valid():
         #Form fields validation
         cd = form.cleaned_data
         #send email
      else:
         form=EmailPostForm()
      return render(request, 'blog/post/share.html', {'post', post, 'form', form})