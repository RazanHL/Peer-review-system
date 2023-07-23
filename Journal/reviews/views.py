from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ReviewDetailes
from django.core.mail import EmailMessage, get_connection, send_mail
from django.conf import settings
from django.http import FileResponse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from profiles.models import Profiles, ProfilesFilter
from profiles.views import is_editor, is_reviewer, is_editor_or_reviewer
from .forms import InviteReviewForm, ReviewForm
from notifications.signals import notify

from articles.models import Article, STAGE_UNDER_REVIEW
import datetime
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy

# def review(request):
#     return render(request, 'home.html')
@login_required
@user_passes_test(is_editor)
def reviewer_filtered_list(request, page=1):
    filtered_profiles = ProfilesFilter(request.GET, queryset=Profiles.objects.all())
    result_counts = filtered_profiles.qs.count()
    
    paginator = Paginator(filtered_profiles.qs, per_page=10)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=2)
    context = {
               'filter': filtered_profiles.form, 
               'object_list': page_object,
               'result_counts': result_counts,
               'filter_items': filtered_profiles.data.items,}
    return render(request, 'articles/article_review.html', context)


# class InviteReviewer(FormView):
#     template_name = 'reviews/invite_reviewer.html'
#     form_class = InviteReviewForm
#     success_url = reverse_lazy('sent')

#     def form_valid(self, form):
#         form.send()
#         review = ReviewDetailes.objects.get(article_id=self.kwargs['article_id'], reviewer_id=self.kwargs['rev_id'])
#         review.invited = True
#         today = datetime.date.today() 
#         review.invited_at = today
#         review.invitation_expire_on = today + datetime.timedelta(7)
#         review.save()
#         rev_email = User.objects.get(id=self.kwargs['rev_id'])
#         article = Article.objects.get(id=self.kwargs['article_id'])
#         extra_context={
#             'rev_id' : rev_email,
#             'site': get_current_site(self.request),
#             'article': article,}
#         return super().form_valid(form)



# class InviteRev(TemplateView):
#     template_name = 'reviews/invite_reviewer.html'
#     form_class = InviteReviewForm
#     # success_url = reverse_lazy('sent')
#     # def get_redirect_url(self, **kwargs):
#     #     return reverse_lazy('sent',
#     #                         kwargs={'article_id': kwargs['article_id']})
    
#     def post(self, request, **kwargs):
#         # if self.request.method == "POST": 
#         # with get_connection(  
#         #    host=settings.EMAIL_HOST, 
#         #     port=settings.EMAIL_PORT,  
#         #     username=settings.EMAIL_HOST_USER, 
#         #     password=settings.EMAIL_HOST_PASSWORD, 
#         #     use_tls=settings.EMAIL_USE_TLS  
#         # ) as connection:  
#         subject = request.POST.get("subject")  
#         email_from = settings.EMAIL_HOST_USER  
#         recipient_list = [request.POST.get("email"), ]  
#         message_mail = request.POST.get("message")
        
#         #     EmailMessage(subject, message_mail, email_from, recipient_list, connection=connection).send()
#         send_mail(subject,message_mail, email_from, recipient_list, fail_silently=False) 
#         messages.success(request, 'invitation sent')
#         # actor = request.user
#         # recipient_reviewer = User.objects.get(id=rev_id)
#         # notify.send(actor, recipient=recipient_reviewer, verb='You have been invited by E.mail to review a manuscript',
#         #     target=review)
#         review = ReviewDetailes.objects.get(article_id=kwargs['article_id'], reviewer_id=kwargs['rev_id'])
#         review.invited = True
#         today = datetime.date.today() 
#         review.invited_at = today
#         review.invitation_expire_on = today + datetime.timedelta(7)
#         review.save()

#         actor = User.objects.get(id=kwargs['rev_id'])
#         target = Article.objects.get(id=kwargs['article_id'])           
#         recipient_reviewer = User.objects.filter(id=kwargs['rev_id'])
#         # recipient_authors = User.objects.filter(Article__id = article.id)
#         notify.send(actor, recipient=recipient_reviewer, verb='You have received an invitation to review a maniscript by email',
#                     target=target)
        
