from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User, comments, following, post
from django.shortcuts import get_object_or_404
import simplejson as json
import jwt, datetime
from rest_framework.decorators import api_view, renderer_classes

@api_view(['POST'])
def login(request):
    mail = json.loads(request.body)['email']
    pas = json.loads(request.body)['password']
    if not User.objects.filter(email = mail):
        raise AuthenticationFailed("User Not Found")
    user = User.objects.get(email = mail)
    if user.password != pas:
        return HttpResponse('Incorrect Password')
    payload = {
        'id' : user.user_id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat' : datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt' : token
    }
    return response

def comment(request, id):

    if(request.method == 'POST'):
        token = request.COOKIES.get('jwt')
        if token == None :
            AuthenticationFailed("Unauthenticated User")
            return HttpResponse("Failed")
        try :
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed("Unauthenticated User")

        curr = json.loads(request.body)['text']
        b = payload['id']
        mail = User.objects.get(pk = b)
        if (not post.objects.filter(post_id = id)):
            return HttpResponse("404")
        posts = post.objects.get(post_id = id)
        posts.comments_set.create(text = curr, by = mail)
        cmnt = comments.objects.filter(post = id, text = curr, by = mail)
        print(mail.email + " commented")
        x = cmnt.count()
        return JsonResponse([cmnt[x-1].pk], safe = False)
    return HttpResponse("")

def show(request):
    token = request.COOKIES.get('jwt')
    if token == None :
        AuthenticationFailed("Unauthenticated User")
        return HttpResponse("Failed")
    try :
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        AuthenticationFailed("Unauthenticated User")

    curr = payload['id']
    user = User.objects.get(user_id = curr)
    followers = following.objects.filter(followed = user.email).count()
    followings = following.objects.filter(follower = curr).count()
    return JsonResponse({"Email" : user.email, "Followers" : followers, "Following" : followings}, safe=False)

def Post(request):
    token = request.COOKIES.get('jwt')
    if token == None :
        AuthenticationFailed("Unauthenticated User")
        return HttpResponse("Failed")
    try :
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        AuthenticationFailed("Unauthenticated User")

    descp = json.loads(request.body)['desc']
    head = json.loads(request.body)['title']
    id = payload['id']
    user = User.objects.get(pk = id)
    if(not post.objects.filter(desc = descp, title = head, created_by = id)):
        user.post_set.create(desc = descp, title = head, created_on = timezone.now())
        new = post.objects.get(desc = descp, title = head, created_by = id)
        print("post created by - ")
        print(user.email)
        return JsonResponse({"POST_ID" : new.post_id, "Title" : head, "Description" : descp, "Created Time" : new.created_on}, safe=False)
    return HttpResponse("Posted Early")

def follow(request, user_id):
    if(request.method == 'POST'):

        token = request.COOKIES.get('jwt')
        if token == None :
            AuthenticationFailed("Unauthenticated User")
            return HttpResponse("Failed")
        try :
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed("Unauthenticated User")

        curr = json.loads(request.body)['follower']
        followed = get_object_or_404(User,pk = curr)
        follow = get_object_or_404(User,pk = payload['id'])
        check = following.objects.filter(follower = curr, followed = follow)
        if(not check):
            followed.following_set.create(followed = follow)
            print(followed.email + " followed " + follow.email)
            return HttpResponse('success')
        return HttpResponse('already following')
    return HttpResponse("")

def unfollow(request, user_id):
    if(request.method == "POST"):


        token = request.COOKIES.get('jwt')
        if token == None :
            AuthenticationFailed("Unauthenticated User")
            return HttpResponse("Failed")
        try :
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            AuthenticationFailed("Unauthenticated User")

        curr = json.loads(request.body)['follower']
        followed = get_object_or_404(User,pk = curr)
        follow = get_object_or_404(User,pk = payload['id'])
        check = following.objects.filter(follower = curr,followed = follow)
        if(not check):
            return HttpResponse('not following the user')
        check.delete()
        print(followed.email + " unfollowed " + follow.email)
        return HttpResponse("Unfollowed")
    return HttpResponse("")

def like(request, id):
    token = request.COOKIES.get('jwt')
    if token == None :
        AuthenticationFailed("Unauthenticated User")
        return HttpResponse("Failed")
    try :
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        AuthenticationFailed("Unauthenticated User")
    obj = post.objects.get(pk = id)
    obj.likes += 1
    obj.save()
    return HttpResponse("Liked")

def unlike(request, id):
    token = request.COOKIES.get('jwt')
    if token == None :
        AuthenticationFailed("Unauthenticated User")
        return HttpResponse("Failed")
    try :
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        AuthenticationFailed("Unauthenticated User")
    obj = post.objects.get(pk = id)
    obj.unlikes += 1
    obj.save()
    return HttpResponse("Unliked")

def posts(request, id):
    token = request.COOKIES.get('jwt')
    if token == None :
        AuthenticationFailed("Unauthenticated User")
        return HttpResponse("Failed")
    try :
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        AuthenticationFailed("Unauthenticated User")
    if(request.method == 'GET'):
        po = post.objects.get(pk = id)
        return JsonResponse({"Title" : po.title, "Description" : po.desc, "Likes" :
         po.likes, "Unlikes" : po.unlikes, "Created_by" : po.created_by.email})
    if(request.method == 'DELETE'):
        po = post.objects.filter(pk = id)
        po.delete()
        return HttpResponse("Deleted")
    return HttpResponse("")

def all_posts(request, id):
    token = request.COOKIES.get('jwt')
    if token == None :
        AuthenticationFailed("Unauthenticated User")
        return HttpResponse("Failed")
    try :
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        AuthenticationFailed("Unauthenticated User")
    user = User.objects.get(pk = id)
    Posts = post.objects.filter(created_by = user)
    all_p = [[]] * Posts.count()
    for i in range(Posts.count()):
        all_p[i].append(Posts[i].post_id)
        all_p[i].append(Posts[i].title)
        all_p[i].append(Posts[i].desc)
        all_p[i].append(Posts[i].created_on)
        all_p[i].append(Posts[i].likes)
        ne = []
        cmnt = comments.objects.filter(post = Posts[i])
        for j in range(cmnt.count()):
            ne.append(cmnt[j].text)
        all_p[i].append(ne)
    
    x = [[]]
    x.append(all_p[0])
    return JsonResponse(x, safe=False)

