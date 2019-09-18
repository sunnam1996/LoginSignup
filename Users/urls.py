from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',  views.index, name='index'),
    path('register/', views.usercreation, name='register'),
    path('accounts/login/', views.userpage, name='userpage'),
    path('accounts/login/userpage/', views.userauthentication, name='userauthentication'),
    path('postcategory',views.postcategory,name='postcategory'),
    path('postquestion',views.postquestion,name='postquestion'),
    path('viewquestions',views.viewquestions, name='viewquestions'),
    path('viewhistory/', views.viewhistory, name='viewhistory'),
    path('userhistory/<int:pk>/', views.userhistory, name='userhistory'),
    path('updateprofile',views.updateprofile, name = 'updateprofile'),
    path('viewcategory/', views.viewcategory,name= 'viewcategory'),
    path('takequiz/<int:pk>/',views.takequiz, name='takequiz'),
    path('result/<int:pk>/', views.result, name='result'),
    path('editquestion/<int:pk>/', views.editquestions, name='editquestion'),
    path('editcatogiries/<int:pk>/', views.editcategories, name='editcategory'),
    path('success/',views.success, name='success'),
    path('forgot/',views.forgot, name='forgot'),
    path('questionlist/', views.QuestionList.as_view(), name='questionlist'),
    path('questiondetal/<int:pk>/',views.QuestionDetail.as_view(),name='questiondetail'),
    path('viewanswers/',views.viewanswers,name = 'viewanswers')

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