#         return redirect(to=reverse_lazy('sent', kwargs={'article_id': kwargs['article_id']}))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         rev_email = User.objects.get(id=kwargs['rev_id'])
#         article = Article.objects.get(id=kwargs['article_id'])
#         context["rev_id"] = rev_email
#         context["site"] = get_current_site(self.request)
#         context["article"] = article
#         context['article_id'] = kwargs['article_id']

#         return context
 


class InviteSuccessView(TemplateView):
    template_name = 'reviews/invite_success.html'

@login_required
@user_passes_test(is_editor)    
def invite_reviewer(request, rev_id, article_id):
    form = InviteReviewForm() 
    if request.method == "POST": 
        # with get_connection(  
        #    host=settings.EMAIL_HOST, 
        #     port=settings.EMAIL_PORT,  
        #     username=settings.EMAIL_HOST_USER, 
        #     password=settings.EMAIL_HOST_PASSWORD, 
        #     use_tls=settings.EMAIL_USE_TLS  
        # ) as connection:  
        subject = request.POST.get("subject")  
        email_from = settings.EMAIL_HOST_USER  
        recipient_list = [request.POST.get("email"), ]  
        message_mail = request.POST.get("message")  
        #     EmailMessage(subject, message_mail, email_from, recipient_list, connection=connection).send()
        send_mail(subject,message_mail, email_from, recipient_list, fail_silently=False) 
        messages.success(request, 'invitation sent')

        review = ReviewDetailes.objects.get(article_id=article_id, reviewer_id=rev_id)
        review.invited = True
        today = datetime.date.today() 
        review.invited_at = today
        review.invitation_expire_on = today + datetime.timedelta(7)
        review.save()
        actor = request.user
        target = ReviewDetailes.objects.get(article_id=article_id, reviewer_id=rev_id)           
        recipient_reviewer = User.objects.filter(id=rev_id)
        notify.send(actor, recipient=recipient_reviewer, verb='You have received an invitation to review a maniscript by email',
                    target=target)
        
        return redirect(to=reverse_lazy('sent', kwargs={'article_id':article_id}))
    else:
        rev_email = User.objects.get(id=rev_id)
        article = Article.objects.get(id=article_id)
        context = {
            'rev_id' : rev_email,
            'site': get_current_site(request),
            'article': article,
        }
        return render(request, 'reviews/invite_reviewer.html', context)
    # # return redirect(request.META.get('HTTP_REFERER'))
    # # else:
    #     # messages.warning(request, "can't send mail!")
    # rev_email = User.objects.get(id=rev_id)
    # article = Article.objects.get(id=article_id)
    # context = {
    #     'rev_id' : rev_email,
    #     'site': get_current_site(request),
    #     'article': article,
    # }
    # return render(request, 'reviews/invite_reviewer.html', context)

@login_required
@user_passes_test(is_reviewer)
def invite_response(request, rev_id, article_id):
    review = ReviewDetailes.objects.get(article_id=article_id, reviewer_id=rev_id)
    article = Article.objects.get(id=article_id)
    form = ReviewForm(request.POST, instance=review)
    if request.method == 'POST':
        replay = request.POST.get('replay')
        if replay == 'ACCEPT':
            review.replay = 'ACCEPT'
            today = datetime.date.today()
            review.review_start_on = today
            review.review_ends_on = today + datetime.timedelta(weeks=3)
            review.notes_to_editor = request.POST.get('notes_to_editor')
            review.save()
            rev = Profiles.objects.get(id=rev_id)
            article.reviewer.add(rev)
            article.current_status = STAGE_UNDER_REVIEW
            article.save()
            
            actor = request.user
            recipient_editors = User.objects.filter(profiles__user_type = 'EDITOR')
            notify.send(actor, recipient=recipient_editors, verb='The reviewer {} accepted review invitation'.format(actor),
                        target=article)

            context = {'article': article, 'form': form}
            return redirect(to=reverse_lazy('reviewing', kwargs={'rev_id': rev_id, 'article_id': article_id}))
        #    return render(request, 'reviews/reviewing.html', context)
        elif replay == 'REJECT':
            review.replay = 'REJECT'
            review.review_start_on = None
            review.review_ends_on = None
            review.notes_to_editor = request.POST.get('notes_to_editor')
            review.save()
            actor = request.user
            recipient_editors = User.objects.filter(profiles__user_type = 'EDITOR')
            notify.send(actor, recipient=recipient_editors, verb='The reviewer {} rejected review invitation'.format(actor),
                        target=article)
            return redirect(to='home')
    context = {
        'article': article,
        
               }
    return render(request, 'reviews/invite_response.html', context)

