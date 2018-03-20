from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.contrib.auth.models import User
from datetime import datetime

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=128, unique=True)
    activity_type = models.CharField(max_length=128)
    address = models.CharField(max_length=516)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    tags = models.ManyToManyField(Tag)

    @property
    def avgRating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg'] or "No rating"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Activity, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.name


class Picture(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, default='')
    picture = models.ImageField(upload_to='activity_pictures', blank=True)
    activity = models.ForeignKey(Activity)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=128, blank=True, default='Review')
    date = models.DateField()
    rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    message = models.TextField(blank=True, default='')
    activity = models.ForeignKey(Activity)
    user = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        self.date = datetime.today()
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
