from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class DataModel(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'datamodel'
        verbose_name_plural = 'datamodels'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(DataModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('nosql:nosql_list_by_datamodel', args=[self.slug])


class Nosql(models.Model):
    datamodel = models.ForeignKey(DataModel, related_name='nosqls')
    name = models.CharField(max_length=60, db_index=True)
    slug = models.SlugField(max_length=60, db_index=True)
    not_founded_message = "Not found"
    data_url = models.URLField(default=not_founded_message)

    # Optional data
    official_website = models.URLField()
    developer = models.CharField(max_length=100, default=not_founded_message)
    initial_release = models.CharField(max_length=100, default=not_founded_message)
    current_release = models.CharField(max_length=100, default=not_founded_message)
    license = models.CharField(max_length=60, default=not_founded_message)
    implementation_language = models.CharField(max_length=60, default=not_founded_message)
    typing = models.CharField(max_length=200, default=not_founded_message)
    supported_programming = models.CharField(max_length=400, default=not_founded_message)
    operating_systems = models.CharField(max_length=200, default=not_founded_message)


    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(Nosql, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("nosql:nosql_detail", args=[self.id, self.slug])

