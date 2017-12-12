from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models
from django_countries.fields import CountryField
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin





class Trainer(models.Model, HitCountMixin):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=250, verbose_name='Name', blank=True)
    mobile = models.IntegerField(default=0, verbose_name='Mobile', blank=True)
    organisation = models.CharField(max_length=250, verbose_name='Organisation', blank=True)
    designation = models.CharField(max_length=500, verbose_name='Designation', blank=True)
    TCATEGORY_CHOICES = (
        ('LEARNING AND DEVELOPMENT', 'learning and development'),
        ('CONFERENCES', 'conference'),
        ('COMMUNICATION', 'communication'),
        ('MOTIVATION', 'motivation'),
        ('LEADERSHIP', 'leadership'),
        ('EDUCATION', 'education'),
        ('BUSINESS', 'business'),
        ('NETWORKING', 'networking'),
        ('ORGANIZATION', 'organization'),
        ('MEETUPS', 'meetups'),
        ('CREATIVITY AND INNOVATION', 'creativity and innovation'),
        ('MANAGEMENT', 'management'),
        ('INFORMATION TECHNOLOGY', 'information technology'),
        ('OPERATIONS', 'operations'),
        ('CONSULTING', 'consulting'),
        ('FINANCE', 'finance'),
        ('HUMAN RESOURCES', 'human resources'),
        ('MANUFACTURING', 'manufacturing'),
    )
    category = models.CharField(max_length=100, null=True, verbose_name='Category', choices=TCATEGORY_CHOICES, default='', blank=False)
    country = CountryField(blank_label='(select country)', null=True)

    picture = models.FileField(verbose_name='Upload Image', blank=True)
    joindate = models.DateTimeField(auto_now=True, blank=False)
    is_favorite = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.name

    @property
    def percentage_complete(self):
        percent = {'name': 10, 'mobile': 50, 'organisation': 10, 'designation': 10, 'category': 10, 'picture': 10}
        total = 0
        if self.name:
            total += percent.get('name', 0)
        if self.mobile:
            total += percent.get('mobile', 0)
        if self.organisation:
            total += percent.get('organisation', 0)
        if self.designation:
            total += percent.get('designation', 0)
        if self.category:
            total += percent.get('category', 0)
        if self.picture:
            total += percent.get('picture', 0)

        return "%s" % (total)




class Client(models.Model):
    user = models.ForeignKey(User)
    cname = models.CharField(max_length=250, verbose_name='Name')
    cmobile = models.IntegerField(default=0, verbose_name='Mobile')
    corganisation = models.CharField(max_length=250, verbose_name='Organisation')
    cdesignation = models.CharField(max_length=500, verbose_name='Designation')
    CCATEGORY_CHOICES = (
        ('LEARNING AND DEVELOPMENT', 'learning and development'),
        ('CONFERENCES', 'conference'),
        ('COMMUNICATION', 'communication'),
        ('MOTIVATION', 'motivation'),
        ('LEADERSHIP', 'leadership'),
        ('EDUCATION', 'education'),
        ('BUSINESS', 'business'),
        ('NETWORKING', 'networking'),
        ('ORGANIZATION', 'organization'),
        ('MEETUPS', 'meetups'),
        ('CREATIVITY AND INNOVATION', 'creativity and innovation'),
        ('MANAGEMENT', 'management'),
        ('INFORMATION TECHNOLOGY', 'information technology'),
        ('OPERATIONS', 'operations'),
        ('CONSULTING', 'consulting'),
        ('FINANCE', 'finance'),
        ('HUMAN RESOURCES', 'human resources'),
        ('MANUFACTURING', 'manufacturing'),
    )
    ccategory = models.CharField(max_length=100, null=True, verbose_name='Category', choices=CCATEGORY_CHOICES, default='', blank=False)
    country = CountryField(blank_label='(select country)', null=True)

    cpicture = models.FileField(verbose_name='Upload Image')
    cjoindate = models.DateTimeField(auto_now=True, blank=False)





    def __str__(self):
        return self.cname



