from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
import datetime
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UpdateUserForm, UpdateProfileForm, CreateUserForm
from .models import Profiles, ProfilesFilter
from articles.models import Article, Reviewer_publication
from articles.forms import ReviewerpublicationForm
from reviews.models import ReviewDetailes
from django.db.models import Q
from django.urls import reverse
from notifications.signals import notify

# ----DECORATOR
def is_author(user):
    if user.profiles.user_type == "AUTHOR":
        return True
    return False

def is_editor(user):
    if user.profiles.user_type == "EDITOR":
        return True
    return False

def is_reviewer(user):
    if user.profiles.user_type == "REVIEWER":
        return True
    return False

def is_editor_or_reviewer(user):
    if user.profiles.user_type == "EDITOR" or user.profiles.user_type == "REVIEWER":
        return True
    return False

def is_publisher(user):
    if user.profiles.user_type == "PUBLISHER":
        return True
    return False

# Where to go after successful sign in
@login_required
def where_next(request):    
    if request.user.is_anonymous:
        return HttpResponse(reverse('account_login'))
    elif request.user.profiles.user_type == "AUTHOR":
        return HttpResponseRedirect(reverse('author-dashboard'))
    elif request.user.profiles.user_type == "EDITOR":
        return HttpResponseRedirect(reverse('editor-dashboard'))
    elif request.user.profiles.user_type == "REVIEWER":
        return HttpResponseRedirect(reverse('reviewer-dashboard'))
    elif request.user.profiles.user_type == "PUBLISHER":
        return HttpResponseRedirect(reverse('editor-dashboard'))


@login_required
@user_passes_test(is_author, login_url='account_login')
def author_dashboard(request):
    today = datetime.date.today() 
    range = today - datetime.timedelta(7)
    user_articles_unsubmitted = Article.objects.filter(author=request.user).filter(current_status='Unsubmitted').count()
    user_articles_pre_review = Article.objects.filter(author=request.user).filter(current_status='Pre Review').count()
    user_articles_under_review = Article.objects.filter(author=request.user).filter(current_status='Under Review').count()
    user_articles_accepted = Article.objects.filter(author=request.user).filter(current_status='Accepted').count()
    user_articles_rejected = Article.objects.filter(author=request.user).filter(current_status='Rejected').count()
    user_articles_pre_publish = Article.objects.filter(author=request.user).filter(current_status='Typesetting').count()
    user_articles_published = Article.objects.filter(author=request.user).filter(current_status='Published').count()
    user_updated_last_week = Article.objects.filter(author=request.user).filter(updated_at__gt=range).count()

    context = {
        'user_articles_unsubmitted': user_articles_unsubmitted,
        'user_articles_pre_review': user_articles_pre_review,
        'user_articles_under_review': user_articles_under_review,
        'user_articles_accepted': user_articles_accepted,
        'user_articles_rejected': user_articles_rejected,
        'user_articles_pre_publish': user_articles_pre_publish,
        'user_articles_published': user_articles_published,
        'user_updated_last_week': user_updated_last_week,
    }
    return render(request, 'profiles/author_dashboard.html', context)


@login_required
@user_passes_test(is_editor or is_publisher, login_url='account_login')
def editor_dashboard(request):
    articles_unsubmitted = Article.objects.filter(current_status='Unsubmitted').count()
    articles_pre_review = Article.objects.filter(current_status='Pre Review').count()
    articles_under_review = Article.objects.filter(current_status='Under Review').count()
    articles_accepted = Article.objects.filter(current_status='Accepted').count()
    articles_rejected = Article.objects.filter(current_status='Rejected').count()
    articles_pre_publish = Article.objects.filter(current_status='Typesetting').count()
    articles_published = Article.objects.filter(current_status='Published').count()
    today = datetime.date.today() 
    range = today - datetime.timedelta(7)
    updated_last_week = Article.objects.filter(updated_at__gt=range).count()

    user_articles_unsubmitted = Article.objects.filter(author=request.user).filter(current_status='Unsubmitted').count()
    user_articles_pre_review = Article.objects.filter(author=request.user).filter(current_status='Pre Review').count()
    user_articles_under_review = Article.objects.filter(author=request.user).filter(current_status='Under Review').count()
    user_articles_accepted = Article.objects.filter(author=request.user).filter(current_status='Accepted').count()
    user_articles_rejected = Article.objects.filter(author=request.user).filter(current_status='Rejected').count()
    user_articles_pre_publish = Article.objects.filter(author=request.user).filter(current_status='Typesetting').count()
    user_articles_published = Article.objects.filter(author=request.user).filter(current_status='Published').count()
    user_updated_last_week = Article.objects.filter(author=request.user).filter(updated_at__gt=range).count()

    context = {
        'articles_unsubmitted': articles_unsubmitted,
        'articles_pre_review': articles_pre_review,
        'articles_under_review': articles_under_review,
        'articles_accepted': articles_accepted,
        'articles_rejected': articles_rejected,
        'articles_pre_publish': articles_pre_publish,
        'articles_published': articles_published,
        'updated_last_week': updated_last_week,
        'user_articles_unsubmitted': user_articles_unsubmitted,
        'user_articles_pre_review': user_articles_pre_review,
        'user_articles_under_review': user_articles_under_review,
        'user_articles_accepted': user_articles_accepted,
        'user_articles_rejected': user_articles_rejected,
        'user_articles_pre_publish': user_articles_pre_publish,
        'user_articles_published': user_articles_published,
        'user_updated_last_week': user_updated_last_week,
    }
    return render(request, 'profiles/editor_dashboard.html', context)


