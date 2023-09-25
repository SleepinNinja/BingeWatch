from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name = 'home_page'),
    path('/<str:media_type>/', views.media_pages, name = 'media_pages'),
    path('search/<str:search_value>/', views.search, name = 'search'),
    path('search/<str:search_value>/<str:uuid>/', views.open_playlist, name = 'open_playlist'),
    path('search/<str:search_value>/season/<str:season_name>/<str:season_uuid>/', views.open_media, name = 'open_media'),
    path('search/<str:search_value>/season/<str:season_name>/<str:season_uuid>/video/<str:video_uuid>/', views.open_video, name = 'open_video'),
    path('search/<str:search_value>/video/<str:video_uuid>/', views.open_single_video, name="open_single_video"),
    path('login/', views.login_user, name = 'login_user'),
    path('signup/', views.signup, name = 'signup'),
    path('logout/', views.logout_user, name = 'logout_user'),
    path('change_password/', views.change_password, name = 'change_password'),
    path('validate_otp/', views.validate_otp, name = 'validate_otp'),
    path('send_otp/<str:username>/', views.send_otp, name = 'send_otp'),
    path('forgot_password/', views.forgot_password, name = 'forgot_password'),
    path('user_account/<str:username>/', views.user_account, name = 'user_account'),
    path('update_account/<str:username>/', views.update_account, name='update_account'),
    path('<str:username>/upload_media/', views.upload_media, name = 'upload_media'),
    path('upload_multi_media/<str:video_playlist_uuid>/', views.upload_multi_media, name = 'upload_multi_media'),
    path('user_account/<str:username>/recent_uploads/', views.recent_uploads, name = 'recent_uploads'),
    path('user_account/upload_episodes/<str:multi_media_uuid>/<int:episode_count>/', views.upload_episodes, name = 'upload_episodes'),
    path('user_account/<str:username>/edit_playlist/<str:playlist_uuid>/', views.edit_playlist, name = 'edit_playlist'),
    path('user_account/delete_playlist/<str:uuid>/', views.delete_playlist, name = 'delete_playlist'),
    path('user_account/delete_multi_media/<str:uuid>/', views.delete_multi_media, name = 'delete_multi_media'),
    path('user_account/delete_episode/<str:uuid>/', views.delete_episode, name = 'delete_episode'),
    path('user_account/delete_single_media/<str:uuid>/', views.delete_single_media, name = 'delete_single_media'),
    path('user_account/edit_multi_media/<str:uuid>/', views.edit_multi_media, name = 'edit_multi_media'),
    path('user_account/edit_single_media/<str:uuid>', views.edit_single_media, name = 'edit_single_media'),
    path('user_account/edit_episode/<str:uuid>/', views.edit_episode, name = 'edit_episode'),
    path('user_account/add_more_episode/<str:uuid>/', views.add_more_episodes, name = 'add_more_episodes'),
    path('follow/<str:follow_username>/', views.follow_uploader, name='follow_uploader'),
    path('accept_request/<str:request_uuid>', views.accept_request, name='accept_request'),
    path('cancel_request/<str:request_uuid>', views.cancel_request, name = 'cancel_request'),
    path('recent/<str:media_type>', views.FilterByGenreInProfileView.as_view() ,name='recent_media')
]
