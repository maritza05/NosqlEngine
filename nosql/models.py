from django.db import models
from django.core.urlresolvers import reverse

class DataModel(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'datamodel'
        verbose_name_plural = 'datamodels'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('nosql:nosql_list_by_datamodel', args=[self.slug])


class Nosql(models.Model):
    datamodel = models.ForeignKey(DataModel, related_name='nosqls')
    name = models.CharField(max_length=60, db_index=True)
    slug = models.SlugField(max_length=60, db_index=True)
    official_website = models.URLField()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("nosql:nosql_detail", args=[self.id, self.slug])

