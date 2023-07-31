from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect #, render_to_response
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage, get_connection, send_mail
from django.conf import settings 
from notifications.signals import notify
from .forms import ArticleForm, FinalArticleForm, AuthorOrderForm, AuthorOrderFormSet, ReviewerpublicationForm
from .models import (STAGE_UNDER_REVIEW, Article, ArticlesFilter, Author_Order, STAGE_PRE_REVIEW, 
                     STAGE_PUBLISHED, STAGE_REJECTED, STAGE_ACCEPTED, STAGE_READY_FOR_PUBLICATION, 
                     STAGE_UNSUBMITTED, STAGE_TYPESETTING, Reviewer_publication)
from profiles.models import Profiles, ProfilesFilter
from reviews.models import ReviewDetailes
from profiles.views import is_editor, is_author, is_reviewer, is_publisher
from django.db.models import Max
import datetime
from django.db.models import Q


@login_required
def submit_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        art = None
        if form.is_valid():
            new_article = form.save()
            art = Article.objects.get(id=new_article.id)                        
            messages.success(request, 'Please upload manuscript files to complete supmission')
            art.author.add(request.user)

            actor = request.user
            recipient_editors = User.objects.filter(profiles__user_type = 'EDITOR')
            notify.send(actor, recipient=recipient_editors, verb='New Submission by {}'.format(actor),
                       target=art)
            # authors = Article.objects.filter(id=article_id).values_list('author') 
            actor = User.objects.get(id=1)               
            recipient_authors = request.user #User.objects.filter(id__in = author_ids)
            notify.send(actor, recipient=recipient_authors, verb='Thank you for adding new submission to our journal',
                       target=art)
            
            return redirect(to='upload-article', article_id= art.id)            
        else:
            messages.warning(request, "Can't add new paper!")

        context = {'form': form, 'article_id': art.id}
        return render(request, 'articles/article_form.html', context)
    else:
        form = ArticleForm()
        context = {'form': form}
        return render(request, 'articles/article_form.html', context)


@login_required
def upload_article(request, article_id): 
    settings.MEDIA_ROOT = (settings.BASE_DIR / 'Journal/media/documents/{}'.format(article_id))
    article = Article.objects.get(id=article_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance= article)
        if form.is_valid():
            # article.author.add(request.user)
            article.current_status = STAGE_PRE_REVIEW 

            article.save()
            author_ids = []
            authors = Article.objects.filter(id=article_id).values_list('author')
            for i in authors:
                author_ids.append(i[0])
                author = User.objects.get(id=i[0])
                add_element = Author_Order.objects.create(article_id=article, author_id=author, email=author.email)
                add_element.save()
            return redirect(to='home')
        else:
            messages.warning(request, 'Invalid form!')
    else:
        form = ArticleForm(instance= article)
        
    settings.MEDIA_ROOT = (settings.BASE_DIR / 'Journal/media')
    context = {'form': form}
    return render(request, 'articles/article_files.html', context)


def download_manuscript(request, article_id, file_name):
    filePath = 'Journal/media/documents/{}/{}'.format(article_id, file_name)
    try:
        return FileResponse(open(filePath, 'rb'), as_attachment=True)
    except:
        messages.warning(request, "Can't download file")
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def article_update(request, article_id):
    article = Article.objects.get(id=article_id)
    settings.MEDIA_ROOT = (settings.BASE_DIR / 'Journal/media/documents/{}'.format(article_id))
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        order_form = AuthorOrderFormSet(request.POST or None, request.FILES or None, instance=article, prefix='ordered_authors')
        if article_form.is_valid():
            article_form.save()
            new_authors = Article.objects.filter(id=article_id).values_list('author')
            old_authors = Author_Order.objects.filter(article_id=article.id)

            new_authors_ids = [a[0] for a in new_authors]
            for auth in old_authors:
                if auth.author_id.id not in new_authors_ids:
                    auth.delete()
            to_add_author = [x for x in new_authors if x not in old_authors.values_list('author_id')]

            for i in to_add_author:
                add_author = User.objects.get(id=i[0])
                add_element = Author_Order.objects.create(article_id=article, author_id=add_author, email=add_author.email)
                add_element.save()

            editor = request.user
            
            messages.success(request, 'Manuscript is updated')
            
            
            # return redirect(to=next)
            # return redirect(request.META.get('HTTP_REFERER'))
            return redirect('article-detailes', article_id= article_id)
    else:
        article_form = ArticleForm(instance=article)
        order_form = AuthorOrderFormSet(instance=article, prefix='ordered_authors') 
    settings.MEDIA_ROOT = (settings.BASE_DIR / 'Journal/media')
    context = {'form': article_form, 'order_form':order_form, 'article': article}
    return render(request, 'articles/article_update.html', context)


