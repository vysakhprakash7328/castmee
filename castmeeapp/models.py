from django.db import models
from django.contrib.auth.models import User
import os


gender_choice = (("male","male"),("female","female"),("other","other"))

class State(models.Model):
    name = models.CharField(
        max_length = 20,null=True,blank=True
    )
    def __str__(self) -> str:
        return self.name


class District(models.Model):
    name = models.CharField(
        max_length = 20,null=True,blank=True
    )
    state = models.ForeignKey(
        State,on_delete=models.CASCADE
    )
    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(
        max_length = 20,null=True,blank=True
    )
    state = models.ForeignKey(
        State,on_delete=models.CASCADE
    )
    def __str__(self) -> str:
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self) -> str:
        return self.name


class Skills(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class ConsiderMe(models.Model):
    name = models.CharField(
        max_length = 20,null=True,blank=True
    )
    def __str__(self) -> str:
        return self.name


class AvailableFor(models.Model):
    name = models.CharField(
        max_length=20,null=True,blank=True
    )
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "AvailableFor"


class PreferredFormat(models.Model):
    name = models.CharField(
        max_length=30, null=True, blank=True
    )
    def __str__(self) -> str:
        return self.name


class PreferredGene(models.Model):
    name = models.CharField(
        max_length=30, null=True, blank=True
    )
    def __str__(self) -> str:
        return self.name


class Interest(models.Model):
    name = models.CharField(
        max_length=30, null=True, blank=True
    )
    def __str__(self) -> str:
        return self.name


class ProjectType(models.Model):
    name = models.CharField(
        max_length=30, null=True, blank=True
    )
    def __str__(self) -> str:
        return self.name


class HairType(models.Model):
    name = models.CharField(
        max_length=30, null=True, blank=True
    )
    def __str__(self) -> str:
        return self.name


class HairColour(models.Model):
    name = models.CharField(
        max_length=30, null=True, blank=True
    )
    def __str__(self) -> str:
        return self.name


class BodyType(models.Model):
    name = models.CharField(
        max_length=30, null=True, blank=True
    )
    def __str__(self) -> str:
        return self.name


class EyeColor(models.Model):
    name = models.CharField(
        max_length=30, null=True, blank=True
    )
    def __str__(self) -> str:
        return self.name


class SkinColour(models.Model):
    name = models.CharField(
        max_length=30, null=True, blank=True
    )
    def __str__(self) -> str:
        return self.name


class Artist(models.Model):
    user = models.OneToOneField(
        User,on_delete = models.CASCADE
    )
    phone = models.CharField(
        max_length = 12,null =True,blank =True
    )
    gender = models.CharField(
        choices=gender_choice,max_length=12
    )
    looking_for_work = models.CharField(
        max_length =3,null=True,blank=True,
        choices = (("yes",'yes'),('no','no'))
    )
    date_of_birth = models.DateField(
        null=True,blank=True
    )
    verified = models.CharField(
        max_length=10,default = 'pending',
        null=True,blank=True
    )
    created_time = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self) -> str:
        return self.user.first_name

def get_headshot_directry(instance,filename):
    instance_directry = instance.artist.user.username
    return os.path.join(instance_directry+'/headshot/',filename)


def get_bodyshot_directry(instance,filename):
    instance_directry = instance.artist.user.username
    return os.path.join(instance_directry+'/bodyshot/',filename)

def get_left_profile_directry(instance,filename):
    instance_directry = instance.artist.user.username
    return os.path.join(instance_directry+'/left_profile/',filename)


def get_right_profile_directry(instance,filename):
    instance_directry = instance.artist.user.username
    return os.path.join(instance_directry+'/right_profile/',filename)


def get_video_directry(instance,filename):
    instance_directry = instance.artist.user.username
    return os.path.join(instance_directry+'/video/',filename)