@login_required
@user_passes_test(is_reviewer)
def reviewer_dashboard(request):
    invites = ReviewDetailes.objects.filter(reviewer_id=request.user).filter(invited=True).filter(review_start_on__isnull=True).count()
    under_review = ReviewDetailes.objects.filter(reviewer_id=request.user).filter(review_start_on__isnull=False).filter(done_review=False).count()
    done_review = ReviewDetailes.objects.filter(reviewer_id=request.user).filter(done_review=True).count()
    today = datetime.date.today() 
    range = today - datetime.timedelta(7)
    updated_last_week = ReviewDetailes.objects.filter(reviewer_id=request.user).filter(last_update__gt=range).count()

    user_articles_unsubmitted = Article.objects.filter(author=request.user).filter(current_status='Unsubmitted').count()
    user_articles_pre_review = Article.objects.filter(author=request.user).filter(current_status='Pre Review').count()
    user_articles_under_review = Article.objects.filter(author=request.user).filter(current_status='Under Review').count()
    user_articles_accepted = Article.objects.filter(author=request.user).filter(current_status='Accepted').count()
    user_articles_rejected = Article.objects.filter(author=request.user).filter(current_status='Rejected').count()
    user_articles_pre_publish = Article.objects.filter(author=request.user).filter(current_status='Typesetting').count()
    user_articles_published = Article.objects.filter(author=request.user).filter(current_status='Published').count()
    user_updated_last_week = Article.objects.filter(author=request.user).filter(updated_at__gt=range).count()

    context = {
        'invites': invites,
        'under_review': under_review,
        'done_review': done_review,
        'updated_last_week': updated_last_week,
        'user_articles_unsubmitted': user_articles_unsubmitted,
        'user_articles_pre_review': user_articles_pre_review,
        'user_articles_under_review': user_articles_under_review,
        'user_articles_accepted': user_articles_accepted,
        'user_articles_rejected': user_articles_rejected,
        'user_articles_pre_publish': user_articles_pre_publish,
        'user_articles_published': user_articles_published,
        'user_updated_last_week': user_updated_last_week,
    }
    return render(request, 'profiles/reviewer_dashboard.html', context)


@login_required
def view_profile(request, user_id):
    user_object = get_object_or_404(Profiles, id=user_id)
    publications = Article.objects.filter(author=user_id)
    reviews = Article.objects.filter(reviewer=user_id)
    context = {'user_object': user_object, 
               'publications': publications,
               'reviews': reviews,}
    return render(request, 'profiles/profile_details.html', context)


@login_required
def update_profile(request, user_id):
    user = User.objects.get(id = user_id)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, instance=user.profiles)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'profile is updated successfully')
            return redirect(to='update-user-profile', user_id = user.id)
        else:
            messages.warning(request, "Can't update your profile!")
            return redirect(to='update-user-profile', user_id = user.id)
    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.profiles)
    context = {'user_form': user_form, 
               'profile_form': profile_form}
    return render(request, 'profiles/profile_update.html', context)