@login_required
@user_passes_test(is_editor)
def article_delete(request, article_id):
    article = Article.objects.get(id = article_id)
    article.delete()
    messages.success(request, 'Manuscript is deleted')
    return redirect(to='home')


def published_articles(request):
    max_volume = Article.objects.filter(current_status=STAGE_PUBLISHED).aggregate(Max('volume'))['volume__max']
    ye = 2014
    years, res, indx, issue = [], [], [], []
    for vol in range(1, max_volume + 1):
       indx.append(vol)
       years.append(ye)
       ye = ye + 1
       counts, issue_list = [], []
       max_issue = Article.objects.filter(volume=vol).aggregate(Max('issue'))['issue__max']
       for i in range(1, max_issue +1):
           issue_list.append(i)
           counts.append(Article.objects.filter(volume=vol, issue=i).count())
       issue.append(issue_list)
       res.append(counts)
    result = zip(indx, issue, years)

    context = {'volumes': result}
    return render(request,'articles/article_published.html', context)


def show_volume(request, year, volume, issue):
    articles = Article.objects.filter(volume=volume, issue=issue).order_by('from_page')
    context = {'articles': articles, 'year': year,'volume': volume, 'issue': issue}
    return render(request, 'articles/show-volume.html', context)


def article_detailes(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    authors_order = Author_Order.objects.filter(article_id=article_id).order_by('order')#.values()
    authors = article.author.all()
    names, order = [], []
    
    ar_institute = [auth.author_id.profiles.work_address or '' for auth in authors_order]
    en_institute = [auth.author_id.profiles.en_work_address or '' for auth in authors_order]

    ar_institute_set = set(ar_institute)
    ar_institute_list = list(ar_institute_set)
    en_institute_set = set(en_institute)
    en_institute_list = list(en_institute_set)

    ar_names, en_names = [], []
    for i,ins in enumerate(ar_institute_list, 1): 
        ar_names.extend([auth.profiles.name or '', i, authors_order.filter(author_id=auth.id).values_list('order')[0][0] or '', authors_order.filter(author_id=auth.id).values_list('contact')[0][0] or ''] for auth in authors if  auth.profiles.work_address == ins)
    ar_names.extend([auth.profiles.name or '', '', authors_order.filter(author_id=auth.id).values_list('order')[0][0] or '', authors_order.filter(author_id=auth.id).values_list('contact')[0][0] or ''] for auth in authors if  auth.profiles.work_address == None)       

    for i,ins in enumerate(en_institute_list, 1): 
        en_names.extend([auth.profiles.en_name or '', i, authors_order.filter(author_id=auth.id).values_list('order')[0][0] or '', authors_order.filter(author_id=auth.id).values_list('contact')[0][0] or ''] for auth in authors if  auth.profiles.en_work_address == ins)
    en_names.extend([auth.profiles.en_name or '', '', authors_order.filter(author_id=auth.id).values_list('order')[0][0] or '', authors_order.filter(author_id=auth.id).values_list('contact')[0][0] or ''] for auth in authors if  auth.profiles.en_work_address == None)       


    # for i,authoro in enumerate(authors_order):
    #     ar_names.extend([auth.profiles.name or '', i, authors_order.filter(author_id=auth.id).values_list('order')[0][0] or '', authors_order.filter(author_id=auth.id).values_list('contact')[0][0] or ''] for auth in authors if  auth.profiles.work_address == ins)
    #     ar_names.extend([authoro.profiles.name or '', i, authoro.order or '', authoro.contact or ''])
        
    
    context = {'article': article, 
            # 'names' :names, 
            # 'institute': institute_list,
            'ar_names': ar_names,
            'en_names': en_names,
            'ar_institute': ar_institute_list,
            'en_institute': en_institute_list,
            'authors_order': authors_order,
            'site': get_current_site(request),
            }

    return render(request,'articles/article_detail.html', context)


@login_required
@user_passes_test(is_editor)
def unsubmitted_articles(request):
    unsubmitted = Article.objects.filter(current_status=STAGE_UNSUBMITTED)
    context = {'unsubmitted':unsubmitted,}
    return render(request, 'articles/unsubmitted_articles.html', context)


@login_required
@user_passes_test(is_editor)
def pre_review_articles(request):
    pre_review = Article.objects.filter(current_status=STAGE_PRE_REVIEW)
    context = {'pre_review': pre_review,}
    return render(request, 'articles/pre_review_articles.html', context) 


@login_required
@user_passes_test(is_editor)
def under_review_articles(request):
    under_review = Article.objects.filter(current_status=STAGE_UNDER_REVIEW)
    context = {'under_review': under_review,}
    return render(request, 'articles/under_review_articles.html', context) 


@login_required
@user_passes_test(is_editor)
def accepted_articles(request):
    accepted = Article.objects.filter(current_status=STAGE_ACCEPTED)
    context = {'accepted': accepted,}
    return render(request, 'articles/accepted_articles.html', context) 


@login_required
@user_passes_test(is_editor)
def pre_publish_articles(request):
    pre_publish = Article.objects.filter(current_status=STAGE_TYPESETTING)
    context = {'pre_publish': pre_publish,}
    return render(request, 'articles/pre_publish_articles.html', context) 


@login_required
@user_passes_test(is_editor)
def rejected_articles(request):
    rejected = Article.objects.filter(current_status=STAGE_REJECTED).order_by('received_date')
    context = {'rejected': rejected,}
    return render(request, 'articles/rejected_articles.html', context)


@login_required
@user_passes_test(is_editor)
def recently_edited(request):
    today = datetime.date.today() 
    range = today - datetime.timedelta(7)
    recently_updated = Article.objects.filter(updated_at__gt=range)
    context = {'recently_updated': recently_updated,}
    return render(request, 'articles/recently_updated.html', context)


@login_required
def user_unsubmitted_articles(request):
    unsubmitted = Article.objects.filter(author=request.user).filter(current_status=STAGE_UNSUBMITTED)
    context = {'unsubmitted':unsubmitted,}
    return render(request, 'articles/unsubmitted_articles.html', context)


@login_required
def user_pre_review_articles(request):
    pre_review = Article.objects.filter(author=request.user).filter(current_status=STAGE_PRE_REVIEW)
    context = {'pre_review': pre_review,}
    return render(request, 'articles/pre_review_articles.html', context) 


@login_required
def user_under_review_articles(request):
    under_review = Article.objects.filter(author=request.user).filter(current_status=STAGE_UNDER_REVIEW)
    context = {'under_review': under_review,}
    return render(request, 'articles/under_review_articles.html', context) 


@login_required
def user_accepted_articles(request):
    accepted = Article.objects.filter(author=request.user).filter(current_status=STAGE_ACCEPTED)
    context = {'accepted': accepted,}
    return render(request, 'articles/accepted_articles.html', context) 


@login_required
def user_pre_publish_articles(request):
    pre_publish = Article.objects.filter(author=request.user).filter(current_status=STAGE_TYPESETTING)
    context = {'pre_publish': pre_publish,}
    return render(request, 'articles/pre_publish_articles.html', context) 


@login_required
def user_rejected_articles(request):
    rejected = Article.objects.filter(author=request.user).filter(current_status=STAGE_REJECTED).order_by('received_date')
    context = {'rejected': rejected,}
    return render(request, 'articles/rejected_articles.html', context)


@login_required
def user_published_articles(request):
    published_articles = Article.objects.filter(author=request.user).filter(current_status=STAGE_PUBLISHED)
    context = {'published_articles': published_articles,}
    return render(request, 'articles/user_published_articles.html', context)


@login_required
def user_recently_edited(request):
    today = datetime.date.today() 
    range = today - datetime.timedelta(7)
    recently_updated = Article.objects.filter(author=request.user).filter(updated_at__gt=range)
    context = {'recently_updated': recently_updated,}
    return render(request, 'articles/recently_updated.html', context)


@login_required
@user_passes_test(is_reviewer)
def reviewer_invites(request):
    invites = ReviewDetailes.objects.filter(reviewer_id=request.user).filter(invited=True).filter(review_start_on__isnull=True)
    context = {'invites': invites,}
    return render(request, 'articles/reviewer_invites.html', context) 


@login_required
@user_passes_test(is_reviewer)
def reviewer_under_review(request):
    under_review = ReviewDetailes.objects.filter(reviewer_id=request.user).filter(review_start_on__isnull=False).filter(done_review=False) #.values_list('article_id')
    # under_review = Article.objects.filter(id__in=reviews)
    context = {'under_review': under_review,}
    return render(request, 'articles/reviewer_under_review.html', context) 


@login_required
@user_passes_test(is_reviewer)
def reviewer_done_review(request):
    done_review = ReviewDetailes.objects.filter(reviewer_id=request.user).filter(done_review=True)
    context = {'done_review': done_review,}
    return render(request, 'articles/reviewer_done_review.html', context)


@login_required
@user_passes_test(is_reviewer)
def reviewer_recently_edited(request):
    today = datetime.date.today() 
    range = today - datetime.timedelta(7)
    updated_last_week = ReviewDetailes.objects.filter(reviewer_id=request.user).filter(last_update__gt=range)
    context = {'recently_updated': updated_last_week,}
    return render(request, 'articles/reviewer_recently_updated.html', context)


@login_required
@user_passes_test(is_editor)
def articles_filtered_list(request, page=1):
    filtered_Articles = ArticlesFilter(request.GET, queryset=Article.objects.all())
    result_counts = filtered_Articles.qs.count()
    # return render(request, 'profiles/profile_filter.html', {'filter': f, 'result_counts': result_counts})      
    
    paginator = Paginator(filtered_Articles.qs, per_page=10)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=2)
    context = {
               'filter': filtered_Articles.form, 
               'object_list': page_object,
               'result_counts': result_counts,
               'filter_items': filtered_Articles.data.items,}
    return render(request, 'articles/filter_articles.html', context)


