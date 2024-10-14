from django.shortcuts import render, redirect
from post.models import Article as Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from users.forms import UserRegistrationForm  # Import the custom form
from users.forms import UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from django.contrib.auth.models import User
# def home(request):
#     # Example data to be passed to the template
#     context = {
#         'posts': Post.objects.all(), 
#     }
#     return render(request, 'home.html', context)

def post_list_view(request):
    # Fetch all posts from the database
    posts = Post.objects.all()

    # Set up pagination
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the posts for the current page

    # Context data to be passed to the template
    context = {
        'posts': page_obj,
    }

    # Render the 'home.html' template with the context
    return render(request, 'home.html', context)

def post_details(request, id):
    # Fetch the post by its ID
    post = get_object_or_404(Post, id=id)
    
    # Render the post detail page with the fetched post
    return render(request, 'post_detail.html', {'post': post})

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    # messages.info(request, 'You have bee')
    return render(request, 'logout_message.html')

def logout_message(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            # Ensure at least one field is filled
            if (u_form.cleaned_data['username'] or
                u_form.cleaned_data['email'] or
                p_form.cleaned_data['image']):
                
                # Save changes if valid and fields are filled
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile')
            else:
                # If no field is filled, show an error message
                messages.error(request, 'You must fill at least one field to update your profile.')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'edit_profile.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        # Create and save the new post
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        post.save()

        # Redirect to home after successful post creation
        return redirect('home')

    return render(request, 'post_form.html')

@login_required
def update_post(request, id):
    post = get_object_or_404(Post, id=id)

    # Ensure the current user is the author of the post
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        # Update the post details
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()

        # Redirect to the post detail page, passing the `id` to resolve the correct post URL
        return redirect('post_detail', id=post.id)

    return render(request, 'post_update_form.html', {'post': post})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    # Ensure the current user is the author of the post
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()  # Delete the post
        return redirect('home')  # Redirect to home or another appropriate page

    return render(request, 'post_delete.html', {'post': post})

def author_posts_view(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author).order_by('-date')
    
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'posts': posts_page,
        'author': author,
    }
    
    return render(request, 'author_posts.html', context)



class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'  # Your password reset form

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'  # Your password reset done page

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'  # Your password reset confirmation page

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'  # Your password reset complete page
