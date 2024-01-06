from django.db import models
from django.contrib.auth.models import User


gender_choice = (("male","male"),("female","female"),("other","other"))


class Talent_user_details(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    guardian_phone = models.CharField(max_length=20, null=True, blank=True)
    personal_whatsapp_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(choices=gender_choice,max_length=20)
    address = models.TextField(max_length=250, null=True, blank=True)
    communication_address = models.TextField(max_length=250, null=True, blank=True)
    headshot = models.ImageField(upload_to='headshotimage/', null=True, blank=True)
    fullbodyshot = models.ImageField(upload_to='fullbodyimage/', null=True, blank=True)
    character_shots = models.ImageField(upload_to='character_images/', null=True, blank=True)
    intro_video = models.FileField(upload_to='videos/', null=True, blank=True)
    current_profession = models.CharField(max_length=100, null=True, blank=True)
    educational_qualification = models.CharField(max_length=50, null=True, blank=True)
    hobbies = models.TextField(max_length=200, null=True, blank=True)
    have_any_acting_experience = models.BooleanField(default=False)
    video_link = models.TextField(max_length=250, null=True, blank=True)
    instagram = models.TextField(max_length=250, null=True, blank=True)
    youtube = models.TextField(max_length=250, null=True, blank=True)
    facebook_id = models.TextField(max_length=250, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    referer_name = models.CharField(max_length=100, null=True, blank=True)
    mail_merge_status = models.BooleanField(default=False, null=True, blank=True)
    task_owner = models.CharField(max_length=200)
    offline_added_time = models.DateTimeField( null=True, blank=True)


class Skills_master(models.Model):
    skill = models.CharField(max_length=100)

class Language_master(models.Model):
    language = models.CharField(max_length=100)


class Talent_user_languages(models.Model):
    talent_user = models.ForeignKey(Talent_user_details, on_delete=models.CASCADE)
    language = models.ManyToManyField(Language_master)   

class Talent_user_skills(models.Model):
    talent_user = models.ForeignKey(Talent_user_details,on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skills_master)

Recruiter_choices = (("freelancer","freelancer"),("company","company"))


class Talent_recruiter_details(models.Model):
    recruiter_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recruiter_name = models.CharField(max_length=100)
    recruiter_phone = models.CharField(max_length=20)
    recruiter_email = models.EmailField()
    freelancer_or_company = models.CharField(choices=Recruiter_choices, max_length=50)

class Project_type_master(models.Model):
    project_type = models.CharField(max_length=200)


class freelance_recruiter_details(models.Model):
    talent_recruiter_id = models.ForeignKey(Talent_recruiter_details,on_delete=models.CASCADE)
    worked_projects = models.TextField(max_length=250)
    offcl_mmbrship_or_assction_rltd_to_film_prdction = models.BooleanField(default=False,help_text="Hold any official membership in a club or association related to any film production")
    membership_name = models.CharField(max_length=200)
    membership_id = models.CharField(max_length=100)
    reference_name = models.CharField(max_length=200)
    reference_contact_no = models.CharField(max_length=20,null=True, blank=True)
    project_name = models.CharField(max_length=200,null=True, blank=True)
    project_type = models.ForeignKey(Project_type_master, on_delete=models.DO_NOTHING,null=True, blank=True)
    project_location = models.CharField(max_length=100,null=True, blank=True)


class company_recruiter_details(models.Model):
    talent_recruiter_id = models.ForeignKey(Talent_recruiter_details, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_reg_no = models.CharField(max_length=100)
    company_address = models.TextField(max_length=200,null=True, blank=True)
    tid = models.CharField(max_length=100, help_text='tax identification number',null=True, blank=True)