# class SearchArticlesList(ListView):
#     model = Article
#     context_object_name = "articles"
#     template_name = "articles/search_article_result.html"
#     def get_queryset(self, page=1):
#         language = 'arabic'
#         query = self.request.GET.get("query")
        
#         search_query = SearchQuery(query, config=language)
#         search_vector = SearchVector("title", "en_title", "abstract", "key_words", "en_abstract", 
#                                      "en_keyword", "author__username", config=language)
#         result = Article.objects.annotate(
#             # tags_names=ArrayAgg("author__username", distinct=True),
#             search= search_vector, 
#             rank=SearchRank(search_vector, search_query)
#             ).filter(search=search_query).filter(current_status__exact='Published').order_by("-rank")
#         result_counts = result.count()
        
#         paginator = Paginator(result, per_page=10)
#         page_object = paginator.get_page(page)
#         page_object.adjusted_elided_pages = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=2)
#         return (result)

def search_articles(request, page):
    query = request.GET.get('query')
    results = Article.objects.filter(Q(title__icontains=query) | Q(en_title__icontains=query) |
                                    Q(abstract__icontains=query) | Q(en_abstract__icontains=query) |
                                    Q(key_words__icontains=query) |Q(en_keyword__icontains=query) |
                                    Q(author__username__icontains=query)).filter(current_status__exact='Published').distinct()
    paginator = Paginator(results, per_page=10)    
    try:
        page_object = paginator.page(page)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=2)

    except PageNotAnInteger:
        page_object = paginator.page(1)

    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)

    context = {'results': results, 
               'object_list': page_object,
               'query': query,
               }
    return render(request, 'articles/search_article_result.html', context)


