from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import SearchForm, PostCreateForm, CommentForm
from datetime import datetime
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string


# Create your views here.


class HomeBlog(View):
    
    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request,*args,**kwargs)
    #
    def get(self, request):
        # check if it's a search GET request from form. If it is, then make DB queries
        
        if request.GET.get('search') == 'search':
            form = SearchForm(request.GET)
            if form.is_valid():
                posts = form.return_query()
                context = {"posts": posts}
                return render(request, 'blog/blog_listing.html', context)
        # if is not a search GET request, return all posts
        
        posts = Post.objects.all()
        context = {"posts": posts}
        return render(request, 'blog/blog_listing.html', context)

    def post(self, request):
        # check if it's a search GET request from form. If it is, then make DB queries
        print(request.POST)
        if request.POST.get('search') == 'search':
            form = SearchForm(request.GET)
            if form.is_valid():
                posts = form.return_query()
                context = {"posts": posts}
                return render(request, 'blog/blog_listing.html', context)
        # if is not a search GET request, return all posts
    
        context = {" ": ""}
        return render(request, 'blog/blog_listing.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm()
    # comment_form = CommentForm(request.POST)
    # if comment_form.is_valid():
    #     user = User.objects.get(username=request.user)
    #     comment_form.instance.user=user
    #     comment_form.instance.post = post
    #     comment_form.save()
    #
    #     return redirect(reverse ('pages:blog:post_detail', kwargs={'post_id': post_id}))
    comments = post.get_comments()
    return render(request, 'blog/blog_post_detail.html',
                  {'post': post, 'comment_form': comment_form, 'comments': comments})




class PostCommentActions(View):
    """ This is the POST view function that creates a new comment and returns a JSON response"""
    
    def post(self, request):
     
        if request.POST.get('action')=="delete":
            # check if user wants to delete a comment and then find the comment with specific id and detele it.
            # return status when action completed and then hide DIV with comment in HTML page
            comment_id = request.POST.get('commentid')
            comment_obj = Comment.objects.get(pk=comment_id)
            comment_obj.delete()
            return JsonResponse({'status':'delete'})
        
        elif request.POST.get('action')=='update':
            comment_id = request.POST.get('commentid')
            comment_obj = Comment.objects.get(pk=comment_id)
            # check if user wants to update a comment. Find the right comment usind provided id and the return him comment data in JSON format
            return JsonResponse({'status': 'update',
                                 'content': str(comment_obj.content),
                                 'username': str( comment_obj.user.userprofile.username),
                                 'user_pic':  str( comment_obj.user.userprofile.picture.url),
                                 'comment_id': comment_id})
        
        elif request.POST.get("action")=="save_updated_comment":
            # user wants to update a comment.Find specific comment and change it content
            comment_id = request.POST.get("commentid")
            comment_content = request.POST.get("new_content")
            comment_obj = Comment.objects.get(pk=comment_id)
            comment_obj.content = comment_content
            comment_obj.save()
            return JsonResponse({'status':True})
        
        
        else:
            post_id = request.POST.get('postid')
            content = request.POST.get('content')
            post = get_object_or_404(Post, pk=post_id)
            user = User.objects.get(username=request.user)
            comment = Comment(user=user, post=post, content=content)
            comment.save()
            # creating a new comment instance and saving. Return True if saved
            return JsonResponse({'status': True, 'content': str(comment.content), 'username': str(comment.user.userprofile.username),'user_pic':  str(comment.user.userprofile.picture.url)})



class CommentAction(View):
    def post(self, request, post_id, comment_id):
        """check if the user wants to update or to delete a comment post """
        if request.POST['perform'] == "delete":
            comment_obj = Post.objects.get(pk=post_id).comment_set.filter(pk=comment_id)[0]
            comment_obj.delete()
            return redirect(reverse('pages:blog:post_detail', kwargs={'post_id': post_id}))
        
        elif request.POST['perform'] == "update":
            comment_obj = Post.objects.get(pk=post_id).comment_set.filter(pk=comment_id)[0]
            comment_form = CommentForm(request.POST, instance=comment_obj)
            comment_form.save()
            return redirect(reverse('pages:blog:post_detail', kwargs={'post_id': post_id}))
    
    def get(self, request, post_id, comment_id):
        """return comment form with an instance of the comment in order to be changed by the user"""
        post = Post.objects.get(pk=post_id)
        comment_obj = Post.objects.get(pk=post_id).comment_set.filter(pk=comment_id)[0]
        comment_form = CommentForm(instance=comment_obj)
        
        return render(request, 'blog/blog_post_detail.html', {'post': post,
                                                              'update_comment_form': comment_form})


class UpdatePost(View):
    
    def get(self, request, post_id):
        # check and see if user want to update this post or delete it the pass a variable action with info about user intention
        if request.GET["action"] == "edit":
            action = "edit"
        else:
            action = "delete"
        post = Post.objects.get(pk=post_id)
        form = PostCreateForm(instance=post)
        return render(request, "blog/blog_post_update.html",
                      context={"post_update_form": form, "post": post, "action": action})
    
    def post(self, request, post_id):
        
        if request.method == "POST":
            post = Post.objects.get(pk=post_id)
            form = PostCreateForm(request.POST, request.FILES, instance=post)
            # check if user request POST action is for updating of for deleting post
            if request.POST["action"] == "Update Post":
                if form.is_valid():
                    form.save()
                    return redirect(post)
            else:
                post.delete()
                return redirect("pages:blog:home-view")


# class ReviewPost(View):
#     def post(self,request, post_id):
#         post = get_object_or_404(Post, pk=post_id)
#         user = get_object_or_404(User, username=request.user)
#         if request.POST['action']=="like":
#             if post.likes.filter(username=user.username).exists():
#                 # print("Exists")
#                 post.likes.remove(user)
#             else:
#                 # print("Does not exists")
#                 post.likes.add(user)
#
#         if request.POST['action'] == "wishlist":
#             if post.wishlist.filter(username=user.username).exists():
#                 # print("Exists")
#                 post.wishlist.remove(user)
#             else:
#                 # print("Does not exists")
#                 post.wishlist.add(user)
#
#         return redirect(reverse ('pages:blog:post_detail', kwargs={'post_id': post_id}))


class ReviewPost(View):
    
    def post(self, request):
        data = {}
        id = request.POST.get('postid')
        user = User.objects.get(username=request.user)
        post = Post.objects.get(pk=id)
        
        if request.POST.get('type') == 'like':
            if post.likes.filter(username=user).exists():
                post.likes.remove(user)
                data['status'] = 'Like'
            else:
                post.likes.add(user)
                data['status'] = 'Unlike'
            data['like_count'] = post.number_likes()
        else:
            if post.wishlist.filter(username=user.username).exists():
                post.wishlist.remove(user)
                data['status'] = 'add wishlist'
            else:
                post.wishlist.add(user)
                data['status'] = 'remove wishlist'
        
        return JsonResponse(data, )
