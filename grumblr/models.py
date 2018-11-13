from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User

class post(models.Model):
    author = models.ForeignKey('userProfile', on_delete=models.CASCADE,)
    Post = models.CharField(max_length=42,)
    Category = models.CharField(max_length=30,)
    last_changed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Post
    # Returns all recent additions and deletions.
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return post.objects.filter(last_changed__gt=time).distinct()

    @staticmethod
    def get_categories(category="general"):
        return post.objects.filter(Category=category).distinct()

    # Generates the HTML-representation.
    @property
    def html(self):
        return self._html
    @html.setter
    def html(self, context):
        self._html = context

    @staticmethod
    def get_max_time():
        return post.objects.all().aggregate(Max('last_changed'))[
                   'last_changed__max'] or "1970-01-01T00:00+00:00"

class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Age = models.IntegerField(verbose_name='age',default=0)
    email = models.EmailField(max_length=30,)
    tel = models.CharField(max_length=11,)
    whatsUp = models.CharField(max_length=42,)
    picture = models.ImageField(upload_to="grumblr-avators", default='grumblr-avators/default.png',blank=True)
    follower = models.ManyToManyField(User, related_name='followed',
                                    symmetrical=False)
    def __str__(self):
        return self.user

class comment(models.Model):
    post = models.ForeignKey(post,on_delete=models.CASCADE)
    author = models.ForeignKey(userProfile,on_delete=models.CASCADE)
    commentTime = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=42)

    @property
    def html(self):
        return self._html
    @html.setter
    def html(self, context):
        self._html = context
