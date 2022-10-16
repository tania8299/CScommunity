from ast import Try
from contextvars import Context
from django.conf import settings
from email.mime import image
from genericpath import exists
from hashlib import new
from itertools import chain

from multiprocessing import context
from operator import contains
from urllib import request
from xml.etree.ElementTree import Comment
from django import views
from django.contrib.auth.models import User
from django.forms import PasswordInput
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from core.models import  LikePost, Post, Profile

from django.template import Context,Template
from django.contrib.auth.models import User


@login_required(login_url='signin')
def index(request):
       user_object = User.objects.get(username=request.user.username)
       user_profile = Profile.objects.get(user=user_object)
       ALL_REQUEST_USER=Profile.objects.filter(isverified=False)
       posts=Post.objects.all().order_by('created_at').reverse()
       
#        user_following_list = []
#     feed = []

#     user_following = FollowersCount.objects.filter(follower=request.user.username)

#     for users in user_following:
#         user_following_list.append(users.user)

#     for usernames in user_following_list:
#         feed_lists = Post.objects.filter(user=usernames)
#         feed.append(feed_lists)

#     feed_list = list(chain(*feed))

#     # user suggestion starts
#     all_users = User.objects.all()
#     user_following_all = []

#     for user in user_following:
#         user_list = User.objects.get(username=user.user)
#         user_following_all.append(user_list)
    
#     new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
#     current_user = User.objects.filter(username=request.user.username)
#     final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
#     random.shuffle(final_suggestions_list)

#     username_profile = []
#     username_profile_list = []

#     for users in final_suggestions_list:
#         username_profile.append(users.id)

#     for ids in username_profile:
#         profile_lists = Profile.objects.filter(id_user=ids)
#         username_profile_list.append(profile_lists)

#     suggestions_username_profile_list = list(chain(*username_profile_list))


#     return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})
       
       
       return render(request,'index.html',{'user_profile': user_profile,'posts': posts,'unverified_user_count':len(list(ALL_REQUEST_USER))})
def setting(request):
       user_profile = Profile.objects.get(user=request.user)
       if request.method == 'POST':
              
              if request.FILES.get('image')== None:
                     image = user_profile.profileimg
                     name =request.POST['name']
                     bio = request.POST['bio']
                     contact=request.POST['contact']
                     location = request.POST['location']
                     batch=request.POST['batch']
                     working=request.POST['working']
                     techinal_experiance = request.POST['techinal_experiance']

                     user_profile.profileimg =image
                     user_profile.name=name
                     user_profile.bio = bio
                     user_profile.location =location
                     user_profile.batch=batch
                     user_profile.contact=contact
                     user_profile.working=working
                     user_profile.techinal_experiance = techinal_experiance
                     user_profile.save()
              if request.FILES.get('image') !=None:
                     image = request.FILES.get('image')
                     name =request.POST['name']
                     bio = request.POST['bio']
                     location = request.POST['location']
                     contact=request.POST['contact']
                     batch=request.POST['batch']
                     working=request.POST['working']
                     techinal_experiance = request.POST['techinal_experiance']
                     
                     user_profile.profileimg =image
                     user_profile.name=name
                     user_profile.bio =bio
                     user_profile.location =location
                     user_profile.batch=batch
                     user_profile.contact=contact
                     user_profile.working=working
                     user_profile.techinal_experiance = techinal_experiance
                     user_profile.save()

              return redirect('setting')    

       
       return render(request,'setting.html',{'user_profile': user_profile})

def pro(request):
       user_profile = Profile.objects.get(user=request.user)
       ALL_REQUEST_USER=Profile.objects.filter(isverified=False)
      #user_object=
       return render(request,'pro.html',{'user_profile':user_profile,'unverified_user_count':len(list(ALL_REQUEST_USER))})       
def pf(request):
       user_profile = Profile.objects.get(user=request.user)
       return render(request,'pro.html',{'user_profile':user_profile})
