from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from .libs.data_processing import summarizer


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
    implementation_language = models.CharField(max_length=60, default=not_founded_message)
    typing = models.CharField(max_length=200, default=not_founded_message)
    operating_systems = models.CharField(max_length=200, default=not_founded_message)
    stack_description = models.TextField(blank=True)
    official_description = models.TextField(blank=True)
    amount_repos = models.IntegerField(default=0)
    stackshare_votes = models.IntegerField(default=0)
    stackoverflow_followers = models.IntegerField(default=0)
    amount_stackoverflow_questions = models.IntegerField(default=0)


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

    def get_summary(self):
        text = self.stack_description + self.official_description
        summary = summarizer.parseText(text)
        return summary



class License(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.CharField(max_length=100, db_index=True)
    commercial_type = models.BooleanField(default=False)
    open_source_type = models.BooleanField(default=False)
    free_type = models.BooleanField(default=False)
    undefined_type = models.BooleanField(default=True)
    nosql = models.ForeignKey(Nosql, related_name='licenses', null=True)

    def get_type(self):
        type = "Undefined"
        if self.commercial_type:
            type = "Commercial"
        if self.open_source_type:
            type = "Open Source"
        if self.free_type:
            type = "Free"
        return type

    def __str__(self):
        type = "Undefined"
        if self.commercial_type:
            type = "Commercial"
        if self.open_source_type:
            type = "Open Source"
        if self.free_type:
            type = "Free"
        return "%s (%s)" %(self.name, type)


class ProgrammingLanguage(models.Model):
    UNDEFINED = 0
    OFFICIAL = 1
    COMMUNITY_SUPPORTED = 2
    INNOFICIAL = 3
    STATUS_CHOICES = (
        (OFFICIAL, 'Official driver'),
        (COMMUNITY_SUPPORTED, 'Community supported driver'),
        (INNOFICIAL, 'Innoficial driver'),
        (UNDEFINED, 'Undefined status'),
    )
    name = models.CharField(max_length=100, db_index=True)
    slug = models.CharField(max_length=100, db_index=True)
    amount_repos = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNDEFINED)
    nosql = models.ForeignKey(Nosql, related_name='programming_languages', null=True)

    class Meta:
        ordering = ('-amount_repos',)
        verbose_name = 'programming language'
        verbose_name_plural = 'programming languages'

    def __str__(self):
        return "%s (%s)" %(self.name, self.status)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ProgrammingLanguage, self).save(*args, **kwargs)