@login_required
@user_passes_test(is_editor)
def article_review(request, article_id):
    article = Article.objects.get(id=article_id)
    review = ReviewDetailes.objects.filter(article_id=article_id)
    authors = Author_Order.objects.filter(article_id=article_id)
    ids, order_form = [], []
    number_of_reviews = []
    score = []
    if review:
        for rev in review:
            ids.append(rev.reviewer_id)
            number_of_reviews.append(ReviewDetailes.objects.filter(reviewer_id = rev.reviewer_id).count())
            current_review = ReviewDetailes.objects.get(article_id = article_id, reviewer_id = rev.reviewer_id)
            if current_review.score:
                score.append(current_review.score)
    if len(score)> 0:
        article.score = sum(score)/len(score)
        article.save()
    review_list = zip(ids,number_of_reviews)
    unique_review_list = set(review_list)
    review_list = list(unique_review_list)
    today = datetime.date.today()
    settings.MEDIA_ROOT = (settings.BASE_DIR / 'Journal/media/documents/{}'.format(article_id))

    if request.method == 'POST':
        decision_form = ArticleForm(request.POST, request.FILES, instance=article)
        if decision_form.is_valid():
            decision_form.save()
            messages.success(request, 'Updated!')
            new_article = Article.objects.get(id=article_id)
            named_formsets = AuthorOrderFormSet(request.POST or None, request.FILES or None, instance=new_article, prefix='ordered_authors')
            for form in named_formsets:
                form.fields['author_id'].disabled = True
            if all((x.is_valid() for x in named_formsets)):
                for formset in named_formsets:
                    formset.save()
        else:
            messages.warning(request, 'Ordered Authors form is incorrect!')
        return redirect(request.META.get('HTTP_REFERER'))
    else: 
        decision_form = ArticleForm(instance=article)
        named_formsets = AuthorOrderFormSet(instance=article, prefix='ordered_authors')
        for form in named_formsets:
            form.fields['author_id'].disabled = True
    settings.MEDIA_ROOT = (settings.BASE_DIR / 'Journal/media')
    max_volume = Article.objects.aggregate(Max('volume'))['volume__max']
    volume = range(1, max_volume + 1)
    max_issue, year = [], []
    ye = 2014
    for vol in volume:
        year.append(ye)
        max_issue.append(range(1, Article.objects.filter(volume=vol).aggregate(Max('issue'))['issue__max'] +1))
        ye +=1
    issue = zip(year, volume, max_issue)
    context = {'article': article, 
               'review': review, 
               'review_count' : review.count(),
               'rr': review_list, 
               'today': today,
               'decision_form': decision_form,
               'volume': volume,
               'issue': issue,
               'order_form': order_form,
               'authors': authors,
               'named_formsets': named_formsets,}

    return render(request, 'articles/article_review.html', context)


