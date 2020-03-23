from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ResumeForm, ResumeItemForm
from .models import Resume, ResumeItem


@login_required
def resume_list_view(request):
    """
    Handle a request to view a user's resumes.
    """
    resumes = Resume.objects.filter(user=request.user)

    return render(request, 'resume/resumes.html', {
        'resumes': resumes
    })


@login_required
def resume_view(request, resume_id):
    """
    Handle a request to view a resume.
    """
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404

    resume_items = ResumeItem.objects\
        .filter(resume=resume)\
        .order_by('-start_date')

    return render(request, 'resume/resume.html', {
        'resume': resume,
        'resume_items': resume_items
    })


@login_required
def resume_create_view(request):
    """
    Handle a request to create a new resume.
    """
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            new_resume = form.save(commit=False)
            new_resume.user = request.user
            new_resume.save()

            return redirect(resume_view, new_resume.id)
    else:
        form = ResumeForm()

    return render(request, 'resume/resume_create.html', {
        'form': form
    })


@login_required
def resume_rename_view(request, resume_id):
    """
    Handle a request to rename a resume.

    :param resume_id: The database ID of the Resume to rename.
    """
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404

    template_dict = {
        'resume': resume
    }

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            form = ResumeForm(instance=resume)
            template_dict['message'] = 'Resume updated'
    else:
        form = ResumeForm(instance=resume)

    template_dict['form'] = form

    return render(request, 'resume/resume_rename.html', template_dict)


@login_required
def resume_item_create_view(request, resume_id):
    """
    Handle a request to create a new resume item.
    """
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = ResumeItemForm(request.POST)
        if form.is_valid():
            new_resume_item = form.save(commit=False)
            new_resume_item.resume = resume
            new_resume_item.save()

            return redirect(
                resume_item_edit_view,
                resume_id,
                new_resume_item.id
            )
    else:
        form = ResumeItemForm()

    return render(request, 'resume/resume_item_create.html', {
        'resume': resume,
        'form': form
    })


@login_required
def resume_item_edit_view(request, resume_id, resume_item_id):
    """
    Handle a request to edit a resume item.

    :param resume_item_id: The database ID of the ResumeItem to edit.
    """
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404
    try:
        resume_item = ResumeItem.objects\
            .filter(resume=resume)\
            .get(id=resume_item_id)
    except ResumeItem.DoesNotExist:
        raise Http404

    template_dict = {
        'resume': resume
    }

    if request.method == 'POST':
        if 'delete' in request.POST:
            resume_item.delete()
            return redirect(resume_view, resume_id)

        form = ResumeItemForm(request.POST, instance=resume_item)
        if form.is_valid():
            form.save()
            form = ResumeItemForm(instance=resume_item)
            template_dict['message'] = 'Resume item updated'
    else:
        form = ResumeItemForm(instance=resume_item)

    template_dict['form'] = form

    return render(request, 'resume/resume_item_edit.html', template_dict)
