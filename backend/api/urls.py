from django.urls import path,include
from api import views as api_views
from django.contrib.auth import views as auth_views

urlpatterns = [
     
    path('', api_views.trang, name='trang'),
    path('login/', api_views.user_login, name='login'),
    path('logout/', api_views.user_logout, name='logout'),
    path('register/', api_views.register, name='register'),
    path('search/', api_views.search, name='search_posts'),
    path('trangchu/',api_views.trangchu,name='trang_chu'),
    path('trang/',api_views.trang,name='trang'),
    path('vechungtoi/',api_views.vechungtoi,name='vechungtoi'),
    path('lienhe/',api_views.lienhe,name='lienhe'),
    path('baiviet/',api_views.baiviet,name='baiviet'),
    path('add-post/', api_views.add_post, name='add_post'),
    path('post/<int:id>/', api_views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', api_views.like_post, name='like_post'),
    path('my-posts/', api_views.user_posts, name='user_posts'),
    path('edit_post/<int:id>/', api_views.edit_post, name="edit_post"),
    path('post/<int:pk>/delete/', api_views.post_delete, name='post_delete'),
    path('profile/<int:id>/', api_views.user_profile, name='user_profile'),
    path('profile/',api_views.profile,name='profile'),
    path('category/<int:id>/', api_views.category_post_list, name='category_post_list'),
    path('categories/create/',api_views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', api_views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', api_views.category_delete, name='category_delete'),
    path('danhmuc/',api_views.danhmuc,name='danhmuc'),
    path('test_code/',api_views.test_code,name='test_code'),
    path('thongbao',api_views.test_code,name='thongbao'),
    path('trangchu/thongbao/', api_views.notifications, name='notifications'),
    path('saved-posts/', api_views.saved_posts, name='saved_posts'),
    path('delete-comment/<int:id>/', api_views.delete_comment, name='delete_comment'),
    path('follow/<int:id>/', api_views.follow_user, name='follow_user'),
    path('myprofile/', api_views.my_profile, name='myprofile'),
    path('follower_detail/<int:id>/',api_views.follower_detail,name='follower_detail'),
    path('following_detail/<int:id>/',api_views.following_detail,name='following_detail'),
    path('change-password/', api_views.change_password, name='change_password'),
    #sau khi đổi pass thì chuyến hướng tới trang này, sau đó đăng nhập lại để vào
    path('change-password/complete', api_views.change_password_complete, name='change_password_complete'),
    #URL quên pass
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    # URL xác nhận đặt lại mật khẩu
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    # URL để nhập mật khẩu mới
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),

    # URL hoàn tất đặt lại mật khẩu
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]


