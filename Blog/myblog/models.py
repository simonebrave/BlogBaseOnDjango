from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    status_choice = ((0, '离线'),
                     (1, '在线'))

    username = models.CharField(max_length=68, unique=True, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    password = models.CharField(max_length=568, verbose_name='登录密码')
    re_time = models.DateTimeField(default=timezone.now, verbose_name='注册时间')
    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name='用户状态')

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-re_time',]
        verbose_name = '用户'
        verbose_name_plural='用户'


class Blog(models.Model):
    status_choice = ((0, '发表'),
                     (1, '草稿'))

    title = models.CharField(max_length=100, verbose_name='标题')
    status = models.SmallIntegerField(choices=status_choice, default=1, verbose_name='博客状态')
    author = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='作者', related_name='blog_post')
    # body = models.ForeignKey('Content', null=True, blank=True, on_delete=models.CASCADE, verbose_name='博文', related_name='blog_body')
    body = models.TextField(verbose_name='博文', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='发表时间', null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_time',]
        verbose_name = '博客'
        verbose_name_plural = '博客'


class Content(models.Model):
    blog_id = models.OneToOneField('Blog', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        blog = Blog.objects.get(pk=self.blog_id)
        return blog.title

    class Meta:
        ordering = ['blog_id',]
        verbose_name = '博文'
        verbose_name_plural = '博文'

class Comment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name='博客')
    comment_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='评论者')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    comment_text = models.TextField(verbose_name='评论详情')

    class Meta:
        ordering = ['-publish_time']
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return 'comment by {} on {}'.format(self.comment_by, self.blog)


