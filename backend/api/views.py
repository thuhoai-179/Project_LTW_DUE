from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import *
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum
from django.db.models import Count
from django.dispatch import receiver
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def index(request):  
    return render(request,"base.html")
def home(request):
    return render(request, 'home.html')
def trangchu(request):
    trending_posts=Post.objects.all().order_by('-view')[:5]
    categories = Category.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')[:5]
    popular_posts=Post.objects.all().order_by('-date')[:5]
    context={
        'trending_posts':trending_posts,
        'categories':categories,
        'popular_posts':popular_posts,
    }
    return render(request,"trangchu.html",context)

def danhmuc(request):
    categories=Category.objects.all()
    return render(request,'danhmuc.html',{'categories':categories})

def test_code(request):
    trending_posts=Post.objects.all().order_by('-view')[:5]
    categories = Category.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')[:5]
    popular_posts=Post.objects.all().order_by('-date')[:5]
    context={
        'trending_posts':trending_posts,
        'categories':categories,
        'popular_posts':popular_posts,
    }
    return render(request,"test_code.html",context)

def vechungtoi(request):
    return render(request,'vechungtoi.html')
def lienhe(request):
    return render(request,'lienhe.html')


def trang(request):
    return render(request,'trang.html')

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  
    return render(request, 'register.html', {'form': form})

def user_login(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('trang')  
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def search(request):
    query = request.GET.get('q', '') 
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)  
        )
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search.html', context)


def baiviet(request):
    baiviet=Post.objects.all()
    count_baiviet=baiviet.count()
    return render(request,'baiviet.html',{'baiviet':baiviet,'count_baiviet':count_baiviet}) 

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.profile = request.user.profile 
            post.save()
            return redirect('user_posts')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    profile = post.user.profile
    post.view += 1
    post.save()
    comments = post.comments.filter(parent=None).order_by('-date')
    likes_count = post.likes.count()
    is_bookmarked = Bookmark.objects.filter(user=request.user, post=post).exists() if request.user.is_authenticated else False
    form = CommentForm()
    total_comments = post.comments.count()
    bookmarks_count = post.bookmark_set.count()
    if request.method == 'POST':
        if 'bookmark' in request.POST:
            if not request.user.is_authenticated:
                return redirect("login")
            else:
                if is_bookmarked:
                    Bookmark.objects.filter(user=request.user, post=post).delete()
                else:
                    Bookmark.objects.create(user=request.user, post=post)
                is_bookmarked = Bookmark.objects.filter(user=request.user, post=post).exists()
                if post.user != request.user:
                    Notification.objects.create(
                    user=post.user,  # Người nhận thông báo (người tạo bài viết)
                    post=post,
                    type="Bookmark",
                    initiator=request.user  # Người lưu bài viết
                )
                return redirect('post_detail', id=post.id)
        else   :            
            form = CommentForm(request.POST)
            if not request.user.is_authenticated:
                return redirect('login')
            else:
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.post = post
                    comment.user = request.user
                    reply_id = request.POST.get('reply_id')
                    if reply_id:
                        comment.parent = Comment.objects.get(id=reply_id) 

                    comment.save()
                    if post.user != request.user:
                        Notification.objects.create(
                            user=post.user,  
                            post=post,
                            type="Comment",
                            initiator=request.user 
                        )

                    elif comment.parent:
                        parent_comment = comment.parent
                        if parent_comment.user != request.user:
                            Notification.objects.create(
                                user=parent_comment.user,  # Người nhận thông báo (người bị trả lời)
                                post=post,
                                type="Reply",
                                initiator=request.user  # Người trả lời
                            )
                    return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'likes_count': likes_count,
        'is_bookmarked':is_bookmarked,
        'profile':profile,
        'total_comments':total_comments,
        'bookmarks_count':bookmarks_count,
    })
    
@login_required
def edit_post(request,id):
    post = get_object_or_404(Post, id=id)  
    if post.user != request.user:
        return HttpResponseForbidden("Bạn không có quyền chỉnh sửa bài viết này.")
    if request.method == "POST":
        form = Edit_PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("user_posts") 
    else:
        form = Edit_PostForm(instance=post)
    
    return render(request, "edit_post.html", {"form": form, "post": post})  

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user 
    if user in post.likes.all():
        
        post.likes.remove(user) 
    else:
        post.likes.add(user)  

    if post.user != user:
            Notification.objects.create(
                user=post.user, 
                post=post,
                type="Like",
                initiator=user 
            )
    return redirect('post_detail', id=post.id)

