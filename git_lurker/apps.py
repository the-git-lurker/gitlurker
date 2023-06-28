class GitLurkerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'git_lurker'
    verbose_name = 'Git Lurker'
    fixtures = ['initial_projects.json']