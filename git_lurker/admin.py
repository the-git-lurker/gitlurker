from django.contrib import admin
from .models import project, release, repo_detail, contrib, repo_list, team, note_event

admin.site.register(project)
admin.site.register(release)
admin.site.register(repo_detail)
admin.site.register(contrib)
admin.site.register(repo_list)
admin.site.register(team)
admin.site.register(note_event)