from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import loader
from .models import User, ToDoItem

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'GET':
        return redirect('/ToDoItem')
    newuser = User.objects.validate(request.POST)
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each) #for each error in the list, make a message for each one.
        return redirect('/')
    if newuser[0] == True:
        request.session['id'] = newuser[1].id
        return redirect('/ToDoItem')

def login(request):
    if 'id' in request.session:
        return redirect('/ToDoList')
    if request.method == 'GET':
        return redirect('/')
    else:
        user = User.objects.login(request.POST)
        if user[0] == False:
            for each in user[1]:
                messages.add_message(request, messages.INFO, each)
            return redirect('/')
        if user[0] == True:
            request.session['id'] = user[1].id
            return redirect('/ToDoItem')

def ToDoItem(request):
    if 'id' not in request.session:
        return redirect ("/")
    user= User.objects.get(id=request.session['id'])
    toDoItem = ToDoItem.objects.filter(user=user, granted=False)
    grantedToDoItem = ToDoItem.objects.filter(user=user, granted=True)

    context = {
        "user": user,
        "ToDoItem": ToDoItem,
        "grantedToDoItem": grantedToDoItem
    }
    return render(request, 'ToDoItem.html', context)

def newToDoItem(request):
    if 'id' not in request.session:
        return redirect ("/")
    user= User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    return render(request, 'create.html', context)

def createToDoItem(request):
    if 'id' not in request.session:
        return redirect ("/")
    if request.method != 'POST':
        return redirect ("/ToDoItem")
    new_toDoItem= ToDoItem.objects.createToDoItem(request.POST, request.session["id"])
    if new_ToDoItem[0]== False:
        for each in new_ToDoItem[1]:
            messages.add_message(request, messages.INFO, each)
        return redirect('/ToDoItem/new')
    else:
        return redirect('/ToDoItem')

def edit(request, ToDoItem_id):
    if 'id' not in request.session:
        return redirect ("/")
    ToDoItem= ToDoItem.objects.get(id=ToDoItem_id)
    context = {
        "ToDoItem": ToDoItem
    }
    return render(request, 'edit.html', context)

def editToDoItem(request,ToDoItem_id):
    if 'id' not in request.session:
        return redirect ("/")
    if request.method != 'POST':
        return redirect ("/ToDoItem")
    edited_ToDoItem = ToDoItem.objects.edittheToDoItem(ToDoItem_id, request.POST)
    if edited_ToDoItem[0]== False:
        for each in edited_ToDoItem[1]:
            messages.add_message(request, messages.INFO, each)
        return redirect(f'/ToDoItem/edit/{ToDoItem_id}')
    else:
        return redirect("/ToDoItem")

def grant(request, ToDoItem_id):
    if 'id' not in request.session:
        return redirect ("/")
    ToDoItem_granted =ToDoItem.objects.grantToDoItemh(ToDoItem_id)
    return redirect("/ToDoItem")

def remove(request, ToDoItem_id):
    if 'id' not in request.session:
        return redirect ("/")
    ToDoItem = ToDoItem.objects.deleteToDoItem(ToDoItem_id)
    return redirect("/ToDoItem")

def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    del request.session['id']
    return redirect('/')