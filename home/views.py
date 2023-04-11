from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.forms import modelformset_factory, inlineformset_factory, modelform_factory
from django.contrib.auth.decorators import login_required
from . import models, forms
import random
import smtplib


# Create your views here
def find(search_value):
    genres = [genres[1] for genres in models.BaseMedia.MEDIA_GENRES]
    if search_value in genres:
        playlist_obj = models.VideoPlayList.objects.first()
        print(search_value, playlist_obj.genre, playlist_obj.media_type == 'A', search_value in str(playlist_obj.genre))
        anime = [playlist for playlist in models.VideoPlayList.objects.filter(media_type = 'A') if (search_value in str(playlist.genre))]
        web_series = [playlist for playlist in models.VideoPlayList.objects.filter(media_type = 'W') if (search_value in str(playlist.genre))]
        single_medias = [single_media for single_media in models.SingleMedia.objects.all() if search_value in str(single_media.genre)]
        print(anime, web_series, single_medias)
           
    else:
        play_lists = models.VideoPlayList.objects.filter(name__icontains = search_value)
        single_medias = models.SingleMedia.objects.filter(name__icontains = search_value)
        anime = play_lists.filter(media_type = 'A')
        web_series = play_lists.filter(media_type = 'W')
    
    return single_medias, web_series, anime


def media_pages(request, media_type):
    context = None
    # need to include search bar
    if request.method == 'GET':
        for value, name in models.BaseMedia.MEDIA_TYPES:
            if (name == media_type) and (value in ('A', 'W')):
                medias = models.VideoPlayList.objects.filter(media_type = value)
                break

            else:
                medias = models.SingleMedia.objects.all()

        context = {
            'medias': medias,
            'media_type': media_type,
        }

    return render(request, 'home/media_pages.html', context)


def home_page(request):
    context = None 
    media_types = models.BaseMedia.MEDIA_TYPES
    genres = models.BaseMedia.MEDIA_GENRES

    if request.method == 'POST':
        form = forms.SearchForm(request.POST)

        if form.is_valid():
            search_value = form.cleaned_data.get('query')
            return redirect('search', search_value = search_value)

        else:
            form = forms.SearchForm(request.POST)
            genres = models.BaseMedia.MEDIA_GENRES

            context = {
                'search_form': form,
                'genres': genres,
                'media_types': media_types,
            }

    elif request.method == 'GET':
        form = forms.SearchForm()

        context = {
            'search_form': form,
            'genres': genres,
            'media_types': media_types
        }

    return render(request, 'home/home_page.html', context)

def search(request, search_value):
    contexxt = None 

    if request.method == 'POST':
        form = forms.SearchForm(request.POST)

        if form.is_valid():
            search_value = form.cleaned_data.get('query')
            form = forms.SearchForm()

            return redirect('search', search_value = search_value)

        else:
            form = forms.SearchForm(requst.POST)
            genres = models.BaseMedia.MEDIA_GENRES

            context = {
                'search_form': form,
                'genres': [genre[1] for genre in genres],
            }

    elif request.method == 'GET':
        form = forms.SearchForm()
        genres = models.BaseMedia.MEDIA_GENRES
        movies, web_series, anime = find(search_value)
        
        context = {
            'search_value': search_value,
            'search_form': form,
            'genres': [genre[1] for genre in genres],
            'moveis': movies,
            'web_series': web_series,
            'animes': anime,
        }

    return render(request, 'home/search.html', context)



# <------------------ show search results ------------------>

def open_playlist(request, search_value, uuid):
    if request.method == 'GET':
        playlist = models.VideoPlayList.objects.get(uuid = uuid)
        multi_medias = playlist.multimedia_set.all()
      
        context = {
            'playlist': playlist,
            'multi_medias': multi_medias,
        }

    return render(request, 'home/open_playlist.html', context)


def open_media(request, search_value, season_name, season_uuid):
    if request.method == 'GET':
        multi_media = models.MultiMedia.objects.get(uuid = season_uuid)
        medias = multi_media.media_set.all()

        print(medias)

        context = {
            'medias': medias,
        }

    return render(request, 'home/open_media.html', context) 


