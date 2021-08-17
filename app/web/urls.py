from django.urls import path
from app.web import views as web_view
app_name='web'
urlpatterns = [
    path('', web_view.Index.as_view(), name='index'),
]