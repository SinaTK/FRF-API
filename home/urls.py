from django.urls import path
from home import views
app_name = 'home'

urlpatterns = [
    path('', views.Home.as_view(), name='home'), # endpoint
    path('questions/', views.QuestionsListView.as_view()),
    path('question/create/', views.QuestionsCreateView.as_view()),
    path('question/update/<int:pk>', views.QuestionUpdateView .as_view()),
    path('question/delete/<int:pk>', views.QuestionDeleteView .as_view()),

]   