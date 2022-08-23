from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import *
import json
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        content = request.POST["create_post"]
        try:
            image = request.FILES['image_post']
        except:
            image=None
        if content =="":
            return JsonResponse({"error":"Your request Falied"})
        Post.objects.create(owner=request.user , content=content ,post_image=image)
        return HttpResponseRedirect(reverse("index"))

    posts = Post.objects.all().order_by("-time")
    paginator = Paginator(posts, 10) # Show 1 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html",{
        "posts":posts ,
        "page_obj": page_obj
        
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        try:
            image = request.FILES['image']
        except:
            image=None

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if image:
                user = User.objects.create_user(username, email, password , image=image)
            else:
                user = User.objects.create_user(username, email, password )
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



def post(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        post_content = request.POST["content"].strip()
        owner = request.user.id 
        try:
            Post.objects.create(owner=owner,content=post_content)
        except:
            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse("index"))

    
    else:
        posts = Post.objects.all().order_by("-time")
        return render(request,"network/index.html",{
            "posts":posts
        })



# def profile(request,user_id):
#     if request.method =="GET":
#         if not request.user.is_authenticated:
#             return HttpResponseRedirect(reverse("index"))
#         user_profile = Post.objects.filter(id=user_id).all()
#         image_url = User.objects.get(id=user_id)
#         following = Followers.objects.all() 



def profile_test(request):
    return render(request,"network/profile.html")

@csrf_exempt
def profile(request,user_id):
    user_browsering = User.objects.get(id=request.user.id)
    user_profile = User.objects.get(id=user_id)
    profile_posts=Post.objects.filter(owner=user_profile).all()
    count_posts = profile_posts.count()
    curr_user_follows_this_profile = False
    following = Followers.objects.filter(user=user_profile).all()
    followers = Followers.objects.filter(following=user_profile).all()
    if user_browsering.is_authenticated:
        curr_user_follows_this_profile=Followers.objects.filter(user=user_browsering,following=user_profile).exists()
        
    return render(request,"network/profile.html",{
        "user":user_browsering,
        "user_profile":user_profile,
        "profile_posts":profile_posts ,
        "followers":following,
        "following":followers,
        "count_posts":count_posts ,
        "following_profile": curr_user_follows_this_profile,
        
    })