def signup(request):
       if request.method =='POST':
              username = request.POST['username']
              email = request.POST['email']
             
              password = request.POST['password']
              password2 = request.POST['password2']

              if password == password2:
                     if User.objects.filter(email=email).exists():
                            messages.info(request,'Email taken')
                          
              
                            return redirect('signup')
                     elif User.objects.filter(username=username).exists():
                            messages.info(request,'Userame taken')
                            return redirect('settings')
                     else:
                            user =User.objects.create_user(username=username,email=email,password=password)
                            user.save()
                           
                            messages.success(request, 'You have successfully created account')

                            #create a profile object
                            user_model=User.objects.get(username =username)
                            new_profile= Profile.objects.create(user=user_model,id_user=user_model.id)
                            new_profile.save()
                            return redirect('signup')
              else:
               messages.info(request,'passwod not matching')
               return redirect('signup')
       else:          
        return render(request,'signup.html')
def signin(request):

       if request.method == 'POST':
              username =request.POST['username']
              password =request.POST['password']
              user =auth.authenticate(username=username,password=password)

              if user is not None:
                     USER_PROFILE=Profile.objects.get(user=user)
                     if USER_PROFILE.isverified:
                            auth.login(request,user)
                            return redirect('/')
                     else:
                            return HttpResponse("Your are not Verified by Others.")
              else:
                     messages.info(request,'credential Invalid')
                     return redirect('signin')           
       else:
              return render (request,'signin.html')    


@login_required(login_url="login")

def change_password(request): 
    if request.method =='POST':
        newpass = request.POST.get('newpassword')
        user = User.objects.get(username=request.user.username)
        user.password(newpass)
        user.save();
        messages.success(request,'password has been changed')
        return redirect('/') 
    return render(request,'change_password.html')

@login_required(login_url='signin')
def upload(request):


    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        post_title = request.POST['post_title']
        post_data=request.POST['post_data']

        new_post = Post.objects.create(user=user, image=image,post_title=post_title, post_data=post_data)
        new_post.save()

        return redirect('/')
    else:

        return redirect('settings')
@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')      
def  logout(request):
           auth.logout(request)
           return redirect('signin')  
def code(request):
       # user_profile = Profile.objects.get(user=request.user)
       ALL_REQUEST_USER=Profile.objects.filter(isverified=False)
       # 
       #        return render(request,'code.html'{'user_profile': user_profile})  
       user_profile = Profile.objects.get(user=request.user)


       return render(request,'code.html',{'user_profile':user_profile,'unverified_user_count':len(list(ALL_REQUEST_USER))})
def comment(request):
     

      if request.method == 'POST':
               user = request.user.username
        
               comment_data=request.POST['comment_data']

               new_comment = Post.objects.create(user=user,  comment_data=comment_data)

               new_comment.save()
               return redirect('/')
      else:

                  
           return redirect('setting')

     
def chatroom(request):
       user_profile = Profile.objects.get(user=request.user)
       ALL_REQUEST_USER=Profile.objects.filter(isverified=False)


       return render(request,'chatroom.html',{'user_profile':user_profile,'unverified_user_count':len(list(ALL_REQUEST_USER))})
           
              


def frequest(request):
              user_profile = Profile.objects.get(user=request.user)
              ALL_REQUEST_USER=Profile.objects.filter(isverified=False)
              return render(request,'frequest.html', {'user_profile':user_profile,'all_request_user':ALL_REQUEST_USER})
def accfrequest(request):
              # user_profile = Profile.objects.get(user=request.user)
              UNVERIFIED_USER_NAME=request.GET.get('unverifieduser')
              U_USER=User.objects.get(username=UNVERIFIED_USER_NAME)
              UNVERIFIED_USER=Profile.objects.get(user=U_USER)
              UNVERIFIED_USER.isverified=True
              UNVERIFIED_USER.save()
              return HttpResponse("index.html")

def about_me(request):
              user_profile = Profile.objects.get(user=request.user)


              return render(request,'about_me.html', {'user_profile':user_profile})  


def my_photos(request):
              user_profile = Profile.objects.get(user=request.user)


              return render(request,'my_photos.html', {'user_profile':user_profile})  

def thoughts(request):
              user_profile = Profile.objects.get(user=request.user)


              return render(request,'thoughts.html', {'user_profile':user_profile})                                      
def search(request):
           user_object = User.objects.get(username=request.user.username)
           user_profile = Profile.objects.get(user=user_object)

           if request.method == 'POST':
            username = request.POST['username']
           username_object = User.objects.filter(username__icontains=username)

           username_profile = []
           username_profile_list = []

           for users in username_object:
            username_profile.append(users.id)

           for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
           username_profile_list = list(chain(*username_profile_list))
           return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
def home(request):
           return HttpResponse('home.html')