def open_video(request, search_value, season_name, season_uuid, video_uuid):
    if request.method == 'GET':
        video = models.Media.objects.get(uuid = video_uuid)
        print(video)

        context = {
            'video': video,
            'other_episodes': models.MultiMedia.objects.get(uuid = season_uuid).media_set.all()
        }
    
    return render(request, 'home/open_video.html', context)


# <--------------- User login, logout, authentication ---------------->

def logout_user(request):
    logout(request)
    return redirect('home_page')


def login_user(request):
    context = None

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)
            print(user)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfull!')
                return redirect('home_page')


        else:
            print('form is not valid')
            context = {
                'login_form': form,
            }

    if request.method == 'GET':
        form = forms.LoginForm()

        context = {
            'login_form': form,
        }

    return render(request, 'home/login.html', context)


def signup(request):
    context = None

    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            new_user = models.CustomUser.objects.create(
                username = cleaned_data['username'],
                first_name = cleaned_data['first_name'],
                last_name = cleaned_data['last_name'],
                email = cleaned_data['email'],
            )
            
            password = cleaned_data['password']
            new_user.set_password(password)
            new_user.save()
            messages.success(request, 'Account created successfully, please Login !')
            return redirect('login_user')

        else:
            context = {
                'signup_form': form,
                'signup_form_errors': form.errors,
            }

    elif request.method == 'GET':
        form = forms.SignupForm()

        context = {
            'signup_form': form,
        }

    return render(request, 'home/signup.html', context)


def send_otp(request, username = None):
    if request.user.is_authenticated:
        user_email = request.user.email

    else:
        user = models.CustomUser.objects.get(username = username)
        user_email = user.email

    otp = random.randint(100000, 9999999)

    try:
        send_mail(
            from_email = 'shuklapiyush993@gmail.com',
            auth_password = 'Indi@nPost',
            subject = 'OTP for password change',
            message =  f'Your OTP is {otp}',
            recipient_list = [user_email],
            fail_silently = False,
        )

    except smtplib.SMTPException as e:
        print('There is problem in sending mail', e)
        messages.error(request, 'There is a problem in sending OTP!')
        return redirect('home_page')

    else:
        messages.success(request, 'OTP sent to registered email')
        return redirect('validate_otp', otp = otp)


def validate_otp(request, otp = None):
    context = None

    if request.method == 'POST':
        form = forms.OTPForm(request.POST)

        if form.is_valid():
            entered_otp = form.cleaned_data['otp']

            if entered_otp == sent_otp:
                return redirect('change_password')

            else:
                messages.error(request, 'Passwords do not match')

        else:
            context = {
                'otp_form': form,
            }

    elif request.method == 'GET':
        form = forms.OTPForm()

        context = {
            'otp_form': form,
        }

    return render(request, 'home/otp.html', context)


def forgot_password(request):
    context = None

    if request.method == 'POST':
        form = forms.ForgotPasswordForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            return redirect('send_otp', username = username)

        else:
            context = {
                'forgot_password_form': form,
            }

    elif request.method == 'GET':
        form = forms.ForgotPasswordForm()

        context = {
            'forgot_password_form': form,
        }

    return render(request, 'home/forgot_password.html', context)


@login_required(login_url = '/login/')
def change_password(request):
    context = None

    if request.method == 'POST':
        form = forms.ChangePasswordForm(request.POST)

        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            logout(request)
            return redirect('login_user')

        else:
            context = {
                'change_password_form': form,
            }

    elif request.method == 'GET':
        form = forms.ChangePasswordForm()

        context = {
            'change_password_form': form,
        }

    return render(request, 'home/change_password.html', context)


@login_required(login_url = '/login/')
def user_account(request, username):
    user = request.user
    media_types = models.BaseMedia.MEDIA_TYPES
    obj, create = models.RequestList.objects.get_or_create(user = request.user)
    user_request_list = obj if obj else created 

    context = {
        'user': user,
        'media_types': [media[1] for media in media_types],
        'pending_requests': user_request_list.request_set.filter(accepted = False) 
    }

    print(context)
    return render(request, 'home/user_account.html', context)


