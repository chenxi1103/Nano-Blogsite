from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db import transaction

from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string

from grumblr.models import *
from grumblr.forms import *

@login_required
def home(request):
    try:
        currUser = userProfile.objects.get(user=request.user)
        try:
            friend = currUser.follower.all()
            numFriends = len(friend)
        except:
            numFriends = 0
        numPosts = len(post.objects.filter(author=currUser))
        numFollower = len(userProfile.objects.filter(follower=currUser.user))
        return render(request,'grumblr/homepage.html',{'currUser' : currUser,
                'numPosts':numPosts,
                'numFriends':numFriends,
                'numFollower':numFollower,})
    except:
        raise Http404

@transaction.atomic
def register(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/register.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/register.html', context)
    try:
        new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email'],
                                            first_name=form.cleaned_data['firstName'],
                                            last_name=form.cleaned_data['lastName'],)
        new_user.is_active = 0
        new_user.save()
        token = default_token_generator.make_token(new_user)
        email_body = """
            I am waiting for you for a long time! So great to see you here!
            Welcome to Grumblr (￣∇￣) There is only one last step to be our member!
            Simply click this link and enjoy~
            
            http://%s%s
        """ % (request.get_host(),reverse('confirm',args=(new_user.username, token)))
        send_mail(subject='Welcome to Grumblr! One more step: Verify your email adress!',
                  message=email_body,
                  from_email='chenxili@andrew.cmu.edu',
                  recipient_list=[new_user.email]
                  )
        new_userProfile = userProfile.objects.create(user=new_user,
                                      email=form.cleaned_data['email'],
                                      )
        new_userProfile.save()
        return render(request,'grumblr/emailConfirm.html')
    except:
        return render(request,'grumblr/register.html',{'error':'Sorry! The username is registered! Try another one!'})

@transaction.atomic
def confirmEmail(request,username,token):
    confirmUser = get_object_or_404(User,username=username)
    if not default_token_generator.check_token(confirmUser,token):
        raise Http404
    confirmUser.is_active = True
    confirmUser.save()
    return render(request,'grumblr/confrim_email_complete.html')

@login_required
def showProfile(request):
    try:
        currUser = userProfile.objects.get(user=request.user)
        numPosts = len(post.objects.filter(author=currUser))
        numFollower = len(currUser.follower.all())
        try:
            friend = currUser.follower.all()
            friendProfiles = userProfile.objects.filter(user__in=friend)
            numFriends = len(friend)
            return render(request, 'grumblr/userProfile.html', {
                'currUser': currUser,
                'Friends': friendProfiles,
                'numPosts': numPosts,
                'numFriends': numFriends,
                'numFollower': numFollower,
                })
        except:
            numFriends = 0
            return render(request, 'grumblr/userProfile.html', {
                'currUser': currUser,
                'numPosts': numPosts,
                'numFriends': numFriends,
                'numFollower': numFollower,
                })
    except:
        raise Http404
@login_required
def get_userPost(request):
    try:
        posts = post.objects.filter(author=userProfile.objects.get(user=request.user))
        for Post in posts:
            comment_button = "comment-button-%d" % Post.id
            comment_content = "comment-content-%d" % Post.id
            comment_show = "comment-show-%d" % Post.id
            Post.html = render_to_string('grumblr/userPost.html', {"post": Post,
                                                               "comment_content":comment_content,
                                                               "comment_button":comment_button,
                                                               "comment_show":comment_show})
        context = {"posts": posts}
        return render(request, 'grumblr/posts.json', context,
                      content_type='application/json')
    except:
        raise Http404

@login_required
def changePwd(request):
    context = {}
    try:
        if request.method == 'GET':
            context['form'] = changePassword()
            return render(request, 'grumblr/change_password.html', context)

        form = changePassword(request.POST)
        context['form'] = form

        if not form.is_valid():
            return render(request, 'grumblr/change_password.html', context)
        oldPwd = form.cleaned_data['oldPwd']
        user = authenticate(username=request.user.username, password=oldPwd)
        if user:
            user.set_password(form.cleaned_data['newPwd1'])
            user.save()
            return render(request,'grumblr/password_reset_complete.html')
        else:
            context['errors'] = 'Sorry! You old password is wrong!'
            return render(request,'grumblr/change_password.html', context)
    except:
        raise Http404

