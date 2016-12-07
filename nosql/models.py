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
        ordering = ('-stackoverflow_followers',)
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

    def get_rank(self):
        actual = self.stackoverflow_followers
        if actual > 1000:
            actual = 1000
        std = (actual - 5) / (1000 - 5)
        rank = std * (5-1) + 1
        return int(rank)

    def get_performance_ranking(self):
        comments = Comment.objects.filter(nosql=self)
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        for comment in comments:
            if comment.positive and comment.probability > 0.60:
                positive_count +=1
            elif comment.positive == False and comment.probability > 0.60:
                negative_count += 1
            elif comment.probability <= 0.60:
                neutral_count += 1
        if len(comments) != 0:
            positive = round((positive_count * 100)/len(comments), 2)
            negative = round((negative_count * 100)/len(comments), 2)
            neutral = round((neutral_count * 100)/len(comments), 2)
        else:
            positive = 0
            negative = 0
            neutral = 0
        return [negative, neutral, positive]

    def get_ranking_distribution(self):
        comments = Comment.objects.filter(nosql=self)
        bucket_1 = 0
        bucket_2 = 0
        bucket_3 = 0
        bucket_4 = 0
        bucket_5 = 0
        for comment in comments:
            probability = comment.probability
            if comment.positive == False:
                probability = 1- probability
            if probability <= 0.2:
                bucket_1 += 1
            if probability > 0.2 and probability <= 0.4:
                bucket_2 += 1
            if probability > 0.4 and probability <= 0.6:
                bucket_3 += 1
            if probability > 0.6 and probability <= 0.8:
                bucket_4 += 1
            if probability > 0.8:
                bucket_5 += 1

        if len(comments) != 0:
            bucket_1_perc = round((bucket_1 * 100)/len(comments), 2)
            bucket_2_perc = round((bucket_2 * 100)/len(comments), 2)
            bucket_3_perc = round((bucket_3 * 100)/len(comments), 2)
            bucket_4_perc = round((bucket_4 * 100)/len(comments), 2)
            bucket_5_perc = round((bucket_5 * 100)/len(comments), 2)
        else:
            bucket_1_perc = 0
            bucket_2_perc = 0
            bucket_3_perc = 0
            bucket_4_perc = 0
            bucket_5_perc = 0
        return [bucket_1_perc, bucket_2_perc, bucket_3_perc, bucket_4_perc, bucket_5_perc]

    def get_performance_rank(self):
        comments = Comment.objects.filter(nosql=self)
        v = len(comments)
        m = 10
        total = 0
        wr = 0
        star = 0
        if len(comments) != 0:
            for comment in comments:
                probability = comment.probability
                if comment.positive == False:
                    probability = 1 - probability
                total += probability

            R = total /len(comments)
            c = 6.9
            wr = (v / (v+m)) * R + (m / (v+m)) * c

            if wr <= 2:
                star = 1
            if wr > 2 and wr <= 4:
                star = 2
            if wr > 4 and wr <= 6:
                star = 3
            if wr > 6 and wr <= 8:
                star = 4
            if probability > 8:
                star = 5
        return [round(wr, 1), star]

    def get_comments(self):
        comments = Comment.objects.filter(nosql=self)
        ranking = []
        for comment in comments:
            if comment.positive == False:
                ranking.append(int(round(comment.probability * -10, 0)))
            else:
                ranking.append(int(round(comment.probability * 10, 0)))
        return ranking


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


class Link(models.Model):
    title = models.CharField(max_length=60, unique=True)
    url = models.URLField(unique=True)
    number_backlinks = models.IntegerField(default=0)
    nosql = models.ForeignKey(Nosql, related_name='links', null=False)
    class Meta:
        ordering = ('-number_backlinks',)


class Comment(models.Model):
    nosql = models.ForeignKey(Nosql, related_name='comments')
    url = models.URLField(unique=True)
    body = models.TextField()
    positive = models.BooleanField(default=False)
    probability = models.FloatField(default=0.0)

    def __str__(self):
        return 'Comment {} on {}'.format(self.url, self.nosql)