@login_required(login_url = '/login/')
def update_account(request, username): 
    context = None
    user = request.user
    data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'description': user.description,
            'private_status': user.private,  
        }

    if request.method == 'POST':
        form = forms.UpdateUserDetailsForm(request.POST, initial = data)

        if form.has_changed():
            if form.is_valid():
                for changed_field in form.changed_data:
                    setattr(user, changed_field, form.cleaned_data[changed_field]) 

                user.save()
                print(user)
                return redirect('user_account', username = user.username)
            
            else:
                context = {
                    'update_form': form 
                }

    if request.method == 'GET':
        form = forms.UpdateUserDetailsForm(initial = data)
        context = {
            'update_form': form,
        }

    return render(request, 'home/update_form.html', context = context)


@login_required(login_url = '/login/ ')
def make_playlist(request):
    context = None 

    if request.method == 'POST':
        pass 

    if request.method == 'GET':
        playlist_form = forms.VideoPlayListForm()
        context = {
            'playlist_form': playlist_form,
        }


@login_required(login_url = '/login/')
def upload_media(request, username):
    context = None 

    if request.method == 'POST':
        if 'multi-media-form' in request.POST:
            video_playlist_form = forms.VideoPlayListForm(request.POST)

            if video_playlist_form.is_valid():
                video_playlist_object = video_playlist_form.save()
                video_playlist_object.uploader = request.user
                video_playlist_object.save()
                return redirect('upload_multi_media', video_playlist_uuid = video_playlist_object.uuid)

            else:
                single_media_form = forms.SingleMediaForm()
                media_form = forms.MediaForm()

                context = {
                    'video_playlist_form': video_playlist_form,
                    'single_media_form': single_media_form,
                    'media_form': media_form,
                }

        else:
            single_media_form = forms.SingleMediaForm(request.POST)
            media_form = forms.MediaForm(request.POST)
            media_form = forms.MediaForm()

            if single_media_form.is_valid() and media_form.is_valid():
                single_media_object = single_media_form.save()
                single_media_object.uploader = request.user
                media_object = media_form.save()

                media_object.single_media = single_media_object
                media_object.save()

                print(media_object.single_media.genre, media_object.single_media, media_object.single_media.uploader)
            
            else:
                video_playlist_form = forms.VideoPlayListForm()

                context = {
                    'single_media_form': single_media_form,
                    'video_playlist_form': video_playlist_form,
                    'media_form': media_form
                }


    if request.method == 'GET':
        single_media_form = forms.SingleMediaForm()
        video_playlist_form = forms.VideoPlayListForm()
        media_form = forms.MediaForm()

        context = {
            'single_media_form': single_media_form,
            'video_playlist_form': video_playlist_form,
            'media_form': media_form
        }

    return render(request, 'home/upload_media.html', context)


@login_required(login_url = '/login/')
def upload_multi_media(request, video_playlist_uuid):
    context = None 

    if request.method == 'POST':
        multi_media_form = forms.MultiMediaForm(request.POST)
        print(multi_media_form, request.POST)

        if multi_media_form.is_valid():
            video_playlist = models.VideoPlayList.objects.get(uuid = video_playlist_uuid)
            multi_media_object = multi_media_form.save()
            multi_media_object.playlist = video_playlist 
            multi_media_object.save()

            episode_count = int(multi_media_form.cleaned_data['episode_count'])

            return redirect('upload_episodes', multi_media_uuid = multi_media_object.uuid, episode_count = episode_count)

        else:
           context = {
                'multi_media_form': multi_media_form,
           }

    elif request.method == 'GET':
        video_playlist = models.VideoPlayList.objects.get(uuid = video_playlist_uuid)
        multi_media_form = forms.MultiMediaForm()

        context = {
            'multi_media_form': multi_media_form,
        }

    return render(request, 'home/upload_multi_media.html', context) 



