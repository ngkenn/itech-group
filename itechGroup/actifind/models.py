from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=128, unique=True)
    type = models.CharField(max_length=128)
    address = models.CharField(max_length=516)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    tags = models.ManyToManyField(Tag)

    @property
    def avgRating(self):
        return self.review_set.aggregate(Avg('rating')).values()[0] or "No rating"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Activity, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.name

class Picture(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    picture = models.ImageField(upload_to='activity_pictures', blank=True)
    slug = models.SlugField(unique=True)
    activity = models.ForeignKey(Activity)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Picture, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=128)
    date = models.DateField()
    rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    article = models.ForeignKey(Activity)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
