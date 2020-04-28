from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment


from .forms import CommentForm
from django.shortcuts import render, get_object_or_404


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


#class PostDetailView(DetailView):
#    model = Post


    


class PostDetailView(DetailView):
    model = Post
    slug_url_kward = 'pk_slug'

    def get_object(self, queryset=None):
        # This function overrides DetialView.get_object()

        # Use a custom queryset if provided; this is required for subclasses
        if queryset is None:
            queryset = self.get_queryset()

        # Next, look up our primary key or slug
        pk_slug = self.kwargs.get(self.slug_url_kwarg)
        # If the pk_slug is not None and it is just digits treat as pk
        # Otherwise if it is not None treat as slug
        if pk_slug is not None and pk_slug.isdigit():
          queryset = queryset.filter(pk=pk_slug)
        elif pk_slug is not None:
          slug_field = self.get_slug_field()
          queryset = queryset.filter(**{slug_field: pk_slug})

 # Raise an error if there is no pk_slug in the URLconf

          if pk_slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with an object "
                "pk_slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def dispatch():
        post = get_object_or_404(Post)
        comments = post.comments.filter(active=True, slug=slug)
        new_comment = None



        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
            else:
                comment_form = CommentForm()
                return render(request, post_detail.html, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                          'comment_form': comment_form})

    # Create Comment object but don't save to database yet
             # Assign the current post to the comment
             # Save the comment to the database

   #     return self.get(*args, **kwargs)
    #elif request.method == 'POST':
     #   return self.post(*args, **kwargs)
    #elif #... and so on

    #def post_detail(request, slug):
     #   post = get_object_or_404(Post, slug=slug)
      #  comments = post.comments.all()
       # new_comment = None
        # Comment posted
        #if request.method == 'POST':
         #   comment_form = CommentForm(data=request.POST)
          #  if comment_form.is_valid():
            # Create Comment object but don't save to database yet
           #     new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            #    new_comment.post = post
            # Save the comment to the database
             #   new_comment.save()
        #else:
         #   comment_form = CommentForm()

        #return render(request, template_name, {'post': post,
         #                                  'comments': comments,
          #                                 'new_comment': new_comment,
           #                                'comment_form': comment_form})
 

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')


def post_detail(request, pk):
    template_name = 'post_detail.html'

    comments = Comment.objects.filter(post=pk ,active=True)
    post = Post.objects.get(pk=pk)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})