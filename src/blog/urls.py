from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.post_list, name='posts_list'),
    path('posts/tag/<tag_slug>', views.post_list, name='posts_by_tag'),
    path('posts/search/', views.post_search, name='search'),
    path('posts/category/<str:cate>', views.post_list, name='posts_by_category'),
    path('posts/<slug>', views.post_detail, name='post_detail'),
    path('posts/edit/<post_slug>', views.post_edit, name='post_edit'),
    path('posts/create/', views.postCreate, name='add_post'),
    path('posts/draft/', views.post_draft, name='post_draft'),
    path('posts/draft/<post_id>', views.add_to_draft, name='add_to_draft'),
    path('posts/delete/<post_id>', views.delete_post, name='post_delete'),
    path('posts/publish/<post_id>', views.post_publish, name='post_publish'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_comment/<comment_id>', views.delete_comment, name='delete_comment'),
]
