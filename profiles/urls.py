from django.urls import path
# from profiles import views
from django.contrib.auth import views as auth_views
# from .forms import LoginForm
from . import views

urlpatterns = [
    path('wherenext/', views.where_next,name='where-next'),
    path('author', views.author_dashboard, name='author-dashboard'),
    path('editor', views.editor_dashboard, name='editor-dashboard'),
    path('reviewer', views.reviewer_dashboard, name='reviewer-dashboard'),
    path('publisher', views.publisher_dashboard, name='publisher-dashboard'),
    # path('', views.ProfileView.as_view(), name='profile'),
    # path('', views.profiles, name='users-profile'),
    path('search-profiles/<int:page>', views.search_profiles, name='search-profiles'),
    path('filter-profiles/<int:page>', views.profiles_filtered_list, name='filter-profiles'),
    
    # path('authors/<int:page>', views.all_authors, name= 'all-authors'),
    path('view-profile/<int:user_id>', views.view_profile, name= 'view-user-profile'),
    path('update-profile/<int:user_id>', views.update_profile, name= 'update-user-profile'),
    path('create-profile/', views.creat_profile, name= 'create-user-profile'),
    path('delete-profile/<int:user_id>', views.delete_profile, name= 'delete-user-profile'),

    path('show-reviewers-table/<int:page>', views.show_reviewers_table, name='show-reviewers-table'),
    path('add-reviewer-publications', views.add_reviewer_publications, name='add-reviewer-publications'),
    path('update-reviewer-publications/<int:id>', views.update_reviewer_publications, name='update-reviewer-publications'),
    path('delete-reviewer-publications/<int:id>', views.delete_reviewer_publications, name='delete-reviewer-publications'),
    path('set-reviewer-publications/<int:rev_id>', views.set_reviewer_publications, name='set-reviewer-publications'),
    path('search-publications/<int:page>', views.search_publications, name='search-publications'),

]