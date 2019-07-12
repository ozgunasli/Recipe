from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.
DIFFUCULTY = (
    ('EASY', _('Easy')),
    ('HARD', _('Hard')),
    ('NORMAL', _('Normal')),
)

class Ingredient(models.Model):
    ingredient=models.CharField(max_length=40)

    def __str__(self):
        return self.ingredient

class Recipe(models.Model):
    user=models.ForeignKey('auth.User',verbose_name='usta',on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    description=models.TextField()
    image=models.ImageField(blank=True,null=True)
    difficulty=models.CharField(max_length=45,choices=DIFFUCULTY)
    ingredients=models.ManyToManyField(Ingredient)
    publishing_date=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(editable=False)
    likes=models.ManyToManyField(User,related_name='likes',blank=True)

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('detail',kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('update', kwargs={'slug': self.slug})

    class Meta:
        ordering=['-publishing_date']

    def get_unique_slug(self):
        slug = slugify(self.name.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Recipe.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self,*args,**kwargs):
        self.slug=self.get_unique_slug()
        return super(Recipe,self).save(*args,**kwargs)




