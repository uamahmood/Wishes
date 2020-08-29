from django.contrib import messages
from django.shortcuts import render, redirect
import bcrypt
from .models import *


def index(request):
    return render(request, 'index.html')

def wishes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'all_wishes': Wish.objects.all(),
        'my_ungranted_wishes': Wish.objects.filter(is_granted=False).filter(uploaded_by=user),
        'all_granted_wishes': Wish.objects.filter(is_granted=True)
    }
    return render(request, 'wishes.html', context)

def register(request):
    print(request.POST)
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        print('registering a user')
        password = request.POST['register_password']
        pw_hs = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        print('password: ', password)
        print('pw_hs: ', pw_hs)

        user = User.objects.create(
            first_name=request.POST['register_first_name'],
            last_name=request.POST['register_last_name'],
            email=request.POST['register_email'],
            password=pw_hs
        )
        request.session['user_id'] = user.id
        return redirect('/wishes')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_to_login = User.objects.get(
            email=request.POST['login_email']
        )
        request.session['user_id'] = user_to_login.id
        return redirect('/wishes')

def logout(request):
    request.session.flush()
    return redirect('/')

def wish(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'wishes_new.html', context)

def create_wish(request):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        user_login = User.objects.get(id=request.session['user_id'])
        wish = Wish.objects.create(
            item=request.POST['wish_item'],
            describe=request.POST['item_describe'],
            uploaded_by=user_login
        )
    return redirect('/wishes')

def delete_item(request, wish_id):
    Wish.objects.get(id=wish_id).delete()
    return redirect('/wishes')

def edit_item(request, wish_id):
    context = {
        'wish': Wish.objects.get(id=wish_id)
    }
    return render(request, 'edit_wish.html', context)

def edit_update(request, wish_id):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/wishes/{wish_id}/edit')
    else:
        wish = Wish.objects.get(id=wish_id)
        wish.item = request.POST['wish_item']
        wish.describe = request.POST['item_describe']
        wish.save()

        return redirect('/wishes')

def granted_item(request, wish_id):

    wish_to_granted = Wish.objects.get(id=wish_id)
    print(wish_to_granted)
    print(wish_to_granted.is_granted)
    wish_to_granted.is_granted= True
    wish_to_granted.save()
    return redirect('/wishes')

def granted_like(request, wish_id):
    granted_to_like = Wish.objects.get(id=wish_id)
    user_doing_the_liking = User.objects.get(id=request.session['user_id'])
    granted_to_like.users_who_liked.add(user_doing_the_liking)
    return redirect('/wishes')