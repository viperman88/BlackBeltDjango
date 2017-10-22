from django.shortcuts import render, HttpResponse, redirect
from .models import User, Friend

def index(request):
    return render(request, 'friends/index.html')

def register(request):
    check = User.userManager.register(request.POST['name'], request.POST['alias'], request.POST['email'], request.POST['password'], request.POST['pass_conf'], request.POST['birthday'])
    if (not check[0]):
        errors = []
        for key, value in check[1].iteritems():
            errors.append(value)
        context = {
            'errors' : errors
        }
        return render(request, 'friends/index.html', context)
    else:
        request.session['id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/friends')

def login(request):
    check = User.userManager.login(request.POST['email'], request.POST['password'])
    if (not check[0]):
        errors = [check[1]]
        context = {
            'errors' : errors
        }
        return render(request, 'friends/index.html', context)
    else:
        request.session['id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/friends')

def logout(request):
    request.session['id'] = 0
    return redirect('/')

def friends(request):
    myself = User.objects.get(id=request.session['id'])
    try:
        users = User.objects.all()
        others = []
        for other_user in users:
            if (other_user.id != request.session['id']):
                others.append(other_user)
    except:
        users = None

    try:
        friends = Friend.objects.filter(user_friend=myself)
        real_friends = []
        for each_friend in friends:
            real_friends.append(each_friend.friend_2)
        real_others = []
        for other_user in others:
            if (other_user not in real_friends):
                real_others.append(other_user)
    except:
        friends = None

    context = {
        'myself' : myself,
        'users' : real_others,
        'friends' : real_friends
    }
    return render(request, 'friends/friends.html', context)

def profile(request, id):
    profile = User.objects.get(id=id)
    context = {
        'user' : profile
    }
    return render(request, 'friends/profile.html', context)

def add(request, id):
    User.userManager.addFriend(request.session['id'], id)
    return redirect('/friends')

def remove(request, id):
    User.userManager.removeFriend(request.session['id'], id)
    return redirect('/friends')
