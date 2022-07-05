from django.urls import path
from . import views
from django.contrib.auth import views as loginVieww
urlpatterns = [
    path('',views.home,name='home'),
    path('notes/',views.notes,name='notes'),
    path('delete_a_note/<int:id>',views.deleteNote,name='deleteNote'),
    path('note_detail/<int:pk>',views.noteDetail.as_view(),name='noteDetail'),
    path('homework/',views.homework,name='homework'),
    path('update_homework/<int:pk>',views.updateHomework,name='updateHomework'),
    path('delete_homework/<int:pk>',views.deleteHomework,name='deleteHomework'),
    path('youtube/',views.youtube,name='youtube'),
    path('to-do/',views.todo,name='todo'),
    path('updateTodo/<int:pk>',views.updateTodo,name='updateTodo'),
    path('deleteTodo/<int:pk>',views.deleteTodo,name='deleteTodo'),
    path('books/',views.books,name='books'),
    path('dictionary/',views.dictionary,name='dictionary'),
    path('wikipedia/',views.wiki,name='wikipedia'),
    path('register/',views.signUpForm,name='register'),
    path('login/',loginVieww.LoginView.as_view(template_name='dashboard/login.html'),name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',loginVieww.LogoutView.as_view(template_name='dashboard/logout.html'),name='logout')
]
