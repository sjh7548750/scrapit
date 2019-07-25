from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Folder(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    def __str__(self):
        return self.title


class Scrap(models.Model): #Scrap이라는 객체 이름 만듬
    title = models.CharField(max_length=250) #스크랩 제목
    address = models.TextField() #스크랩 주소
    preview = models.ImageField(upload_to = 'images/') #스크랩 미리보기
    description = models.TextField() #스크랩 설명
    pub_date = models.DateTimeField('date published') #스크랩한 날짜
    folder = models.ForeignKey(Folder, on_delete = models.CASCADE, null = True)
    
    def __str__(self):
        return self.title
    
    