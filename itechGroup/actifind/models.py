from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.contrib.auth.models import User
from datetime import datetime

# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    # String interpretation
    def __str__(self):
        return self.name

# Activity model
class Activity(models.Model):
    name = models.CharField(max_length=128, unique=True)
    activity_type = models.CharField(max_length=128)
    address = models.CharField(max_length=516)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User)

    # Function to get average rating from review set
    @property
    def avgRating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg'] or "No rating"

    # Function to process data on save and assign slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Activity, self).save(*args, **kwargs)

    # String interpretations
    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.name

# Picture model
class Picture(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, default='')
    picture = models.ImageField(upload_to='activity_pictures', blank=True)
    activity = models.ForeignKey(Activity)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name

# Review model
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

    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.title

# User profile model, extension of User
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
