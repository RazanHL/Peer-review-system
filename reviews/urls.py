from django.urls import path
from . import views

urlpatterns = [
    path('select-reviewer', views.reviewer_filtered_list, name='select-reviewer'),
    # path('invite-reviewer/<int:rev_id>/<int:article_id>', views.send_email, name='invite-reviewer'),
    path('invite/<int:rev_id>/<int:article_id>', views.invite_reviewer, name='invite'),
    path('invite-success/<int:article_id>', views.InviteSuccessView.as_view(), name='sent'),
    path('invite-response/<int:rev_id>/<int:article_id>', views.invite_response, name='invite-response'),
    path('reviewing/<int:rev_id>/<int:article_id>', views.revieweing, name='reviewing'),
    path('download-review-file/<int:article_id>/<str:rev_id>/<str:file_name>', views.download_review_file, name='download-review-file'),
    # path('save-evaluation-form/<int:rev_id>/<int:article_id>', views.save_evaluation_form, name='save-evaluation-form'),
]