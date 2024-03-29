from django.template.defaultfilters import slugify
from django.contrib.syndication.views import Feed
from database.models.user import PsUser
from django.db import models
from tinymce import models as tinymce_models


class BlogFeed(Feed):
    title = "Photoshop Park"
    link = "/blog/"

    author_email = "kait@photoshoppark"  # change later

    def item_author_name(self, item):
        return item.author

    def items(self):
        return Article.objects.filter(status=1)


STATUS = (
    (0, "Draft"),
    (1, "Published")
)


class Category(models.Model):
    title = models.CharField(max_length=120)
    image = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

# needs to be a function because of django wierdness
def get_default_category():
    return Category.objects.get_or_create(title="Uncategorized")[0].id


class Article(models.Model):
    title = models.CharField(max_length=120)
    authors = models.ForeignKey(PsUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default=get_default_category,
                                 related_name="articles")

    image = models.URLField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    slug = models.SlugField(max_length=240, unique=True)
    created_on = models.DateField(auto_now_add=True)

    description = models.CharField(max_length=240)
    content = tinymce_models.HTMLField()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