@login_required
def user_posts(request):
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(user=request.user) 
        count_post=user_posts.count()
    else:
        user_posts = []  

    return render(request, 'user_posts.html', {'posts': user_posts,'count_post':count_post}) 

def saved_posts(request):
    saved_posts = Bookmark.objects.filter(user=request.user).select_related('post')
    return render(request, 'saved_posts.html', {
        'saved_posts': saved_posts
    })
    
@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user == comment.user or request.user.is_staff:
        comment.delete()
    else:
        messages.error(request, "Bạn không có quyền xóa bình luận này.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    for notification in notifications:
            notification.seen = True
            notification.save()

    return render(request, "notifications.html", {"notifications": notifications}) 


def category_post_list(request,id):
    category = get_object_or_404(Category, id=id)
    posts = Post.objects.filter(category=category, status="Active").order_by("-date")   
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'category_post_list.html', context)

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('danhmuc')
    else:
        form = CategoryForm()
    return render(request, 'category_create.html', {'form': form, 'action': 'Create'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # if category != request.user:
    #     return HttpResponseForbidden("Bạn không có quyền xóa danh mục này!!!.")
    if request.method == 'POST':
        category.delete()
        return redirect('danhmuc')
    return render(request, 'category_confirm_delete.html', {'category': category})

@login_required
def  post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return HttpResponseForbidden("Bạn không có quyền xóa bài viết này.")
    if request.method == 'POST':
        post.delete()
        return redirect('user_posts')
    return render(request, 'post_confirm_delete.html', {'post': post})


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('danhmuc')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_edit.html', {'form': form, 'action': 'Edit'}) 

@login_required
def follow_user(request, id):
    profile = get_object_or_404(Profile, id=id)
    if profile.user == request.user:
        return redirect('user_profile', id=id)
    if request.user.profile in profile.followers.all():
        profile.followers.remove(request.user.profile) 
    else:
        profile.followers.add(request.user.profile)  
    return redirect('user_profile', id=id)


def user_profile(request, id):
    profile = get_object_or_404(Profile, id=id)
    user_posts = Post.objects.filter(user=profile.user).order_by('-date')
    followers = profile.followers.all()
    following = profile.following.all()
    is_following = request.user.profile in profile.followers.all() if request.user.is_authenticated else False

    if request.method == 'POST':
        if 'follow' in request.POST:
            # Kiểm tra xem người dùng có phải đang tự follow chính mình hay không
            if profile.user != request.user:
                if is_following:
                    profile.followers.remove(request.user.profile)
                    is_following = False
                else:
                    profile.followers.add(request.user.profile)
                    is_following = True

                    # Nếu muốn tạo thông báo, có thể bật lại đoạn code dưới đây
                    # if profile.user != request.user:
                    #     Notification.objects.create(
                    #         user=profile.user,  # Người nhận thông báo (người được follow)
                    #         type="Follow",
                    #         initiator=request.user  # Người thực hiện follow
                    #     )
        return redirect('user_profile', id=profile.id)

    context = {
        'profile': profile,
        'user_posts': user_posts,
        'followers': followers,
        'following': following,
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)


@login_required
def follower_detail(request,id):
    profile = get_object_or_404(Profile, id=id)
    user_posts = Post.objects.filter(user=profile.user).order_by('-date')
    followers = profile.followers.all()
    following = profile.following.all()
    is_following = request.user.profile in profile.followers.all() if request.user.is_authenticated else False 
    context = {
        'profile': profile,
        'user_posts': user_posts,
        'followers':followers,
        'following':following,
        'is_following':is_following,
    }
    return render(request,'follower_detail.html',context)

@login_required
def following_detail(request,id):
    profile = get_object_or_404(Profile, id=id)
    user_posts = Post.objects.filter(user=profile.user).order_by('-date')
    followers = profile.followers.all()
    following = profile.following.all()
    is_following = request.user.profile in profile.followers.all() if request.user.is_authenticated else False 
    context = {
        'profile': profile,
        'user_posts': user_posts,
        'followers':followers,
        'following':following,
        'is_following':is_following,
    }
    return render(request,'following_detail.html',context) 

def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if profile.user != request.user:
        return HttpResponseForbidden("Bạn không có quyền xóa bài viết này.")
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user_profile.html', {'form': form, 'profile': profile})


def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    user_posts = Post.objects.filter(user=profile.user).order_by('-date')
    context = {
        'profile': profile,
        'user_posts': user_posts,

    }
    return render(request, 'profile.html', context)



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Giữ người dùng đăng nhập sau khi đổi mật khẩu
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password_complete')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
#Hàm view cho trang chuyển hướng sau khi đổi pass
def change_password_complete(request):
    return render(request, 'change_password_complete.html')