@login_required(login_url = '/login/')
def upload_episodes(request, multi_media_uuid, episode_count = None):
    context = None 
    multi_media = models.MultiMedia.objects.get(uuid = multi_media_uuid)
    MediaFormset = modelformset_factory(
        models.Media,
        formset = forms.BaseMediaFormSet,
        form = forms.MediaForm,
        extra = episode_count,
    )

    if request.method == 'POST':
        media_formset = MediaFormset(request.POST)

        if media_formset.is_valid():
            for form in media_formset:
                media_object = form.save()
                media_object.multi_media = multi_media 
                media_object.save()

            return redirect('edit_multi_media', uuid = multi_media_uuid, permanent = True)

        else:
            print('formset has errors', media_formset.errors, media_formset.non_form_errors())
            
            context = {
                'media_formset': media_formset,
            }

        print(multi_media.media_set.all())

    elif request.method == 'GET':
        media_formset = MediaFormset()

        context = {
            'media_formset': media_formset,
        }

    return render(request, 'home/episode_upload_form.html', context)


@login_required(login_url = '/login/')
def recent_uploads(request, username):
    context = None
    user = request.user 

    if request.method == 'POST':
        pass 

    if request.method == 'GET':
        single_medias = models.SingleMedia.objects.all().filter(uploader = user)[0:10]
        video_playlists = models.VideoPlayList.objects.all().filter(uploader = user)[0:10]

        context = {
            'single_medias': single_medias,
            'video_playlists': video_playlists,
        }

        return render(request, 'home/recent_uploads.html', context)
        

"""
<------------------- Delete Views ----------------------->
"""

@login_required(login_url = '/login/')
def delete_playlist(request, uuid):
    item = models.VideoPlayList.objects.get(uuid = uuid)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = '/login/')
def delete_multi_media(request, uuid):
    item = models.MultiMedia.objects.get(uuid = uuid)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = '/login/')
def delete_episode(request, uuid):
    item = models.Media.objects.get(uuid = uuid)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))



"""
<---------------- Edit Views --------------------------->
"""
@login_required(login_url = '/login/')
def edit_playlist(request, username, playlist_uuid):
    context = None 
    playlist = models.VideoPlayList.objects.get(uuid = playlist_uuid)
  
    if request.method == 'POST':
        playlist_form = forms.VideoPlayListForm(request.POST, instance = playlist)
        success_redirect = False 

        if playlist_form.has_changed():
            if playlist_form.is_valid():
                for attribute in playlist_form.changed_data:
                    setattr(playlist, attribute, playlist_form.cleaned_data[attribute])
                
                playlist.save()
                success_redirect = True

            else:
                context = {
                    'playlist_form': playlist_form,
                }
        else:
            success_redirect = True 

        if success_redirect:
            return redirect('recent_uploads', username = request.user.username)

    elif request.method == 'GET':
        playlist_form = forms.VideoPlayListForm(instance = playlist)
        multi_medias = playlist.multimedia_set.all()
        
        context = {
            'playlist_form': playlist_form,
            'multi_medias':  multi_medias,
            'playlist': playlist,
        }

    return render(request, 'home/edit_playlist.html', context)



@login_required(login_url = '/login/')
def edit_multi_media(request, uuid):
    context = None 
    multi_media = models.MultiMedia.objects.get(uuid = uuid)
    ModelForm = modelform_factory(models.MultiMedia, 
        fields = ('name', 'description'),
    )

    redirect_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        multi_media_form = ModelForm(request.POST, instance = multi_media)
        success_redirect = False 
        
        if multi_media_form.has_changed():
            if multi_media_form.is_valid():
                for attribute in multi_media_form.changed_data:
                    setattr(multi_media, attribute, multi_media_form.cleaned_data[attribute])
                
                multi_media.save()
                messages.success(request, 'Changes done successfully!')
                success_redirect = True 

            else:
                context = {
                    'multi_media_form': multi_media_form,
                }

        else:
            success_redirect = True 

        if success_redirect:
            return redirect('edit_multi_media', uuid = uuid)


    elif request.method == 'GET':
        multi_media_form = ModelForm(instance = multi_media)
        multi_media_episodes = multi_media.media_set.all()
        print(multi_media_episodes)

        context = {
            'multi_media_form': multi_media_form,
            'multi_media_episodes': multi_media_episodes,
        }

    return render(request, 'home/edit_multi_media.html', context)


