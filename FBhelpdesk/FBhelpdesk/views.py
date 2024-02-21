from django.shortcuts import render, redirect, get_object_or_404
from .models import FacebookPage, Conversation, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .decorators import custom_login_required
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_protect
import facebook
import requests
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings
from urllib.parse import urlencode


def home(request):
    return redirect('fb_page_connections')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('fb_page_connections')  # Redirect to desired page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
@csrf_protect
def fb_page_connections(request):
    user = request.user
    fb_pages = FacebookPage.objects.filter(user=user)
    return render(request, 'fbpageconnections.html', {'fb_pages': fb_pages})

@login_required
@csrf_protect
def delete_fb_page(request, fb_page_id):
    fb_page = get_object_or_404(FacebookPage, id=fb_page_id)
    if request.method == 'POST':
        fb_page.delete()
        return redirect('fb_page_connections')
    return render(request, 'templates/confirm_delete_fb_page.html', {'fb_page': fb_page})


@login_required
def view_conversations(request):
    user = request.user
    conversations = Conversation.objects.filter(user=user)
    return render(request, 'templates/conversations.html', {'conversations': conversations})

# Example view for replying to messages in a conversation
@login_required
def reply_to_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.method == 'POST':
        message_content = request.POST.get('message_content')
        if message_content:
            Message.objects.create(conversation=conversation, sender_id=request.user.id, message=message_content)
            # Redirect to the same conversation page after replying
            return redirect('templates/reply_to_message', conversation_id=conversation_id)
    return render(request, 'templates/reply_to_message.html', {'conversation': conversation})

@login_required
def create_facebook_page(request):
    if request.method == 'POST':
        # Assuming you have a form to capture the necessary data
        user = request.user
        page_id = request.POST.get('page_id')
        access_token = request.POST.get('access_token')
        
        # Create a new FacebookPage object
        facebook_page = FacebookPage.objects.create(
            user=user,
            page_id=page_id,
            access_token=access_token
        )
        
        return redirect('fb_page_connections')  # Redirect to the page where all FacebookPage connections are displayed
    else:
        # Render a form for the user to input the data
        return render(request, 'create_facebook_page.html')
    
@login_required
def manage_fb_page_connections(request):
    user = request.user
    fb_pages = FacebookPage.objects.filter(user=user)
    return render(request, 'manage_fb_page_connections.html', {'fb_pages': fb_pages})

@login_required
def manage_fb_page_connections(request):
    user = request.user
    fb_pages = FacebookPage.objects.filter(user=user)

    if request.method == 'POST':
        if 'create_connection' in request.POST:
            # Redirect to Facebook login page for authentication
            return redirect(f'https://www.facebook.com/v12.0/dialog/oauth?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={settings.FACEBOOK_REDIRECT_URL}&scope=pages_manage_engagement,pages_manage_metadata,pages_read_engagement')

        elif 'delete_connection' in request.POST:
            connection_id = request.POST.get('connection_id')
            FacebookPage.objects.filter(id=connection_id).delete()
            return redirect('manage_fb_page_connections')

    return render(request, 'manage_fb_page_connections.html', {'fb_pages': fb_pages})  

def fb_login(request):
    # Redirect users to Facebook for login
    redirect_uri = request.build_absolute_uri('/fb-callback/')
    login_url = 'https://www.facebook.com/v12.0/dialog/oauth'
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': redirect_uri,
        'scope': 'pages_manage_metadata', 
    }
    return redirect(f'{login_url}?{urlencode(params)}')

def fb_callback(request):
    code = request.GET.get('code')
    if code:
        redirect_uri = request.build_absolute_uri(reverse('fb_callback'))
        oauth_args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': code,
        }
        oauth_response = requests.get('https://graph.facebook.com/v12.0/oauth/access_token', params=oauth_args)
        oauth_data = oauth_response.json()
        access_token = oauth_data.get('access_token')
        
        if access_token:
            graph = facebook.GraphAPI(access_token)
            pages_data = graph.get_object('me/accounts')

            return redirect('fb_page_connections')

    return redirect('error_page')