@login_required
def creat_profile(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        profile_form = UpdateProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            profile_form = UpdateProfileForm(request.POST, instance=new_user.profiles)
 
            profile_form.save()
            messages.success(request, 'profile is created successfully')
            
            actor = User.objects.get(id=1)               
            recipient_user = User.objects.filter(id=profile_form.id)
            notify.send(actor, recipient=recipient_user, verb='Thank you for creating new account in our journal, please complete your profile information before adding new submission',
                       target=recipient_user.profiles)
            
            context = {'user_form': new_user, 'profile_form': profile_form}
            # return render(request, 'profiles/all_authors.html', context)
            return redirect(to='filter-profiles', page= 1)

        else:
            messages.warning(request, 'data is not valid!')
            print('user_form', user_form.errors)
            print('profile_form', profile_form.errors)
            # return redirect(to='create-user-profile')
            context = {'user_form': user_form, 'profile_form': profile_form}
            return render(request, 'profiles/profile_create.html', context)
    else:
        user_form = CreateUserForm()
        profile_form = UpdateProfileForm()

    return render(request, 'profiles/profile_create.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
@user_passes_test(is_editor)
def delete_profile(request, user_id):
    user = User.objects.get(id = user_id)
    user.delete()
    messages.success(request, 'User {} is deleted'.format(user))
    return redirect(to='filter-profiles', page= 1)


@login_required
@user_passes_test(is_editor)
def search_profiles(request, page):
    query = request.GET.get('queryuser')
    results = Profiles.objects.filter(Q(address__icontains=query) | Q(bio__icontains=query) |
                                    Q(certificate__icontains=query) | Q(country__icontains=query) |
                                    Q(name__icontains=query) |Q(specialist__icontains=query) | 
                                    Q(specific_specialist__icontains=query) | Q(work_address__icontains=query)).distinct()
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
               'queryuser': query,
               }
    return render(request, 'profiles/search_result.html', context)


@login_required
@user_passes_test(is_editor)
def profiles_filtered_list(request, page=1):
    filtered_profiles = ProfilesFilter(request.GET, queryset=Profiles.objects.all())
    result_counts = filtered_profiles.qs.count()
    # return render(request, 'profiles/profile_filter.html', {'filter': f, 'result_counts': result_counts})      
    
    paginator = Paginator(filtered_profiles.qs, per_page=10)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=2)
    context = {
               'filter': filtered_profiles.form, 
               'object_list': page_object,
               'result_counts': result_counts,
               'filter_items': filtered_profiles.data.items,}
    return render(request, 'profiles/profile_filter.html', context)


def publisher_dashboard(request):
    return render (request, 'profiles/publisher_dashboard.html')


@login_required
@user_passes_test(is_editor)
def show_reviewers_table(request, page=1):
    reviewers = Reviewer_publication.objects.all().order_by('user_id')
    paginator = Paginator(reviewers, per_page=10)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=2)
    context = {'object_list': page_object, 'reviewers_count': reviewers.count(),}
    return render(request, 'profiles/show_reviewers_table.html', context)


@login_required
@user_passes_test(is_editor)
def set_reviewer_publications(request,rev_id):
    local_publications = Article.objects.filter(author=rev_id).filter(current_status='Published')
    reviewer = User.objects.get(id=rev_id)
    reviewer.profiles.user_type = 'REVIEWER'
    reviewer.save()
    messages.success(request, 'Reviewer is added successfuly')
    
    actor = User.objects.get(id=1)               
    recipient_user = User.objects.filter(id=rev_id)
    notify.send(actor, recipient=recipient_user, verb='You have been assigned as a reviewer in this journal')
    
    for pub in local_publications:
        abstract = str(pub.title) + ', ' + str(pub.abstract)
        reviewer_publication = Reviewer_publication.objects.get_or_create(
            user_id=reviewer, abstract=abstract)
        reviewer_publication[0].save()
        reviewer_publication[0].scope.set(pub.scope.all())
    all_reviewer_publications = Reviewer_publication.objects.filter(user_id=reviewer)    
    context = {'all_reviewer_publications': all_reviewer_publications}
    return render(request, 'profiles/set_reviewer_publications.html', context)


@login_required
@user_passes_test(is_editor)
def add_reviewer_publications(request):
    if request.method == "POST":
        form = ReviewerpublicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Reviewer's publication is added successfuly")
        else:
            messages.warning(request, "Can't add now! form is not valid.")
    else:
        form = ReviewerpublicationForm()
    context = {'form': form}
    return render(request, 'profiles/add_reviewer_publications.html', context)


@login_required
@user_passes_test(is_editor)
def update_reviewer_publications(request, id):
    reviewer_pub = Reviewer_publication.objects.get(id=id)
    if request.method == "POST":
        form = ReviewerpublicationForm(request.POST, instance=reviewer_pub)
        if form.is_valid():
            form.save()
            messages.success(request, "Reviewer's publication is saved successfuly")
        else:
            messages.warning(request, "Can't save now! form is not valid.")
    else:
        form = ReviewerpublicationForm(instance=reviewer_pub)
    context = {'form': form}
    return render(request, 'profiles/add_reviewer_publications.html', context)

@login_required
@user_passes_test(is_editor)
def delete_reviewer_publications(request, id):
    reviewer = Reviewer_publication.objects.get(id=id)
    reviewer.delete()
    messages.success(request, 'Reviewer publications is deleted')
    return redirect(to='filter-profiles', page=1)


@login_required
@user_passes_test(is_editor)
def search_publications(request, page=1):
    query = request.GET.get('querypub')
    results = Reviewer_publication.objects.filter(Q(user_id__username__icontains=query) | Q(abstract__icontains=query) | 
                                                  Q(scope__scope__icontains=query)).distinct()
    paginator = Paginator(results, per_page=10)    
    try:
        page_object = paginator.page(page)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=2)

    except PageNotAnInteger:
        page_object = paginator.page(1)

    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)

    context = {'reviewers_count': results.count(), 
               'object_list': page_object,
               'querypub': query,
               }
    return render(request, 'profiles/show_reviewers_table.html', context)