@login_required(login_url = '/login/')
def edit_episode(request, uuid):
    context = None 
    media = models.Media.objects.get(uuid = uuid)

    if request.method == 'POST':
        media_form = forms.MediaForm(request.POST, instance = media)
        success_redirect = False 

        if media_form.has_changed():
            if media_form.is_valid():
                for attribute in media_form.changed_data:
                    setattr(media, attribute, media_form.cleaned_data[attribute])

                media_form.save()
                messages.success(request, 'Changes done successfully !')
                success_redirect = True 

            else:
                print(media_form.errors, messages)
                context = {
                    'media_form': media_form,
                }

        else:
            success_redirect = True 

        if success_redirect:
            return redirect(request.META.get('HTTP_REFERER')) 

    if request.method == 'GET':
        media_form = forms.MediaForm(instance = media)
        context = {
            'media_form': media_form,
        }

    return render(request, 'home/edit_episode.html', context)


@login_required(login_url = '/login/')
def add_more_episodes(request, uuid):
    context = None 
    multi_media = models.MultiMedia.objects.get(uuid = uuid)

    if request.method == 'POST':
        add_more_episode_form = forms.MoreEpisodeForm(request.POST)

        if add_more_episode_form.is_valid():
            episode_count = add_more_episode_form.cleaned_data['episode_count']
            return redirect('upload_episodes', uuid, episode_count)

            
        else:
            context = {
                'more_episode_form': add_more_episode_form,
            }

    elif request.method == 'GET':
        add_more_episode_form = forms.MoreEpisodeForm()

        context = {
            'more_episode_form': add_more_episode_form,
        }

    return render(request, 'home/more_episode_form.html', context)


# <---------- User Follow and following ------------->

@login_required()
def follow_uploader(request, follow_username):
    user_to_follow = models.CustomUser.objects.get(username = follow_username)
    
    if request.method == 'GET':
        if user_to_follow.private:
            new_request = models.Request.objects.create(user = request.user)
            request_list = models.RequestList.objects.filter(user = user_to_follow)
            
            if request_list.exists():
                user_request_list = request_list[0]
            
            else:
                user_request_list = models.RequestList.objects.create(user = user_to_follow)
            
            user_request_list.request_set.add(new_request)
            user_request_list.save()
            
            print(request_list, new_request)

            messages.info(request, f'Request sent successfully to {user_to_follow.username}')

        else:
            #print(request.user, user_to_follow)
            #print(request.user.followers_set.all(), request.user.following_set.all())
            new_follower = models.Followers.objects.create(follower = request.user)
            new_following = models.Following.objects.create(following = user_to_follow)
            user_to_follow.followers_set.add(new_follower)
            request.user.following_set.add(new_following)
            messages.info(request, f'You started following {follow_username}')

    # need to change this
    return HttpResponse('')


def accept_request(request, request_uuid):
    if request.method == 'GET':
        follow_request = models.Request.objects.get(uuid = request_uuid)
        new_follower = models.Followers.objects.create(follower = follow_request.user)
        new_following = models.Following.objects.create(following = request.user) 
        follow_request.user.followers_set.add(new_follower)
        request.user.following_set.add(new_following)
        follow_request.accepted = True 
        follow_request.save()

    # need to change to jquery request

    return HttpResponse('')

 
def cancel_request(request, request_id):
    if request.method == 'GET':
        user_request_list = models.RequestList.objects.get(user = request.user)
        request_obj = models.Request.objects.get(uuid = request_uuid)
        user_request_list.request_set.remove(request_obj)
        request_obj.delete()

    #need to change this to jquery request
    return HttpResponse('')



          