class ArtistExtended(models.Model):
    CHOICES = [
        ('yes', 'yes'),
        ('no', 'no'),
    ]
    artist = models.OneToOneField(
        Artist, on_delete=models.CASCADE
    )
    age = models.IntegerField(
        null=True,blank=True
    )
    bio = models.TextField(
        null=True,blank = True
    )
    height = models.IntegerField(
        null=True,blank = True,
        verbose_name = 'height in cm'
    )
    weight = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=True,blank=True
    )
    hair_type = models.ForeignKey(
        HairType,on_delete=models.DO_NOTHING,
        null=True,blank=True
    )
    hair_color = models.ForeignKey(
        HairColour,on_delete=models.DO_NOTHING,
        null=True,blank=True
    )
    body_type = models.ForeignKey(
        BodyType,on_delete=models.DO_NOTHING,
        null=True,blank=True
    )
    eye_color = models.ForeignKey(
        EyeColor,on_delete=models.DO_NOTHING,
        null=True,blank=True
    )
    skin_color = models.ForeignKey(
        SkinColour,on_delete=models.DO_NOTHING,
        null=True,blank=True
    )
    current_state = models.ForeignKey(
        State,on_delete = models.CASCADE,
        null=True,blank=True,
        related_name = 'current_state_set'
    )
    current_city = models.ForeignKey(
        City,on_delete = models.CASCADE,
        null=True,blank=True,
        related_name = 'current_city_set'
    )
    native_state = models.ForeignKey(
        State,on_delete = models.CASCADE,
        null=True,blank=True,
        related_name = 'native_state_set'
    )
    native_city = models.ForeignKey(
        City,on_delete = models.CASCADE,
        null=True,blank=True,
        related_name = 'native_city_set'
    )
    languages_known = models.ManyToManyField(
        Language
    )
    skills = models.ManyToManyField(
        Skills
    )
    address = models.TextField(
        null=True,blank=True
    )
    headshot_image = models.ImageField(
        upload_to=get_headshot_directry, 
        null=True, blank=True
    )
    fullbodyshot_image = models.ImageField(
        upload_to=get_bodyshot_directry, 
        null=True, blank=True
    )
    left_profile = models.ImageField(
        upload_to=get_left_profile_directry, 
        null=True,blank=True
    )
    right_profile = models.ImageField(
        upload_to=get_right_profile_directry,
        null=True,blank=True
    )
    video = models.FileField(
        upload_to=get_video_directry, null=True, blank=True
    )
    instagram = models.CharField(
        max_length=250, null=True, blank=True
    )
    facebook = models.CharField(
        max_length=250, null=True, blank=True
    )
    twitter = models.CharField(
        max_length=250, null=True, blank=True
    )
    linkedin = models.CharField(
        max_length=250, null=True, blank=True
    )
    youtube = models.CharField(
        max_length=250, null=True, blank=True
    )
    consider_me_for = models.ManyToManyField(
        ConsiderMe
    )
    available_for = models.ManyToManyField(
        AvailableFor
    )
    preferred_format = models.ManyToManyField(
        PreferredFormat
    )
    preferred_genre=models.ManyToManyField(
        PreferredGene
    )
    interest = models.ManyToManyField(
        Interest
    )
    smoking_on_screen = models.CharField(
        max_length=3, choices=CHOICES, default='no'
    )
    swimming_on_screen = models.CharField(
        max_length=3, choices=CHOICES, default='no'
    )
    two_wheeler_driving = models.CharField(
        max_length=3, choices=CHOICES, default='no'
    )
    four_wheeler_driving = models.CharField(
        max_length=3, choices=CHOICES, default='no')
    kissing_on_screen = models.CharField(
        max_length=3, choices=CHOICES, default='no'
    )
    intimate_scenes = models.CharField(
        max_length=3, choices=CHOICES, default='no'
    )
    nudity_on_screen = models.CharField(
        max_length=3, choices=CHOICES, default='no'
    )


def get_project_directry(instance,filename):
    instance_directry = instance.artist.user.username
    return os.path.join(instance_directry+'/project/',filename)




class ArtistWorkExperience(models.Model):
    ROLES =(
        ('Lead','Lead'),
        ('Supporting','Supporting'),
        ('Mid Level','Mid Level'),
    )
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE
    )
    project_type = models.ForeignKey(
        ProjectType, on_delete = models.CASCADE,
        null=True, blank=True
    )
    role = models.CharField(
        choices=ROLES,max_length = 20,
        null=True,blank=True
    )
    project_name = models.CharField(
        max_length=100,null=True,blank=True
    )
    project_link = models.CharField(
        max_length = 255,null=True,blank=True
    )
    image=models.ImageField(
        upload_to=get_project_directry, 
        null=True,blank=True
    )


class Producer(models.Model):
    ROLE_CHOICES = [
        ('channel', 'channel'),
        ('production house', 'production House'),
        ('casting agency', 'casting agency'),
        ('other', 'other'),
    ]
    user = models.OneToOneField(
        User,on_delete = models.CASCADE
    )
    company_name = models.CharField(
        max_length =100,null=True,blank=True
    )
    producer_type = models.CharField(
        max_length = 25,choices=ROLE_CHOICES,
        null=True,blank=True
    )
    phone = models.CharField(
        max_length = 12,null=True,blank=True
    )
    verified = models.CharField(
        max_length=10,default = 'pending',
        null=True,blank=True
    )
    created_time = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self) -> str:
        return self.user.first_name


class ProducerExtended(models.Model):
    producer = models.OneToOneField(
        Producer, on_delete=models.CASCADE
    )
    offcl_mmbrship_or_assction_rltd_to_film_prdction = models.BooleanField(
        default=False,help_text="Hold any official membership in a club or \
              association related to any film production"
    )
    membership_name = models.CharField(
        max_length=200,null=True,blank=True
    )
    membership_id = models.CharField(
        max_length=200,null=True,blank=True
    )
    reference_name = models.CharField(
        max_length=200,null=True,blank=True
    )
    reference_contact_no = models.CharField(
        max_length=20,null=True, blank=True
    )
    company_name = models.CharField(
        max_length=200,null=True,blank=True
    )
    company_reg_no=models.CharField(
        max_length=200,null=True,blank=True
    )
    company_address = models.TextField(
        null=True, blank=True
    )
    tid = models.CharField(
        max_length=100, help_text='tax identification number',
        null=True, blank=True
    )
    def __str__(self) -> str:
        return self.producer.user.username


def get_file_directry(instance,filename):
    instance_directry = instance.producer.user.username
    return os.path.join(instance_directry+'/files/',filename)


class ProducerExperience(models.Model):
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE
    )
    project_name = models.CharField(
        max_length=200,null=True, blank=True
    )
    project_type = models.ForeignKey(
        ProjectType, on_delete=models.CASCADE,
        null=True, blank=True
    )
    project_location = models.CharField(
        max_length=100,null=True, blank=True
    )
    file=models.FileField(
        upload_to=get_file_directry, 
        null=True,blank=True
    )
    def __str__(self) -> str:
        return self.producer.user.username
