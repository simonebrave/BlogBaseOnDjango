from django.shortcuts import render, HttpResponse,redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
import hashlib

from .models import User, Blog, Comment
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
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username', None)
            password = cd.get('password', None)
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

                    blogs_obj = Blog.objects.filter(status=0).order_by('-publish_time')
                    blogs = list()
                    for blog in blogs_obj:
                        blogs.append({'title': blog.title, 'id': blog.id})
                    redirect(reverse('myblog:userindex', args=(user_obj.username,)))
                    return render(request, 'myblog/userindex.html', {'username': username,'blogs': blogs})
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
        status = request.POST.get('status', 0)
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
        return render(request, 'myblog/newblog1.html', {'message': message})


def user_drafts(request, username):
    blogs = Blog.objects.filter(author__username=username, status=1)
    blogs_title = list()
    for blog in blogs:
        blogs_title.append({'id': blog.id, 'title': blog.title})

    return render(request, 'myblog/drafts.html', {'blogs': blogs_title, 'username': username})


def blog_detail(request, id):
    if request.method == 'GET':
        try:
            blog = Blog.objects.get(pk=id)
            comments = list()
            comments_obj = Comment.objects.filter(blog__pk=id)[:3]
            for comment in comments_obj:
                comments.append('{}: {}'.format(comment.comment_by, comment.comment_text))
            print(comments)
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            return render(request, 'myblog/detail.html', {'title': blog.title,
                                                          'author': blog.author.username,
                                                          'publish_time': blog.publish_time,
                                                          'body': blog.body,
                                                          'status': blog.status,
                                                          'id': id,
                                                          'comments': comments})
        except Blog.DoesNotExist:
            message = '你要找的博文已经没有啦！'
            return render(request, 'myblog/detail.html', {'message': message, 'id': id,})
        except Exception:
            message = '发生了一点意外哟！'
            return render(request, 'myblog/detail.html', {'message': message, 'id': id,})
    elif request.method == 'POST':
        comment_by_id = request.session.get('user_id', None)
        if comment_by_id:
            comment_text = request.POST.get('comment_body', None)
            if comment_text:
                comment = Comment()
                comment.blog = Blog.objects.get(pk=request.POST['blog_id'])
                comment.comment_by = User.objects.get(pk=comment_by_id)
                comment.comment_text = comment_text
                comment.publish_time = timezone.now()
                comment.save()
                return render(request, 'myblog/detail.html', {'comment': comment_text,
                                                              'comment_by': comment.comment_by.username,
                                                              'id': request.POST['blog_id']
                                                              })
            else:
                return HttpResponse('评论内容不可为空！')
        else:
            return HttpResponse('请先登录!')


def index(request):
    try:
        blogs_obj = Blog.objects.filter(status=0).order_by('-publish_time')
        blogs = list()
        for blog in blogs_obj:
            blogs.append({'title': blog.title, 'id':blog.id})
        return render(request, 'myblog/index.html', {'blogs': blogs})
    except:
        message = 'No data'
        return render(request, 'myblog/index.html', {'message':message})