import pandas as pd

@login_required
@user_passes_test(is_editor_or_reviewer)
def revieweing(request, rev_id, article_id):
    review = ReviewDetailes.objects.get(article_id=article_id, reviewer_id=rev_id)
    article = Article.objects.get(id=article_id)
    score = None
    old_status = review.done_review
    settings.MEDIA_ROOT = (settings.BASE_DIR / 'Journal/media/documents/{}/{}'.format(article_id, review.reviewer_id))

    if request.method == "POST":
        form =  ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            print('old_status', old_status)
            print('form.cleaned_data', form.cleaned_data['done_review'])
            if form.cleaned_data['done_review'] == True and old_status == False:
                actor = User.objects.get(id=rev_id)
                recipient_editors = User.objects.filter(profiles__user_type = 'EDITOR')
                notify.send(actor, recipient=recipient_editors, verb='The reviewer {} has just funished reviewing Manuscript'.format(actor),
                            target=article)
                actor = User.objects.get(id=1)
                recipient_editors = User.objects.get(id=rev_id)
                notify.send(actor, recipient=recipient_editors, verb='THank you for reviewing Manuscript',
                            target=article)
            messages.success(request, 'form is saved')
        else:
            messages.warning(request, 'Form is not valid')
        q_list =[]
        for x in range(1,15):
            q = 'q'+ str(x)
            if form.cleaned_data[q]:
                q_list.append(form.cleaned_data[q])

        # print('wwwwwwww', q_list.count)
        # print ('qqqqqqqqqqq', q_list)
        df = pd.DataFrame(q_list, index=range(1,len(q_list)+1))
        vc = df.value_counts()
        dd = zip([x[0] for x in vc.index], [int(y) for y in vc.values]) 
        vc = vc.sort_index()
        print ('dataframe',dd)
        
        rr = 0
        for i,y in dd:
            rr += int(i) * int(y)
        
        if len(q_list)> 0:
            review.score = round(rr/len(q_list),2)
            review.save()    
    else:
        form = ReviewForm(instance=review)
        # review_decision_form = ReviewDecisionForm(instance=review)
    settings.MEDIA_ROOT = (settings.BASE_DIR / 'Journal/media')
    context = {'article': article, 'form': form, 'review': review}
    return render(request, 'reviews/reviewing.html', context)


@login_required
@user_passes_test(is_editor)
def download_review_file(request, article_id, rev_id, file_name):
    filePath = 'Journal/media/documents/{}/{}/{}'.format(article_id, rev_id, file_name)
    try:
        return FileResponse(open(filePath, 'rb'), as_attachment=True)
    except:
        messages.warning(request, "Can't download file")
        return redirect(request.META.get('HTTP_REFERER'))

# def review_pending_article(request, article_id):
#     reviewed_article = get_object_or_404(Article, id=article_id)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             new_comment = form.cleaned_data['new_comment']
#             if form.cleaned_data['approval'] == 'approve':
#                 reviewed_article.current_status = STAGE_ACCEPTED
#             else:
#                 reviewed_article.current_status = STAGE_REJECTED
#             reviewed_article.save()
#             if new_comment:
#                 # c = EditorNote(article=reviewed_article, text=new_comment)
#                 reviewed_article.save()
#             return HttpResponseRedirect(reverse('article-list'))
#     else:
#         form = ReviewForm()
#         return render(request, 'articles/review-article.html', {'form': form, 'article': reviewed_article})
#                                                                 #'comments': reviewed_article.Editornotes.all()})
