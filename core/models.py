from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    
    USER_ROLES = [
        ('admin', 'Administrator'),
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='job_seeker')
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
class Seeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    contcact_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length = 200, blank = True)
    city = models.CharField(max_length = 100, blank = True)
    about_me = models.TextField(blank=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
        # return f"Seeker: {self.profile.user.username}"

class Skill(moodels.Models):
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.CharField(
        max_length = 30,
        choices = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default = 'beginner'
    )

    def __str__(self):
        return f"{self.skill_name} ({self.seeker.full_name})"
    

class Expeprience(models.Models):
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150)
    position_title = models.CharField(max_length = 100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position_title} at {self.company_name}"
    

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    company_name = modelsCharField(max_length = 20)
    industry = models.CharField(max_length = 100, blank = True)
    company_email = models.EmailField(blank=True)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name
    

class JobPost(models.Model):
    emloymemt_type = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=150)
    job_description = models.TextField()
    location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=emloymemt_type)
    salary_range = models.CharField(max_length=100, blank=True)
    requirements = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')

    def __str__(self):
        return self.job_title
    

class SkillRequired(models.Models):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    importance_level = models.CharField(
        max_length = 20,
        choices = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default = 'medium'
    )

    def __str__(self):
        return f"{self.skill_name} - {self.job.job_title}"
    

class Application(models.Models):
    status_choices = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.seeker.full_name} → {self.job.job_title}"
    

class Match(models.Models):
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    match_score = models.DecimalField(max_digits=5, decimal_places=2)
    date_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seeker.full_name} - {self.match_score}%"
    

class Report(model.Models):
    report_type_choices = [
        ('job listings', 'Job Listings'),
        ('applicant statistics', 'Applicant Statistics'),
        ('system hires', 'System Hires'),
    ]
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50, choices=report_type_choices)
    date_generated = models.DateTimeField(auto_now_add = True)
    summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.report_type} by {self.generated_by.username}"
    

class Message(models.Models):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.reciever.username}"
    
