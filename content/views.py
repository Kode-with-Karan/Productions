from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Content
from .forms import ContentUploadForm,CollaborateUploadForm
from django.db.models import Q
from django.contrib import messages
from blog.models import Blog
from django.core.mail import send_mail

def browse_content(request):
    query = request.GET.get("q", "")
    content_type = request.GET.get("content_type", "")
    sort_by = request.GET.get("sort_by", "latest")

    contents = Content.objects.all()

    if query:
        contents = contents.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if content_type:
        contents = contents.filter(content_type=content_type)

    if sort_by == "popular":
        contents = contents.order_by("-views")
    elif sort_by == "latest":
        contents = contents.order_by("-uploaded_at")

    return render(request, "content/browse.html", {"contents": contents})


def home(request):
    contents = Content.objects.all()
    blogs = Blog.objects.filter(status='published').order_by('-created_at')[:4]
    return render(request, 'content/home.html', {'contents': contents, 'blogs': blogs})

def category(request, content_type):
    contents = Content.objects.filter(content_type=content_type).order_by('-uploaded_at')
    return render(request, 'content/category.html', {'contents': contents, 'content_type': content_type})

@login_required
def upload_content(request):

    if request.method == 'POST':

        form = ContentUploadForm(request.POST, request.FILES)
        # image_form = ContentImageForm(request.POST, request.FILES)

        # images = request.FILES.getlist('image')  # Get multiple uploaded images

            # Save each image separately
            
        if form.is_valid():
            content = form.save(commit=False)
            content.uploaded_by = request.user.profile
            content.save()
            # for img in images:
                # ContentImageForm.objects.create(content=content, image=img)
            return redirect('home')
    else:
        form = ContentUploadForm()
        # image_form = ContentImageForm()
    return render(request, 'content/upload_content.html', {'form': form})

def content_detail(request, pk):
    content = get_object_or_404(Content, pk=pk)
    content.views += 1
    content.earnings += 1
    content.save()
    return render(request, 'content/content_detail.html', {'content': content})
def content_display(request, pk):
    content = get_object_or_404(Content, pk=pk)
    return render(request, 'content/content_display.html', {'content': content})

@login_required
def collaborate(request):
    if request.method == 'POST':
        form = CollaborateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.user = request.user
            content.save()

            # Prepare email content
            subject = "New Collaboration Submission"
            recipient_email = "karanost12@gmail.com"  # Change to the actual recipient's email
            sender_email = request.user.email  # Sender is the logged-in user's email
            message = f"""
            A new collaboration request has been submitted.

            User: {request.user.get_full_name()} ({request.user.email})
            
            Submission Details:
            ----------------------------
            """
            for field, value in form.cleaned_data.items():
                message += f"{field}: {value}\n"

            # Send the email
            send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)


            return redirect('home')
    else:
        form = CollaborateUploadForm()
    return render(request, 'content/collaborate.html', {'form': form})


@login_required
def edit_content(request, pk):
    content = get_object_or_404(Content, pk=pk)

    # Ensure only the owner can edit
    if str(content.uploaded_by) != str(request.user):

        messages.error(request, "You do not have permission to edit this content.")
        return redirect('dashboard')

    if request.method == "POST":
        content.title = request.POST.get("title")
        content.description = request.POST.get("description")
        content.save()
        messages.success(request, "Content updated successfully!")
        return redirect('dashboard')

    return render(request, "content/edit_content.html", {"content": content})


@login_required
def delete_content(request, pk):
    content = get_object_or_404(Content, pk=pk)

    # Ensure only the owner can delete their content
    if str(content.uploaded_by) != str(request.user):
        messages.error(request, "You do not have permission to delete this content.")
        return redirect('dashboard')  # Redirect to dashboard

    if request.method == "POST":
        content.delete()
        messages.success(request, "Content deleted successfully!")
        return redirect('dashboard')  # Redirect after deletion

    return render(request, "content/delete_confirm.html", {"content": content})