@login_required
def editProfile(request):
    currUser = request.user
    try:
        currProfile = userProfile.objects.get(user=currUser)
        context = {'currUser':currProfile}
        if request.method == 'GET':
            context['form'] = EditProfile()
            return render(request, 'grumblr/editProfile.html', context)
        form = EditProfile(request.POST, request.FILES)
        if not form.is_valid():
            context['form'] = form
            return render(request,'grumblr/editProfile.html',context)
        currUser.first_name = form.cleaned_data['firstName']
        currUser.last_name = form.cleaned_data['lastName']
        currProfile.Age = form.cleaned_data['Age']
        currProfile.tel = form.cleaned_data['tel']
        currProfile.whatsUp = form.cleaned_data['whatsUp']
        if request.FILES.get('photo'):
            currProfile.picture = request.FILES.get('photo')
        currUser.save()
        currProfile.save()
        return redirect(reverse('userProfile'))
    except:
        raise Http404

@login_required
def get_photo(request,id):
    currUser = get_object_or_404(userProfile,id=id)
    if not currUser.picture:
        return Http404
    content_type = guess_type(currUser.picture.name)
    return HttpResponse(currUser.picture,content_type=content_type)


@login_required
def qpost(request):
    if request.method == 'POST':
        try:
            form = QuickPost(request.POST)
            if not form.is_valid():
                return redirect(reverse('userProfile'))
            Category = form.cleaned_data['Category']
            userPost = form.cleaned_data['Post'].strip()
            newPost = post.objects.create(author=userProfile.objects.get(user=request.user),
                                          Post=userPost,
                                          Category=Category,
                                         )
            newPost.save()
            return HttpResponse("Success!")
        except:
            return HttpResponse("Error!")
    else:
        return HttpResponse("Error!")

@login_required
def AllPost(request):
    currUser = userProfile.objects.get(user=request.user)
    try:
        friend = currUser.follower.all()
        numFriends = len(friend)
    except:
        numFriends = 0
    numPosts = len(post.objects.filter(author=currUser))
    numFollower = len(userProfile.objects.filter(follower=request.user))
    return render(request, 'grumblr/global.html', {
            'category': 'All',
            'numFriends':numFriends,
            'numPosts':numPosts,
            'numFollower':numFollower,
            'currUser':currUser,
            'author' : post.author,
            })

# Returns all recent changes to the database, as JSON
@login_required
def get_changes(request, time="1970-01-01T00:00+00:00"):
    try:
        max_time = post.get_max_time()
        posts = post.get_changes(time).order_by('last_changed')
        for Post in posts:
            comment_button = "comment-button-%d" % Post.id
            comment_content = "comment-content-%d" % Post.id
            comment_show = "comment-show-%d" % Post.id
            Post.html = render_to_string('grumblr/post.html', {"post": Post,
                                                               "comment_content":comment_content,
                                                               "comment_button":comment_button,
                                                               "comment_show":comment_show,
                                                               "currUser": request.user})
        context = {"max_time": max_time, "posts": posts}
        return render(request, 'grumblr/posts.json', context,
                      content_type='application/json')
    except:
        raise Http404

@login_required
def get_category(request,category="General"):
    try:
        posts = post.get_categories(category=category).order_by('last_changed')
        for Post in posts:
            comment_button = "comment-button-%d" % Post.id
            comment_content = "comment-content-%d" % Post.id
            comment_show = "comment-show-%d" % Post.id
            Post.html = render_to_string('grumblr/post.html', {"post": Post,
                                                               "comment_content":comment_content,
                                                               "comment_button":comment_button,
                                                               "comment_show":comment_show,
                                                               "currUser":request.user})
        context = {"posts": posts}
        return render(request, 'grumblr/posts.json', context,
                      content_type='application/json')
    except:
        raise Http404