class Event(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    etitle = models.CharField(max_length=250, verbose_name='Event Title', blank=False)
    ECATEGORY_CHOICES = (
        ('LEARNING AND DEVELOPMENT', 'learning and development'),
        ('CONFERENCES', 'conference'),
        ('COMMUNICATION', 'communication'),
        ('MOTIVATION', 'motivation'),
        ('LEADERSHIP', 'leadership'),
        ('EDUCATION', 'education'),
        ('BUSINESS', 'business'),
        ('NETWORKING', 'networking'),
        ('ORGANIZATION', 'organization'),
        ('MEETUPS', 'meetups'),
        ('CREATIVITY AND INNOVATION', 'creativity and innovation'),
        ('MANAGEMENT', 'management'),
        ('INFORMATION TECHNOLOGY', 'information technology'),
        ('OPERATIONS', 'operations'),
        ('CONSULTING', 'consulting'),
        ('FINANCE', 'finance'),
        ('HUMAN RESOURCES', 'human resources'),
        ('MANUFACTURING', 'manufacturing'),
    )
    ecategory = models.CharField(max_length=100, verbose_name='Category', choices=ECATEGORY_CHOICES, default='', blank=False)
    ESUBCATEGORY_CHOICES = (
        ('LEARNING AND DEVELOPMENT', 'learning and development'),
        ('CONFERENCES', 'conference'),
        ('COMMUNICATION', 'communication'),
        ('MOTIVATION', 'motivation'),
        ('LEADERSHIP', 'leadership'),
        ('EDUCATION', 'education'),
        ('BUSINESS', 'business'),
        ('NETWORKING', 'networking'),
        ('ORGANIZATION', 'organization'),
        ('MEETUPS', 'meetups'),
        ('CREATIVITY AND INNOVATION', 'creativity and innovation'),
        ('MANAGEMENT', 'management'),
        ('INFORMATION TECHNOLOGY', 'information technology'),
        ('OPERATIONS', 'operations'),
        ('CONSULTING', 'consulting'),
        ('FINANCE', 'finance'),
        ('HUMAN RESOURCES', 'human resources'),
        ('MANUFACTURING', 'manufacturing'),
    )
    esubcategory = models.CharField(max_length=100, verbose_name='Sub Category', choices=ESUBCATEGORY_CHOICES, default=0, blank=False )
    EDURATION_CHOICES = (
        ('SHORT', 'Short'),
        ('MEDIUM', 'Medium'),
        ('LONG', 'Long'),
    )
    eduration = models.CharField(max_length=20, choices=EDURATION_CHOICES, verbose_name='Event Duration', default=0, blank=False)
    EDELIVERY_CHOICES = (
        ('CLASSROOM', 'Classroom'),
        ('ONLINE', 'Online'),

    )
    edelivery = models.CharField(max_length=20, choices=EDELIVERY_CHOICES, verbose_name='Event Delivery', default=0, blank=False)



    eventstart = models.DateTimeField(null=True, blank=True, verbose_name='Start Date & Time')
    eventend = models.DateTimeField(null=True, blank=True, verbose_name='End Date & TIme')


    edescription = models.CharField(max_length=500, verbose_name='Description', blank=False, default='')
    ecost = models.IntegerField(default=0, verbose_name='Event Cost')
    elocation = models.CharField(max_length=250, verbose_name='Location', blank=False)
    efacebook = models.CharField(max_length=300, verbose_name='Facebook Link',default='')
    ewebsite = models.CharField(max_length=300, verbose_name='Website Link',default='')
    epicture = models.FileField(verbose_name='Upload Image', blank=False)
    epublish = models.DateTimeField(auto_now=True, blank=False)
    is_favorite = models.BooleanField(default=False)



    def __str__(self):
        return self.etitle



class Webinar(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    wtitle = models.CharField(max_length=250, verbose_name='Webinar Title')
    WCATEGORY_CHOICES = (
        ('LEARNING AND DEVELOPMENT', 'learning and development'),
        ('CONFERENCES', 'conference'),
        ('COMMUNICATION', 'communication'),
        ('MOTIVATION', 'motivation'),
        ('LEADERSHIP', 'leadership'),
        ('EDUCATION', 'education'),
        ('BUSINESS', 'business'),
        ('NETWORKING', 'networking'),
        ('ORGANIZATION', 'organization'),
        ('MEETUPS', 'meetups'),
        ('CREATIVITY AND INNOVATION', 'creativity and innovation'),
        ('MANAGEMENT', 'management'),
        ('INFORMATION TECHNOLOGY', 'information technology'),
        ('OPERATIONS', 'operations'),
        ('CONSULTING', 'consulting'),
        ('FINANCE', 'finance'),
        ('HUMAN RESOURCES', 'human resources'),
        ('MANUFACTURING', 'manufacturing'),
    )
    wcategory = models.CharField(max_length=100, verbose_name='Category', choices=WCATEGORY_CHOICES, default=0,
                                 blank=False)

    webinarstart = models.DateTimeField(null=True, blank=True, verbose_name='Start Date & Time')
    webinarend = models.DateTimeField(null=True, blank=True, verbose_name='End Date & TIme')
    wdescription = models.CharField(max_length=500, verbose_name='Description', null=True)
    wcost = models.IntegerField(default=0, verbose_name='Webinar Cost')
    wwebsite = models.CharField(max_length=300, verbose_name='Website Link', default='')
    wpublish = models.DateTimeField(auto_now=True, blank=False)

    wpicture = models.FileField(verbose_name='Upload Image')
    is_favorite = models.BooleanField(default=False)



    def __str__(self):
        return self.wtitle



class Article(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    atitle = models.CharField(max_length=250,verbose_name='Title')
    adiscription = models.CharField(max_length=500,verbose_name='Description')

    ACATEGORY_CHOICES = (
        ('LEARNING AND DEVELOPMENT', 'learning and development'),
        ('CONFERENCES', 'conference'),
        ('COMMUNICATION', 'communication'),
        ('MOTIVATION', 'motivation'),
        ('LEADERSHIP', 'leadership'),
        ('EDUCATION', 'education'),
        ('BUSINESS', 'business'),
        ('NETWORKING', 'networking'),
        ('ORGANIZATION', 'organization'),
        ('MEETUPS', 'meetups'),
        ('CREATIVITY AND INNOVATION', 'creativity and innovation'),
        ('MANAGEMENT', 'management'),
        ('INFORMATION TECHNOLOGY', 'information technology'),
        ('OPERATIONS', 'operations'),
        ('CONSULTING', 'consulting'),
        ('FINANCE', 'finance'),
        ('HUMAN RESOURCES', 'human resources'),
        ('MANUFACTURING', 'manufacturing'),
    )
    acategory = models.CharField(max_length=100, verbose_name='Category', choices=ACATEGORY_CHOICES, default=0,
                                 blank=False)
    apicture = models.FileField(verbose_name='Upload Image')
    apublish = models.DateTimeField(auto_now=True, blank=False)
    is_favorite = models.BooleanField(default=False)



    def __str__(self):
        return self.atitle


class Elearning(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    ltitle = models.CharField(max_length=250,verbose_name='Title')
    ldiscription = models.CharField(max_length=500,verbose_name='Description')
    LCATEGORY_CHOICES = (
        ('LEARNING AND DEVELOPMENT', 'learning and development'),
        ('CONFERENCES', 'conference'),
        ('COMMUNICATION', 'communication'),
        ('MOTIVATION', 'motivation'),
        ('LEADERSHIP', 'leadership'),
        ('EDUCATION', 'education'),
        ('BUSINESS', 'business'),
        ('NETWORKING', 'networking'),
        ('ORGANIZATION', 'organization'),
        ('MEETUPS', 'meetups'),
        ('CREATIVITY AND INNOVATION', 'creativity and innovation'),
        ('MANAGEMENT', 'management'),
        ('INFORMATION TECHNOLOGY', 'information technology'),
        ('OPERATIONS', 'operations'),
        ('CONSULTING', 'consulting'),
        ('FINANCE', 'finance'),
        ('HUMAN RESOURCES', 'human resources'),
        ('MANUFACTURING', 'manufacturing'),
    )
    lcategory = models.CharField(max_length=100, verbose_name='Category', choices=LCATEGORY_CHOICES, default=0,
                                 blank=False)
    lpicture = models.FileField(verbose_name='Upload Image')
    lwebsite = models.CharField(max_length=300, verbose_name='Elearning platform Link', default='')
    lpublish = models.DateTimeField(auto_now=True, blank=False)
    is_favorite = models.BooleanField(default=False)



    def __str__(self):
        return self.ltitle



class Olocation(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    otitle = models.CharField(max_length=250, verbose_name='Title')
    odiscription = models.CharField(max_length=500, verbose_name='Description')
    location = models.CharField(max_length=250, verbose_name='Location')
    opublish = models.DateTimeField(auto_now=True, blank=False)
    owebsite = models.CharField(max_length=300, verbose_name='Website Link', default='')
    opicture = models.FileField(verbose_name='Upload Image')
    is_favorite = models.BooleanField(default=False)



    def __str__(self):
        return self.otitle








class Eventreview(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000, verbose_name='Write Review', blank=False)
    rating = models.CharField(max_length=10,verbose_name='Give Rating', blank=False, default='')
    ereviewdate = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.review


class Eventcomment(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    eventreview = models.ForeignKey(Eventreview, on_delete=models.CASCADE, default=1)
    comment = models.CharField(max_length=1000, verbose_name='Comment')
    ecommentdate = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.comment





class Eventquery(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    subject = models.CharField(max_length=100, verbose_name='Write Subject', default=1, blank=False)
    message = models.CharField(max_length=1000, verbose_name='Write Message', blank=False)
    equerydate = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.message




class Webinarreview(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000, verbose_name='Write Review', blank=False)
    rating = models.CharField(max_length=10,verbose_name='Give Rating', blank=False, default='')
    wreviewdate = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.review


class Webinarcomment(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)
    webinarreview = models.ForeignKey(Webinarreview, on_delete=models.CASCADE, default=1)
    comment = models.CharField(max_length=1000, verbose_name='Comment')
    wcommentdate = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.comment



class Olocationreview(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    olocation = models.ForeignKey(Olocation, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000, verbose_name='Write Review', blank=False)
    rating = models.CharField(max_length=10,verbose_name='Give Rating', blank=False, default='')
    oreviewdate = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.review


class Olocationcomment(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    olocation = models.ForeignKey(Olocation, on_delete=models.CASCADE)
    olocationreview = models.ForeignKey(Olocationreview, on_delete=models.CASCADE, default=1)
    comment = models.CharField(max_length=1000, verbose_name='Comment')
    ocommentdate = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.comment



class Elearningreview(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    elearning = models.ForeignKey(Elearning, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000, verbose_name='Write Review', blank=False)
    rating = models.CharField(max_length=10,verbose_name='Give Rating', blank=False, default='')
    lreviewdate = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.review


class Elearningcomment(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    elearning = models.ForeignKey(Elearning, on_delete=models.CASCADE)
    elearningreview = models.ForeignKey(Elearningreview, on_delete=models.CASCADE, default=1)
    comment = models.CharField(max_length=1000, verbose_name='Comment')
    lcommentdate = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.comment