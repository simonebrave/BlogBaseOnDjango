from django.shortcuts import render, HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
import hashlib

from .models import User, Blog
from .forms import LoginForm, RegisterForm

# Create your views here.

def hash_code(s, salt='saltps'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def user_login(request):
    if request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('myblog:userindex', args=(request.session['user_name'],)))
    if request.method == 'POST':
        warning = ''
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username', None)
            password = cd.get('password', None)
            print(username, password)
            try:
                user_obj = User.objects.get(username=username)
            except User.DoesNotExist:
                warning = '用户不存在！'
                return render(request, 'myblog/login.html', {'form':form, 'warning':warning})
            if user_obj:
                if user_obj.password == hash_code(password):

                    #允许登录
                    user_obj.status = 1
                    user_obj.save()
                    request.session['is_login'] = True
                    request.session['user_id'] = user_obj.id
                    request.session['user_name'] = user_obj.username

                    return HttpResponseRedirect(reverse('myblog:userindex', args=(user_obj.username,)))
                else:
                    warning = '密码不正确！'
                    return render(request, 'myblog/login.html', {'form':form,'warning':warning})
        else:
            warning = '请检查输入数据！'
            return render(request, 'myblog/login.html', {'form':form,'warning':warning})
    else:
        form = LoginForm()
    return render(request, 'myblog/login.html', {'form':form})


def user_regist(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            try:
                user_obj = User.objects.get(username=username)
                if user_obj:
                    warning = '用户名已被注册！'
                    return render(request, 'myblog/register.html', {'form':form,'warning':warning})
            except User.DoesNotExist:
                password = hash_code(cd['password1'])
                email = cd['email']
                new_user = User(username=username, email=email, password=password, re_time=timezone.now())
                new_user.save()
                message = '注册成功！'
                return render(request, 'myblog/register.html', {'message': message})
        else:
            warning = '请检查输入数据！'
            return render(request, 'myblog/register.html', {'form':form,'warning':warning})
    else:
        form = RegisterForm()
    return render(request, 'myblog/register.html', {'form': form})


def user_index(request, username):
    print(username)
    return render(request, 'myblog/userindex.html', {'username': username})

def user_logout(request, username):
    if request.session.get('is_login', None):
        print('logout................')
        user_obj = User.objects.get(username=username)
        user_obj.status = 0
        user_obj.save()

        request.session.flush()
        return HttpResponseRedirect(reverse('myblog:login'))

    return HttpResponseRedirect(reverse('myblog:login'))


def user_blogs(request, username):
    if request.method == 'GET':
        try:
            user_obj = User.objects.get(username=username)
            return render(request, 'myblog/blogs.html', {'username': username})
        except User.DoesNotExist:
            return HttpResponse('用户不存在')



def user_posts(request, username):
    blogs = Blog.objects.filter(author__username=username, status=0)
    blogs_title = list()
    for blog in blogs:
        blogs_title.append({'id':blog.id, 'title':blog.title})

    return render(request, 'myblog/posts.html', {'blogs': blogs_title, 'username': username})


def user_newblog(request, username):
    if request.method == 'GET':
        return render(request, 'myblog/newblog1.html', {'username': username})
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        status = request.POST['status']
        print(title, body, status)

        newblog = Blog()
        newblog.title = title
        newblog.body = body
        newblog.status = status
        newblog.created_time = timezone.now()
        newblog.publish_time = timezone.now()
        try:
            author = User.objects.get(username=username)
            newblog.author = author
        except User.DoesNotExist:
            return HttpResponse('用户不存在')
        newblog.save()
        if not status:
            message = '发表成功！'
        else:
            message = '已存为草稿！'
        return render(request, 'myblog/newblog1.html', {'message': message})


def user_drafts(request, username):
    blogs = Blog.objects.filter(author__username=username, status=1)
    blogs_title = list()
    for blog in blogs:
        blogs_title.append({'id': blog.id, 'title': blog.title})

    return render(request, 'myblog/drafts.html', {'blogs': blogs_title, 'username': username})


def blog_detail(request, id):
    try:
        blog = Blog.objects.get(pk=id)
        title = blog.title
        author = blog.author.username
        publish_time = blog.publish_time
        body = blog.body
        status = blog.status
        return render(request, 'myblog/detail.html', {'title': title,
                                                      'author': author,
                                                      'publish_time': publish_time,
                                                      'body': body,
                                                      'status': status})
    except Blog.DoesNotExist:
        message = '你要找的博文已经没有啦！'
        return render(request, 'myblog/detail.html', {'message': message})
    except Exception:
        message = '发生了一点意外哟！'
        return render(request, 'myblog/detail.html', {'message': message})