@login_required
@user_passes_test(is_editor)
def send_email(request, author_id, article_id):
    article = Article.objects.get(id=article_id)
    review = ReviewDetailes.objects.filter(article_id=article_id)
    actor = request.user
    authors = Article.objects.filter(id=article_id).values_list('author')
    author_ids = [x[0] for x in authors]
    recipient_authors = User.objects.filter(id__in = author_ids)
    # recipient_emails = [x.email for x in recipient_authors]
    if request.method == 'POST':
        
        subject = request.POST.get("subject")  
        email_from = settings.EMAIL_HOST_USER  
        recipient_list = [request.POST.get("email"), ]  
        message_mail = request.POST.get("message") 
        attachment = request.POST.get("attach")
        email_author = EmailMessage(subject, message_mail, email_from, recipient_list)
        
        if (attachment):
            try:
                attached_file = (settings.BASE_DIR / 'Journal/media/documents/{}/{}'.format(article_id, attachment))
                email_author.attach_file(attached_file)
                email_author.send()
                messages.success(request, 'E.mail sent')
                notify.send(actor, recipient=recipient_authors, 
                    verb='A replay from editor has been sent to you by email', target=article)
                return redirect('article-review', article_id=article_id)
            except FileNotFoundError:
                messages.warning(request, 'No such file or directory')
        else:
            email_author.send()
            messages.success(request, 'E.mail sent')
            notify.send(actor, recipient=recipient_authors, 
                verb='A replay from editor has been sent to you by email', target=article)
            return redirect('article-review', article_id=article_id)
    author = User.objects.get(id=author_id)
    context = {
        'author': author,
        'site': get_current_site(request),
        'article': article,
        'review': review,
        # 'recipient_emails': recipient_emails,
    }
    return render(request, 'articles/email_author.html', context)


