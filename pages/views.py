from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Editorial_board, Contact_journal
from django.contrib.auth.models import User
from profiles.models import Profiles
from .forms import UpdateEditorialBoard, ContactUsForm
from django.contrib import messages
import os
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.auth.decorators import user_passes_test, login_required
from profiles.views import is_editor
from django.http import FileResponse

def home(request):
    return render(request, 'home.html')

def editorial_board(request):
    ed_board = Editorial_board.objects.all()
    international_editorial_board = []
    national_editorial_board = []
    international_reviewers = []
    national_reviewers = []
    editor_in_chief, co_editor_in_chief, secretary_of_journal, statistical_analysis, website_adminstrator, en_proofreading, ar_proofreading =None,None,None,None,None,None,None
    for member in ed_board:
        if member.job_title == 'رئيس_التحرير':
            editor_in_chief = member
        elif member.job_title == 'رئيس_التحرير_المشارك':
            co_editor_in_chief = member
        elif member.job_title == 'أمين_سر_المجلة':
            secretary_of_journal = member
        elif member.job_title == 'التحليل_الإحصائي':
            statistical_analysis = member
        elif member.job_title == 'مشرف_الموقع':
            website_adminstrator = member
        elif member.job_title == 'مدقق_لغة_انكليزي':
            en_proofreading = member
        elif member.job_title == 'مدقق_لغة_عربي':
            ar_proofreading = member
        elif member.job_title == 'هيئة_التحرير_الدولية':
            international_editorial_board.append(member)
        elif member.job_title == 'هيئة_التحرير_المحلية':
            national_editorial_board.append(member)
        elif member.job_title == 'المحكمين_الدوليين':
            international_reviewers.append(member)
        elif member.job_title == 'المحكمين_المحليين':
            national_reviewers.append(member)
    journal_editors = {
        'Editor in Chief': editor_in_chief,
        'Co-editor in Chief': co_editor_in_chief,
        'Secretary of Journal': secretary_of_journal,
        'statistical_analysis': statistical_analysis,
        'Website Adminstrator': website_adminstrator,
        'English Language Proofreading': en_proofreading,
        'Arabic Language Proofreading': ar_proofreading,
        }

    context = {'ed_board': ed_board,
               'journal_editors': journal_editors,
               'international_editorial_board': international_editorial_board,
               'national_editorial_board': national_editorial_board,
               'international_reviewers': international_reviewers,
               'national_reviewers': national_reviewers,
               }
    return render(request, 'pages/editorial_board.html', context)


@login_required
@user_passes_test(is_editor)
def add_editorial_member(request):
    if request.method == 'POST':
        ed_form = UpdateEditorialBoard(request.POST)
        if ed_form.is_valid():
            ed_form.save()
            messages.success(request, 'saved successfully!')
        else:
            messages.warning(request, 'error')
        return redirect(to='editorial-board')
    else:
        ed_form = UpdateEditorialBoard()
    return render(request, 'pages/update_editorial_board.html', {'ed_form': ed_form})
  

@login_required
@user_passes_test(is_editor)
def update_editorial_member(request, member_id):
    editor = Editorial_board.objects.get(id = member_id)
    if request.method == 'POST':
        ed_form = UpdateEditorialBoard(request.POST, instance= editor)
        if ed_form.is_valid():
            ed_form.save()
            messages.success(request, 'saved successfully!')
        else:
            messages.warning(request, 'error')
        return redirect(to='editorial-board')
    else:
        ed_form = UpdateEditorialBoard(instance= editor)
    return render(request, 'pages/update_editorial_board.html', {'ed_form': ed_form, 'editor': editor})


@login_required
@user_passes_test(is_editor)
def delete_editorial_member(request, member_id):
    member = Editorial_board.objects.get(id = member_id)
    member.delete()
    messages.success(request, 'member is deleted')
    return redirect(to='editorial-board')


def publication_ethics(request):
    return render(request, 'pages/publication_ethics.html')


def guidelines(request):
    return render(request, 'pages/guidelines.html')


def download_guidelines(request, file_name):
    if file_name == 1:
        path = 'Journal/files/Guidelines_arabic.pdf'
    elif file_name == 2:
        path = 'Journal/files/Guidelines_english.pdf'
    elif file_name == 3:
        path = 'Journal/files/Copyright-form-arabic.pdf'
    else:
        path = 'Journal/files/Copyright-form-english.pdf'
    return FileResponse(open(path, 'rb'), as_attachment=True)


def copyright_form(request):
    return render(request, 'pages/copyright_form.html')


def contact(request):
    if request.method == 'POST':
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            recipient_editors = User.objects.filter(profiles__user_type = 'EDITOR')
            if request.user.is_anonymous:
                actor = Contact_journal.objects.get(id=contact_form.instance.pk) #User.objects.get(pk=1)
            else:
                actor = request.user

            notify.send(actor, recipient=recipient_editors, verb='Contact-Us request by {}'.format(actor),
                       target=contact_form.instance)
            messages.success(request, 'Your message was sent. Thank you for contacting us we will respond to your message as soon as possible')
        else:
            messages.warning(request, "Can't send the message now!")
        return redirect(to='home')
    else:
        contact_form = ContactUsForm()
    all_messages = Contact_journal.objects.all()
    context = {'contact_form': contact_form , 'all_messages': all_messages}
    return render(request, 'pages/contact_us.html', context)


def contact_details(request, pk):
    cont = Contact_journal.objects.get(id=pk)
    context = {'cont': cont}
    return render(request, 'pages/contact_details.html', context)


def show_notifications(request, notification_id):
    notifcation = get_object_or_404(Notification, pk=notification_id, recipient= request.user)
    notifcation.mark_as_read()
    return redirect(notifcation.target.get_absolute_url())


def mark_all_notify_as_read(request):
    notifcation = Notification.objects.filter(recipient=request.user)
    for notify in notifcation:
        notify.mark_as_read()
    return redirect(request.META.get('HTTP_REFERER'))
