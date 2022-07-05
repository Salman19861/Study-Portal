from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib import messages 
from youtubesearchpython import VideosSearch
import requests, json, wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method=='POST':
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f'Notes added Successfully by {request.user.username} !')
    
    form=NotesForm()
    notes=Notes.objects.filter(user=request.user)
    
    return render(request,'dashboard/notes.html',{'notes':notes,'form':form})

@login_required
def deleteNote(request,id):
    Notes.objects.get(id=id).delete()
    return HttpResponseRedirect('/notes/')

from django.views import generic
class noteDetail(generic.DetailView):
    model=Notes

@login_required
def homework(request):
    if request.method=='POST':
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False

            homework=Homework(user=request.user,subject=request.POST['subject']
            ,chapter=request.POST['chapter'],topic=request.POST['topic'],due=request.POST['due'],
            is_finished=finished)
            homework.save()
            messages.success(request,'Homework added Successfully !')


    form=HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False
    return render(request,'dashboard/homework.html',{'homework':homework,'homework_done':homework_done,'form':form})

@login_required
def updateHomework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return HttpResponseRedirect('/homework/')

@login_required
def deleteHomework(request,pk):
    Homework.objects.get(id=pk).delete()
    messages.success(request,'homework deleted Successfully !')
    return HttpResponseRedirect('/homework/')

@login_required
def youtube(request):
    if request.method=='POST':
        try:
            form=DashbaordForm(request.POST)
            search=request.POST['search']
            videos=VideosSearch(search,limit=20)
            result_list=[]
            for i in videos.result()['result']:
                result_dict={
                    'title':i['title'],
                    'duration':i['duration'],
                    'thumbnail':i['thumbnails'][0]['url'],
                    'channel':i['channel']['name'],
                    'link':i['link'],
                    'views':i['viewCount']['short'],
                    'published':i['publishedTime']
                }
                desc=''
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        desc=j['text']
                result_dict['description']=desc
                result_list.append(result_dict)
            return render(request,'dashboard/youtube.html',{'form':form,'results':result_list})
        except:
            messages.warning(request,'Please Check your Internet Connection !')

    else:        
        form=DashbaordForm()
    return render(request,'dashboard/youtube.html',{'form':form})


@login_required
def todo(request):
    if request.method=='POST':
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False
                finished.save()
            except:
                finised=False
            todo=Todo(user=request.user,title=request.POST['title'])
            todo.save()
            messages.success(request,'Created Successfully !')


    form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todoDone=True
    else:
        todoDone=False
    return render(request,'dashboard/todo.html',{'todo':todo,'todoDone':todoDone,'form':form})


@login_required
def updateTodo(request,pk=None):
    todoObjects=Todo.objects.get(id=pk)
    if todoObjects.is_finished==True:
        todoObjects.is_finished=False
    else:
        todoObjects.is_finished=True
    todoObjects.save()
    return HttpResponseRedirect('/to-do/')

@login_required
def deleteTodo(request,pk):
    Todo.objects.get(id=pk).delete()
    messages.success(request,'Task deleted Successfully !')
    return HttpResponseRedirect('/to-do/')

@login_required
def books(request):
    if request.method=='POST':
        try:
            form=DashbaordForm(request.POST)
            search=request.POST['search']
            url="https://www.googleapis.com/books/v1/volumes?q="+search
            r=requests.get(url)
            answer=r.json()                                        #pip install requests
            result_list=[]                                          #import requests
            for i in range(10):
                result_dict={
                    'title':answer['items'][i]['volumeInfo']['title'],
                    'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                    'description':answer['items'][i]['volumeInfo'].get('description'),
                    'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                    'categories':answer['items'][i]['volumeInfo'].get('categories'),
                    'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                    'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                    'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                }
            
                result_list.append(result_dict)
            return render(request,'dashboard/books.html',{'form':form,'results':result_list})
        except:
            messages.warning(request,'Please Check your Internet Connection !')

    else:        
        form=DashbaordForm()
    return render(request,'dashboard/books.html',{'form':form})


@login_required
def dictionary(request):
    if request.method=='POST':
        try:
            form=DashbaordForm(request.POST)
            search=request.POST['search']
            url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+search
            # url="https://od-api.oxforddictionaries.com/api/v2/entries/en-us/"+search
            r=requests.get(url)
            answer=r.json()
            try:
                phonetics=answer[0]['phonetics'][0]['text']
                audio=answer[0]['phonetics'][0]['audio']
                definition=answer[0]['meanings'][0]['definitions'][0]['definition']
                example=answer[0]['meanings'][0]['definitions'][0]['example']
                synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
                context={'form':form,'input':search,'phonetics':phonetics,'audio':audio,'definition':definition,
                'example':example,'synonyms':synonyms}
                
            except:
                context={'form':form,'input':''}
                messages.warning(request,'Word Not Found in dictionary !')
            
            return render(request,'dashboard/dictionary.html',context)

        except:
            print('217')
            messages.warning(request,'Please Check your Internet Connection !')
    else:
        print(220)
        form=DashbaordForm()
    return render(request,'dashboard/dictionary.html',{'form':form})

@login_required
def wiki(request):                         #pip install wikipedia      #import wikipedia
    if request.method=='POST':
        try:
            search=request.POST['search']
            print('224')
            form=DashbaordForm(request.POST)
            search=wikipedia.page(search)
            context={
                'form':form,
                'title':search.title,
                'link':search.url,
                'details':search.summary,
            }
        except:
            messages.warning(request,'Not Found!')
            context={'form':form}

        return render(request,'dashboard/wiki.html',context)

    form=DashbaordForm()
    return render(request,'dashboard/wiki.html',{'form':form})    


def signUpForm(request):
    if request.method=='POST':
        form=registrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account, Created Successfully !')
            return HttpResponseRedirect('/login/')
    else:
        form=registrationForm()
    return render(request,'dashboard/register.html',{'form':form})

@login_required
def profile(request):
    homework=Homework.objects.filter(is_finished=False,user=request.user)
    todo=Todo.objects.filter(is_finished=False,user=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False
    
    if len(todo)==0:
        todo_done=True
    else:
        todo_done=False
    return render(request,'dashboard/profile.html',{'homework':homework,'todo':todo,'homework_done':homework_done,'todo_done':todo_done})



