from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import loader
from .models import User, Wish

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'GET':
        return redirect('/wishes')
    newuser = User.objects.validate(request.POST)
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each) #for each error in the list, make a message for each one.
        return redirect('/')
    if newuser[0] == True:
        request.session['id'] = newuser[1].id
        return redirect('/wishes')

def login(request):
    if 'id' in request.session:
        return redirect('/wishes')
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
            return redirect('/wishes')

def wishes(request):
    if 'id' not in request.session:
        return redirect ("/")
    user= User.objects.get(id=request.session['id'])
    wishes = Wish.objects.filter(wisher=user, granted=False)
    grantedwishes = Wish.objects.filter(wisher=user, granted=True)

    context = {
        "user": user,
        "wishes": wishes,
        "grantedwishes": grantedwishes
    }
    return render(request, 'wishes.html', context)

def newWish(request):
    if 'id' not in request.session:
        return redirect ("/")
    user= User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    return render(request, 'create.html', context)

def createwish(request):
    if 'id' not in request.session:
        return redirect ("/")
    if request.method != 'POST':
        return redirect ("/wishes")
    new_wish= Wish.objects.createwish(request.POST, request.session["id"])
    if new_wish[0]== False:
        for each in new_wish[1]:
            messages.add_message(request, messages.INFO, each)
        return redirect('/wishes/new')
    else:
        return redirect('/wishes')

def edit(request, wish_id):
    if 'id' not in request.session:
        return redirect ("/")
    wish= Wish.objects.get(id=wish_id)
    context = {
        "wish": wish
    }
    return render(request, 'edit.html', context)

def editwish(request, wish_id):
    if 'id' not in request.session:
        return redirect ("/")
    if request.method != 'POST':
        return redirect ("/wishes")
    edited_wish = Wish.objects.editthewish(wish_id, request.POST)
    if edited_wish[0]== False:
        for each in edited_wish[1]:
            messages.add_message(request, messages.INFO, each)
        return redirect(f'/wishes/edit/{wish_id}')
    else:
        return redirect("/wishes")

def grant(request, wish_id):
    if 'id' not in request.session:
        return redirect ("/")
    wish_granted = Wish.objects.grantwish(wish_id)
    return redirect("/wishes")

def remove(request, wish_id):
    if 'id' not in request.session:
        return redirect ("/")
    wish = Wish.objects.deletewish(wish_id)
    return redirect("/wishes")

def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    del request.session['id']
    return redirect('/')