@login_required
def deletePost(request,id):
    try:
        currPost = post.objects.get(id=id)
        currPost.delete()
        return HttpResponse("Success!")
    except:
        pass
        return HttpResponse("Error!")

@login_required
def add_comments(request, id):
    try:
        currPost = post.objects.get(id=id)
        author = userProfile.objects.get(user=request.user)
        if request.method == 'POST':
            form = makeComment(request.POST)
            if form.is_valid():
                Comment = form.cleaned_data['comment']
                newComment = comment(post=currPost,
                                     author=author,
                                     content=Comment)
                newComment.save()
                return HttpResponse("Success!")
            else:
                return HttpResponse("Error!")
        else:
            return HttpResponse("Error!")
    except:
        return HttpResponse("Error!")

@login_required
def get_comments(request,id):
    try:
        currPost = post.objects.get(id=id)
        comments = comment.objects.filter(post=currPost)
        for Comment in comments:
            Comment.html = render_to_string('grumblr/comment.html',{"comment":Comment, "post-id":id, "currUser":request.user})
        context = {"post_id":id, "comments":comments}
        return render(request, 'grumblr/comments.json', context, content_type='application/json')
    except:
        return render(request,'grumblr/homepage.html')

@login_required
def deleteComment(request,id):
    try:
        currComment = comment.objects.get(id=id)
        currComment.delete()
        return HttpResponse("Success!")
    except:
        pass
        return HttpResponse("Error!")

@login_required
def checkUser(request):
    try:
        if request.method == 'GET':
            userName = request.GET['author']
            user = User.objects.get(username=userName)
            thisAuthor = userProfile.objects.get(user=user)
            return render(request, 'grumblr/checkUser.html', {
                'author': thisAuthor,
                'currUser':request.user})
        else:
            return render(request, 'grumblr/checkUser.html',
                          {'error': 'Sorry, no such user exists'})
    except:
        raise Http404

@login_required
def followUser(request, operation, id):
    try:
        newFriend = userProfile.objects.get(id=id).user
        currUser = userProfile.objects.get(user=request.user)
        if operation == 'follow':
            if request.user != newFriend:
                currUser.follower.add(newFriend)
        elif operation == 'remove':
            currUser.follower.remove(newFriend)
        return redirect(reverse('followStream'))
    except:
        raise Http404

@login_required
def followStream(request):
    try:
        Friends = userProfile.objects.get(user=request.user).follower.all()
        if len(Friends)!=0:
            return render(request, 'grumblr/followerStream.html',
                              {'friends': Friends,})
        else:
            return render(request, 'grumblr/followerStream.html', {
                'error': 'Sorry! You have not follow anyone :('
                })
    except:
        raise Http404

@login_required
def get_followerStream(request):
    try:
        Friends = userProfile.objects.get(user=request.user).follower.all()
        friends = userProfile.objects.filter(user__in=Friends)
        posts = post.objects.filter(author__in=friends).order_by('last_changed')
        for Post in posts:
            comment_button = "comment-button-%d" % Post.id
            comment_content = "comment-content-%d" % Post.id
            comment_show = "comment-show-%d" % Post.id
            Post.html = render_to_string('grumblr/follower.html', {"post": Post,
                                                               "comment_content":comment_content,
                                                               "comment_button":comment_button,
                                                               "comment_show":comment_show})
        context = {"posts": posts}
        return render(request, 'grumblr/posts.json', context,
                      content_type='application/json')
    except:
        raise Http404

@login_required
def checkByCategory(request, category):
    try:
        currUser = userProfile.objects.get(user=request.user)
        try:
            friends = currUser.follower.all()
            numFriends = len(friends)
        except:
            numFriends = 0
        numPosts = len(post.objects.filter(author=currUser))
        numFollower = len(userProfile.objects.filter(follower=request.user))
        return render(request,'grumblr/categories.html',{
                'category' : category,
                'currUser': currUser,
                'numFriends':numFriends,
                'numPosts':numPosts,
                'numFollower':numFollower
                })
    except:
        raise Http404