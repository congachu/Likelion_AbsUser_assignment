from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    #User DB의 PK와 user를 1:1 대응 관계로 선언
    #1:1 대응 관계는 외래키와 조금 다른데 1:1 대응 관계는 외래키에 최소성을 만족한 것과 같다.
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    nickname = models.CharField(max_length=10, null=True)
    image = models.ImageField(upload_to='profile/', null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.nickname

