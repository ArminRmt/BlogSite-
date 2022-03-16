from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




from app.views import (
    home_page,
    signup,
    signin,
    signout,
    CreatePost,
    Edame_Akhbar,
    updatePost,
    deletePost,
    post_detail,
    list_akhbar,
    SearchView,
    Varzeshi,
    Elmi,
    Siasi,
    Eghtesadi,
    date_view
)

urlpatterns = [
    path('', home_page, name='home'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout', signout, name='signout'),

    # path('<slug:slug>/', post_detail, name='post_detail'),    
    path('create_post/', CreatePost, name="create_post"),
    path('post/<int:id>/',Edame_Akhbar, name='Edame_Akhbar'),
    path('update_post/<str:pk>/', updatePost, name="update_post"),
    path('delete_post/<str:pk>/', deletePost, name="delete_post"),
    path('post_detail/<str:pk>/', post_detail, name="post_detail"),
    path('list_akhbar/', list_akhbar, name="list_akhbar"),
    
    
    path('results/', SearchView.as_view(), name='search'),
    
    
    path('varzeshi/', Varzeshi, name='varzeshi'),
    path('elmi/', Elmi, name='elmi'),
    path('siasi/', Siasi, name='siasi'),
    path('eghtesadi/', Eghtesadi, name='eghtesadi'),
    
    
    path('date_view/', date_view, name='Date'),


]

if settings.DEBUG : 
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