@login_required
@user_passes_test(is_editor)
def filter_reviewers(request, article_id, page):
    filtered_profiles = ProfilesFilter(request.GET, queryset=Profiles.objects.all())

    result_counts = filtered_profiles.qs.count()
    paginator = Paginator(filtered_profiles.qs, per_page=10)

    details = ReviewDetailes.objects.all()
    
    review = ReviewDetailes.objects.filter(article_id=article_id)

    try:
        page_object = paginator.page(page)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=2)

    except PageNotAnInteger:
        page_object = paginator.page(1)

    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)

    r_list = [rev.reviewer_id for rev in review]
    ids = []
    number_of_reviews = []
    number_of_invitations = []
    number_of_done_reviews = []
    for rev in page_object:
        ids.append(rev.id)
        number_of_reviews.append(ReviewDetailes.objects.filter(reviewer_id = rev.id, replay__isnull=True).count())
        number_of_done_reviews.append(ReviewDetailes.objects.filter(reviewer_id = rev.id, replay__isnull=False).count())
        number_of_invitations.append(ReviewDetailes.objects.filter(reviewer_id = rev.id, invited=True).count())
    review_list = zip(ids, number_of_reviews, number_of_invitations, number_of_done_reviews)
    unique_review_list = set(review_list)
    review_list = list(unique_review_list)

    context = { 'article_id': article_id,
                'filter': filtered_profiles.form, 
                'object_list': page_object,
                'result_counts': result_counts,
                'filter_items': filtered_profiles.data.items,
                # 'details': rev_id,
                'rr': r_list,
                'review_list': review_list}
    return render(request, 'articles/filter_reviewers.html', context)


@login_required
@user_passes_test(is_editor)
def add_to_reviewer_list(request, rev_id, article_id):
    article = Article.objects.get(id=article_id)
    reviewer = User.objects.get(id=rev_id)
    #order = request.GET.get('order')
    review = ReviewDetailes.objects.create(article_id= article, reviewer_id= reviewer) #, order=order)
    review.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(is_editor)
def remove_from_reviewer_list(request, rev_id, article_id):
    review = ReviewDetailes.objects.filter(article_id=article_id, reviewer_id=rev_id)    
    review.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(is_editor)
def invite_reviewer(request, rev_id, article_id):
    review = ReviewDetailes.objects.get(article_id=article_id, reviewer_id=rev_id)
    review.invited = True
    # review.replay = 'ACCEPT'
    today = datetime.date.today() 
    review.invited_at = today
    review.invitation_expire_on = today + datetime.timedelta(7)
    review.save()   
    return redirect(request.META.get('HTTP_REFERER'))


# @login_required
# @user_passes_test(is_editor)
# def delete_ordered_author(request, pk):
#     try:
#         author = Author_Order.objects.get(id=pk)
#     except author.DoesNotExist:
#         messages.success(
#             request, 'author Does not exit'
#             )
#         return redirect('update_product', pk=author.article.id)

#     author.delete()
#     messages.success(
#             request, 'author deleted successfully'
#             )
#     return redirect('update_product', pk=author.product.id)
