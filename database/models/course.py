from django.db import models
from django.template.defaultfilters import slugify
from django.views.generic import ListView
from tinymce import models as tinymce_models
from database.models.user import PsUser as User


class Lesson(models.Model):
    title = models.CharField(max_length=120, default="")
    authors = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=240)
    created_on = models.DateField(auto_now_add=True)
    slug = models.CharField(max_length=120, default="")
    image = models.URLField(
        default="https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/cute-photos-of-cats-cuddling-1593203046.jpg")
    content = tinymce_models.HTMLField()

    def __str__(self):
        return self.title

    # Automaticly generate slugs on save, admin field also comes prefilled
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Lesson, self).save(*args, **kwargs)


class Course(models.Model):
    lessons = models.ManyToManyField(Lesson, related_name="courses", blank=True)
    title = models.CharField(max_length=120)
    authors = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=240)
    slug = models.CharField(max_length=120, default='')
    image = models.URLField(blank=True,
                            default='https://image-cdn.essentiallysports.com/wp-content/uploads/2022-05'
                                    '-06T155027Z_1312978751_UP1EI561801C4_RTRMADP_3_TENNIS-MADRID.jpg?width=600')

    def __str__(self):
        return self.title

    # autogen slugs again
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

# Enrollment joining table for the many to many and also progress tracking!
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    progress = models.IntegerField()