@login_required
@csrf_exempt
def like(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        like = data.get("like")
        if like:
            post = Post.objects.get(id=post_id)
            user=User.objects.get(id=request.user.id)
            if user in post.likes.all():
                l = LikedPost.objects.get(post_owner=post.owner,post=post,liker=user)
                l.delete()
                post.likes.remove(user)
                post.save()
                print(post.likes.count())
                return JsonResponse({"like":"etshal","likes_count":str(post.likes.count())},status=200)
            else:
                post.likes.add(user)
                l = LikedPost(post_owner=post.owner,post=post,liker=user)
                l.save()
                print(post.likes.count())
                post.save()
                return JsonResponse({"like":"like et7aet","likes_count":str(post.likes.count())},status=200)

    else:
        return JsonResponse({"error":"Your request Falied"})

def follow(request,user_profile_id):
    if request.method != "POST":
        JsonResponse({"error":"This method is not supported"})
    if request.user.is_authenticated:
        if request.method == "POST":
            user_follow_sent = User.objects.get(id=request.user.id)
            user_following_recived = User.objects.get(id=user_profile_id)
            print(user_follow_sent,user_following_recived)
            if "unfollow_btn" in  request.POST:
                f=Followers.objects.filter(user=user_follow_sent,following=user_following_recived)
                f.delete()
                print("deleted")
            elif "follow_btn" in request.POST:
                f = Followers(user=user_follow_sent,following=user_following_recived)
                f.save()
                print("added")
            else:
                print("test")
            
            return HttpResponseRedirect(reverse("profile", args=(user_profile_id, )))
    else:
        return HttpResponseRedirect(reverse("login"))
@csrf_exempt
def postedit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        content_edit = data.get("content")
        post = Post.objects.get(id=post_id)
        print(data)
        post = Post.objects.get(id=post_id)
        if request.user != post.owner:
            return JsonResponse({"error":"Can only edit your own posts"})
        post.content = content_edit
        print(post.content)
        post.save()
        return HttpResponseRedirect(reverse("profile"),args=(post_id,))
        
@csrf_exempt
def sendit(request,user_profile_id):
    if request.method =="POST":
        receiver = User.objects.get(id=user_profile_id)
        sender = User.objects.get(id=request.user.id)
        content = request.POST["content"]
        if sender.id != receiver.id:
            m=DirectMessage(sender=sender,receiver=receiver,content=content)
            m.save()
        return HttpResponseRedirect(reverse("profile", args=(user_profile_id,)))
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

def inbox(request):
    user = request.user
    return render(request,"network/inbox.html",{
        "user":user
    })

@csrf_exempt
def loadbox(request):
    user = request.user
    my_messages = DirectMessage.objects.filter(receiver=user).order_by("-timestamp").all()
    my_messages_dics = [message.serialize() for message in my_messages]
    # for m in my_messages_dics:
    #     print(m["sender_image"])
    # print("loadtamam")
    return JsonResponse(my_messages_dics,safe=False) 


# from network.models import *
# >>> sherif = User.objects.get(username="sherif")
# >>> seif = User.objects.get(username="seif")
# >>> sh = DirectMessage.objects.filter(sender=sherif , receiver=seif).order_by("-timestamp").all()
# >>> se = DirectMessage.objects.filter(sender=seif , receiver=sherif).order_by("-timestamp").all()
# >>> se
# <QuerySet [<DirectMessage: seif send sherif>]>
# >>> sh
# <QuerySet [<DirectMessage: sherif send seif>, <DirectMessage: sherif send seif>]>
# >>> shl = [i for i in sh]
# >>> shl
# [<DirectMessage: sherif send seif>, <DirectMessage: sherif send seif>]
# >>> sel = [i for i in se]
# >>> [ shl.append(i) for i in sel ]
# [None]
# >>> shl
# [<DirectMessage: sherif send seif>, <DirectMessage: sherif send seif>, <DirectMessage: seif send sherif>]
# >>> shls = sorted(shl , key=lambda message: message.timestamp,reverse=True)
# >>> shls
# [<DirectMessage: sherif send seif>, <DirectMessage: seif send sherif>, <DirectMessage: sherif send seif>]
# >>> 

@csrf_exempt
def load_message(request,message_id):
    try:
        message = DirectMessage.objects.get(id=message_id)
        sherif = message.sender
        seif = message.receiver
       
    except:
        return JsonResponse({"error": "Message not found."}, status=404)

    if request.method =="PUT":
        read_true = json.loads(request.body)
        if read_true.get("read") is not None:
            message.read = read_true.get("read")
            # print(message.read)
            message.save()
            return JsonResponse({"message": "Email sent successfully."},status=204)

    elif request.method =="GET":
        seifm = list(DirectMessage.objects.filter(sender=seif , receiver=sherif).order_by("-timestamp").all())
        sherifm = list(DirectMessage.objects.filter(sender=sherif , receiver=seif).order_by("-timestamp").all())
        for i in seifm:
            sherifm.append(i)
        # print(sherifm)
        sherifm_sorted = sorted(sherifm , key=lambda message: message.timestamp)
        # for i in sherifm_sorted:
        #     print(f"{i.content}")
        messages_box = [ message.serialize() for message in sherifm_sorted ]
        return JsonResponse(messages_box,safe=False)

    else:
        return JsonResponse({"error":"The request must be PUT or get"},status=400)

@csrf_exempt
def directmessages(request):
    print(request)
    if request.method =="POST":
        try:
            data = json.loads(request.body)
            input = data.get("input")
            if input == None:
                return JsonResponse({"error":"please provide a message"},status=401)
            sender = User.objects.get(id=request.user.id)
            receiver = data.get("message_sender")
            receiver_object = User.objects.get(username=receiver)
            m = DirectMessage(sender=sender,receiver=receiver_object,content=input)
            m.save()
        except:
            return JsonResponse({"error":"please provide a message"},status=401)
        print(input,receiver)
        return JsonResponse({"input" : input},status=201)
    else:
        return JsonResponse({"error":"only POST request is allowed"},status=400)


# posts = Post.objects.filter(owner=user).all()
# >>> liker_lists = [ i.likes.all() for i in posts]
# >>> liker_lists
# [<QuerySet [<User: sherif>]>, <QuerySet [<User: seif>, <User: sherif>]>, <QuerySet [<User: sherif>]>]

def notifications(request):
    user = User.objects.get(id=request.user.id)
    following = user.followers.all()
    followers = user.following.all()
    user_posts = Post.objects.filter(owner=user).all()
    
    liked = LikedPost.objects.filter(post_owner=user).all()
    

    return render(request,"network/notifications.html",{
        "name" : user.username,
        "posts":liked,
    "followers":followers,
    "following":following,
    "userposts":user_posts
    })

@csrf_exempt
def delete(request,post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        post.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
