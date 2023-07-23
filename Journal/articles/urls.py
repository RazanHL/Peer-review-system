from django.urls import path

from . import views
from mlapplications.views import quality_prediction, decision_prediction #, reviewer_recommender, arabert_predict, extra_reviewer_recommender
from mlapplications.views import quality_prediction
urlpatterns = [
    

    path('unsubmitted-articles', views.unsubmitted_articles, name='unsubmitted-articles'),
    path('pre-review-articles', views.pre_review_articles, name='pre-review-articles'),
    path('under-review-articles', views.under_review_articles, name='under-review-articles'),
    path('accepted-articles', views.accepted_articles, name='accepted-articles'),
    path('pre-publish-articles', views.pre_publish_articles, name='pre-publish-articles'),
    path('rejected-articles', views.rejected_articles, name='rejected-articles'),
    path('recently-updated', views.recently_edited, name='recently-updated'),

    path('user-unsubmitted-articles', views.user_unsubmitted_articles, name='user-unsubmitted-articles'),
    path('user-pre-review-articles', views.user_pre_review_articles, name='user-pre-review-articles'),
    path('user-under-review-articles', views.user_under_review_articles, name='user-under-review-articles'),
    path('user-accepted-articles', views.user_accepted_articles, name='user-accepted-articles'),
    path('user-pre-publish-articles', views.user_pre_publish_articles, name='user-pre-publish-articles'),
    path('user-rejected-articles', views.user_rejected_articles, name='user-rejected-articles'),
    path('user-recently-updated', views.user_recently_edited, name='user-recently-updated'), 
    path('user-published-articles', views.user_published_articles, name='user-published-articles'),

    path('reviewer-invites', views.reviewer_invites, name='reviewer-invites'),
    path('reviewer-under-review', views.reviewer_under_review, name='reviewer-under-review'),
    path('reviewer-done-review', views.reviewer_done_review, name='reviewer-done-review'),
    path('reviewer-recently-edited', views.reviewer_recently_edited, name='reviewer-recently-edited'),


    # path('search-articles/<int:page>', views.SearchArticlesList.as_view(), name='search-articles'),
    path('search-articles/<int:page>', views.search_articles, name='search-articles'),
    path('filter-articles/<int:page>', views.articles_filtered_list, name='filter-articles'),

    path('submit-article', views.submit_article, name='submit-article'),

    # path('editor/article-list', views.article_list, name='article-list'),
    # path('editor/article-list/pending/<int:article_id>', views.review_pending_article, name='review_article'),
    # path('scope-prediction/<int:article_id>', arabert_predict, name='scope-prediction'),
    # # path('editor/article-list/pending/quality-prediction/<int:article_id>', quality_prediction, name='quality-prediction'),
    # path('editor/article-list/pending/recommender-system/<int:article_id>', reviewer_recommender, name='recommender-system'),
    # path('editor/article-list/pending/plus-recommender-system/<int:article_id>', extra_reviewer_recommender, name='plus-recommender-system'),
    # path('editor/article-list/pending/decision-prediction/<int:article_id>', decision_prediction, name='decision-prediction'),

    path('published-articles/', views.published_articles, name='published-articles'),
    path('show-volume/<int:year>/<int:volume>/<int:issue>', views.show_volume, name='show-volume'),
    path('article-detailes/<int:article_id>', views.article_detailes, name='article-detailes'),

    # path('pendind-articles/', views.pendind_articles, name='pendind-articles'),
    path('article-review/<int:article_id>', views.article_review, name='article-review'),
    path('article-update/<int:article_id>', views.article_update, name='article-update'),
    path('article-delete/<int:article_id>', views.article_delete, name="article-delete"),
    # path('quality-prediction/<int:article_id>', quality_prediction, name='quality-prediction'),
    # path('add-author-to-article', views.add_author_to_article, name="add-author-to-article"),
    # path('set-reviewer/<int:user_id>', views.set_reviewer, name='set-reviewer'),
    path('filter-reviewers/<int:article_id>/<int:page>', views.filter_reviewers, name='filter-reviewers'),
    path('add-reviewer/<int:rev_id>/<int:article_id>', views.add_to_reviewer_list, name='add-reviewer'),
    path('remove-reviewer/<int:rev_id>/<int:article_id>', views.remove_from_reviewer_list, name='remove-reviewer'),
    # path('invite_reviewer/<int:rev_id>/<int:article_id>', views.invite_reviewer, name='invite_reviewer'),
    path('download-manuscript/<int:article_id>/<str:file_name>', views.download_manuscript, name='download_manuscript'),
    path('upload-article/<int:article_id>', views.upload_article, name='upload-article'),
    path('email-author/<int:author_id>/<int:article_id>', views.send_email, name='email-author'),

]