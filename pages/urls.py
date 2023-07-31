from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pages/editorial-board', views.editorial_board, name="editorial-board"),
    path('pages/add-editorial-member', views.add_editorial_member, name='add-editorial-member'),
    path('pages/edit-editorial-member/<int:member_id>', views.update_editorial_member, name='edit-editorial-member'),
    path('pages/delete-editorial-member/<int:member_id>', views.delete_editorial_member, name='delete-editorial-member'),
    path('pages/publication-ethics', views.publication_ethics, name='publication-ethics'),
    path('pages/guidelines', views.guidelines, name='guidelines'),
    path('pages/download-guidelines/<int:file_name>', views.download_guidelines, name='download-guidelines'),
    path('pages/copyright-form', views.copyright_form, name='copyright-form'),
    path('pages/contact-us', views.contact, name='contact-us'),
    path('pages/contact-details/<int:pk>', views.contact_details, name='contact-details'),
    path('pages/show-notifications/<int:notification_id>', views.show_notifications, name="show_notifications"),
    path('pages/mark-as-read', views.mark_all_notify_as_read, name="mark-as-read"),
]