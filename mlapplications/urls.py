from django.urls import path
from django.contrib.auth import views as auth_views
# from .forms import LoginForm
from . import views

urlpatterns = [
    path('scope-prediction/<int:article_id>', views.arabert_predict, name='scope-prediction'),
    path('quality-prediction/<int:article_id>', views.quality_prediction, name='quality-prediction'),
    path('decision-prediction/<int:article_id>', views.decision_prediction, name='decision-prediction'),
    path('recommender-system/<int:article_id>', views.reviewer_recommender, name='recommender-system'),
    path('plus-recommender-system/<int:article_id>', views.extra_reviewer_recommender, name='plus-recommender-system'),
]