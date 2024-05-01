from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, username, password, email=None, **kwargs):
        user = self.model(
            username=username,
            **kwargs
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, username, password, email=None,**kwargs):
        self._create_user(username, password, email,**kwargs)
    def create_superuser(self, username, password, email=None, **kwargs):
        kwargs.setdefault('is_superuser', True)
        self._create_user(username, password, email,**kwargs)

#유저 확장
class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'

    username = models.CharField(unique=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    organization = models.CharField(max_length=50, null=True)
    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_superuser


#게시물
class Blog(models.Model):
    title = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', null=True)
    #User DB의 pk User id를 외래키로 갖게 됨
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField('Tag', blank=True)
    #한 사람은 여러 게시물의 좋아요가 가능하고 한 게시물은 여러 사람에게 좋아요를 받을 수 있음
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_blog')



    class Meta:
        db_table = 'blog'
    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]

#댓글
class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    #Blog DB의 pk 즉 Blog id를 외래키로 갖게 됨
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    #User DB의 pk User id를 외래키로 갖게 됨
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


    class Meta:
        db_table = 'comment'

    def __str__(self):
        return self.content + ' | ' +str(self.author)
#태그
class Tag(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name

class Profile(models.Model):
    #User DB의 PK와 user를 1:1 대응 관계로 선언
    #1:1 대응 관계는 외래키와 조금 다른데 1:1 대응 관계는 외래키에 최소성을 만족한 것과 같다.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    nickname = models.CharField(max_length=10, null=True)
    image = models.ImageField(upload_to='profile/', null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.nickname