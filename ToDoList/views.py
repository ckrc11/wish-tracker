from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import loader
from .models import User, ToDoItem

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'GET':
        return redirect('/todolist')
    newuser = User.objects.validate(request.POST)
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each) #for each error in the list, make a message for each one.
        return redirect('/')
    if newuser[0] == True:
        request.session['id'] = newuser[1].id
        return redirect('/todolist')

def login(request):
    if 'id' in request.session:
        return redirect('/todolist')
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
            return redirect('/todolist')

def todolist(request):
    if 'id' not in request.session:
        return redirect ("/")
    user= User.objects.get(id=request.session['id'])
    toDoItems = ToDoItem.objects.filter(user=user, granted=False)
    grantedToDoItems = ToDoItem.objects.filter(user=user, granted=True)

    context = {
        "user": user,
        "toDoItems": toDoItems,
        "grantedToDoItems": grantedToDoItems
    }
    return render(request, 'todolist.html', context)

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
        return redirect ("/todolist")
    new_todoitem= ToDoItem.objects.createToDoItem(request.POST, request.session["id"])
    if new_todoitem[0]== False:
        for each in new_ToDoItem[1]:
            messages.add_message(request, messages.INFO, each)
        return redirect('/todolist/new')
    else:
        return redirect('/todolist')

def edit(request, ToDoItem_id):
    if 'id' not in request.session:
        return redirect ("/")
    todoitem= ToDoItem.objects.get(id=ToDoItem_id)
    context = {
        "todoitem": todoitem
    }
    return render(request, 'edit.html', context)

def editToDoItem(request,ToDoItem_id):
    if 'id' not in request.session:
        return redirect ("/")
    if request.method != 'POST':
        return redirect ("/todolist")
    edited_ToDoItem = ToDoItem.objects.edittheToDoItem(ToDoItem_id, request.POST)
    if edited_ToDoItem[0]== False:
        for each in edited_ToDoItem[1]:
            messages.add_message(request, messages.INFO, each)
        return redirect(f'/todolist/edit/{ToDoItem_id}')
    else:
        return redirect("/todolist")

def grant(request, ToDoItem_id):
    if 'id' not in request.session:
        return redirect ("/")
    ToDoItem_granted =ToDoItem.objects.grantToDoItem(ToDoItem_id)
    return redirect("/todolist")

def remove(request, ToDoItem_id):
    if 'id' not in request.session:
        return redirect ("/")
    toDoItem = ToDoItem.objects.deleteToDoItem(ToDoItem_id)
    return redirect("/todolist")

def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    del request.session['id']
    return redirect('/')