from django.db import models

# Simple model for including projects
class project(models.Model):
    """Projects to Include"""
    repository = models.CharField(max_length=100, default='')
    owner = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return self.repository

# Model for the release basic info
class release(models.Model):
    """Basic release level model"""
    repository = models.ForeignKey(project, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)
    latest_release = models.CharField(max_length=50, default='')
    publisher = models.CharField(max_length=200, default='')
    version = models.CharField(max_length=200, default='')
    notes = models.TextField(default='')

    def __int__(self):
        return self.repository

# Model for the repo basic info
class repo_list(models.Model):
    """Basic repository level model"""
    owner = models.ForeignKey(project, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)
    git_id = models.IntegerField()
    github_url = models.URLField(max_length=200, default='')
    name = models.CharField(max_length=200, default='')
    description = models.TextField(max_length=350, default='')
    last_updated = models.CharField(max_length=50, default='')

    def __int__(self):
        return self.owner      
    
# Model for the contributors basic info
class team(models.Model):
    """Basic contributors level model"""
    owner = models.ForeignKey(project, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)
    avatar_url = models.URLField(max_length=200, default='')
    github_url = models.URLField(max_length=200, default='')
    user_id = models.IntegerField()
    handle = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')

    def __int__(self):
        return self.owner
    
# Model for the repo basic info
class repo_detail(models.Model):
    """Basic repository level model"""
    repository = models.ForeignKey(project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    date_updated = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=350, default='')
    repo_url = models.URLField(max_length=200, default='')
    followers = models.IntegerField()
    forks = models.IntegerField()
    open_issues = models.IntegerField()

    def __int__(self):
        return self.repository

# Model for the contributors basic info
class contrib(models.Model):
    """Basic contributors level model"""
    repository = models.ForeignKey(project, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)
    avatar_url = models.URLField(max_length=200, default='')
    github_url = models.URLField(max_length=200, default='')
    user_id = models.IntegerField()
    handle = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=200, default='')
    contributions = models.IntegerField()

    def __int__(self):
        return self.repository