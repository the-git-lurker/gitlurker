from django.shortcuts import render,redirect
from .utils import get_release_info, get_members, get_repo_info, get_contributors, get_repo_summary
from datetime import date, datetime, timedelta
import pytz, os
from .models import project, release, repo_list, team, repo_detail, contrib

# Time Zone localization to UTC
utc=pytz.UTC

# API call variables
verify_ssl = True

# Auth token env variable
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization" : f"Token {AUTH_TOKEN}"
        }

# Handle any pages that are unexpected
def handle_unrecognized_url(request, unrecognized_url):
    # Redirect to a specific page or display a custom error message
    return redirect('index')  # Example: Redirect to the home page

# Home view
def index(request):
    """Summary view. This fetches the latest release information about the projects."""
    project_list = project.objects.values()
    
    projects_data = [] 
    for p in project_list:
        owner = p["owner"]
        repo = p["repository"]
        rep_id = p["id"]
        release_data = release.objects.filter(repository=rep_id).values()

        # Check if the release data in the DB is recent. If not update via the GitHub APIs.
        if not release_data or release_data[0]["date_updated"] <= utc.localize(datetime.now()) - timedelta(hours=12):
            endpoint1 = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            release_data_api = get_release_info(endpoint1, verify_ssl, headers, repo)
            version = release_data_api["version"]
            publisher = release_data_api["publisher"]
            latest_release = release_data_api["latest_release"]
            notes = release_data_api["notes"]
        else:
            version = release_data[0]["version"]
            publisher = release_data[0]["publisher"]
            latest_release = release_data[0]["latest_release"]
            notes = release_data[0]["notes"]
        
        date_only = latest_release[:10]
        numdate = date.fromisoformat(date_only)
        cutoff = date.fromordinal(date.today().toordinal()-7)
        if numdate >= cutoff:
            recent = "Y"
        else:
            recent = "N"

        if not version and not publisher and not latest_release:
            projects_data.append({})
        else: 
            projects_data.append({"version":version, "latest_release":latest_release, "publisher":publisher, "owner":owner, "repo":repo, "recent":recent, "notes":notes})#
        projects_data_sorted = sorted(projects_data, key=lambda x: (x['latest_release']), reverse=True)
    
    date_updated = release.objects.values().last()["date_updated"]
    date_updated_str = f"{date_updated}"
    latest_pull = f"Data updated on: {date_updated_str[:16]} UTC"

    return render(request, "git_lurker/index.html", context={"projects":projects_data_sorted, "latest_pull":latest_pull})

# Support page
def support_view(request):
    """Support page view"""
    context = {}
    return render(request, 'git_lurker/support.html', context) 

# Release view
def release_view(request, owner, repo):
    """Release view"""
    project_data = project.objects.filter(owner=owner, repository=repo)
    if len(project_data) > 0:
        rep_id = project_data[0]
        release_data = release.objects.filter(repository=rep_id).values()

        # Check if the release data in the DB is recent. If not update via the GitHub APIs.
        if not release_data or release_data[0]["date_updated"] <= utc.localize(datetime.now()) - timedelta(hours=12):
            endpoint1 = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            release_data = get_release_info(endpoint1, verify_ssl, headers, repo)
        else:
            release_data = release_data[0]

        if not release_data:
            release_data = "NOT REPORTED"

        date_updated = release.objects.values().last()["date_updated"]
        date_updated_str = f"{date_updated}"
        latest_pull = f"Data updated on: {date_updated_str[:16]} UTC"
        return render(request, "git_lurker/release.html", context={"release":release_data, "owner":owner, "repo":repo, "release_url":f"https://github.com/{owner}/{repo}/releases", "latest_pull":latest_pull})
    else:
        return redirect("index")

# Project Repository List view
def project_view(request, owner):
    """Project Repository List view"""
    proj_owner = project.objects.filter(owner=owner)
    if len(proj_owner) > 0:
        repos_data = repo_list.objects.filter(owner=proj_owner[0])
        teams_data = team.objects.filter(owner=proj_owner[0])

        # Repository List: Check if the release data in the DB is recent. If not update via the GitHub APIs.
        if not repos_data or repos_data.values().first()["date_updated"] <= utc.localize(datetime.now()) - timedelta(hours=12):
            endpoint1 = f"https://api.github.com/orgs/{owner}/repos"
            endpoint1_usr = f"https://api.github.com/users/{owner}/repos"
            repos = get_repo_info(endpoint1, endpoint1_usr, verify_ssl, headers, proj_owner)
        else:
            repos_unsorted = []
            for repo in repos_data.values():
                name = repo["name"]
                description = repo["description"]
                github_url = repo["github_url"]
                last_updated = repo["last_updated"]
                git_id = repo["git_id"]
                repos_unsorted.append({"name":name, "description":description, "github_url":github_url, "last_updated":last_updated, "git_id":git_id})
            repos = sorted(repos_unsorted, key=lambda x: x['name'].lower())

        # Repository List: Check if the release data in the DB is recent. If not update via the GitHub APIs.
        if not teams_data or teams_data.values().first()["date_updated"] <= utc.localize(datetime.now()) - timedelta(hours=12):
            endpoint2 = f"https://api.github.com/orgs/{owner}/public_members"
            members = get_members(endpoint2, verify_ssl, headers, proj_owner)
        else:
            members_unsorted = []
            for member in teams_data.values():
                handle = member["handle"]
                github_url = member["github_url"]
                avatar_url = member["avatar_url"]
                name = member["name"]
                members_unsorted.append({"handle":handle, "name":name, "github":github_url, "avatar":avatar_url})
            members = sorted(members_unsorted, key=lambda x: x['handle'].lower())
        
        if not members and not repos:
            members = "NONE REPORTED"
            repos = "NONE REPORTED"
        
        if not members:
            members = "NONE REPORTED"
        owner_url = f"https://github.com/{owner}"

        date_updated = repos_data.values().last()["date_updated"]
        date_updated_str = f"{date_updated}"
        latest_pull = f"Data updated on: {date_updated_str[:16]} UTC"

        return render(request, "git_lurker/project.html", context={"owner":owner, "team_members":members, "repos": repos, "owner_url":owner_url, "latest_pull":latest_pull})
    else:
        return redirect("index")


# Repository view
def repository_view(request, owner, repo):
    """Repository view"""
    project_data = project.objects.filter(owner=owner, repository=repo)
    if len(project_data) > 0:
        rep_id = project_data[0]
        repository_data = repo_detail.objects.filter(repository=rep_id).values()
        contrib_data = contrib.objects.filter(repository=rep_id).values()

        # Check if the Repo Summary data in the DB is recent. If not update via the GitHub APIs.
        if not repository_data or repository_data[0]["date_updated"] <= utc.localize(datetime.now()) - timedelta(hours=12):
            endpoint1 = f"https://api.github.com/repos/{owner}/{repo}"
            summary = get_repo_summary(endpoint1, verify_ssl, headers, rep_id)
        else:
            summary = repository_data[0]
        
        # Repository List: Check if the release data in the DB is recent. If not update via the GitHub APIs.
        if not contrib_data or contrib_data.values().first()["date_updated"] <= utc.localize(datetime.now()) - timedelta(hours=12):
            endpoint2 = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=50"
            contribs = get_contributors(endpoint2, verify_ssl, headers, rep_id)
        else:
            contrib_unsorted = []
            for contributor in contrib_data.values():
                handle = contributor["handle"]
                github_url = contributor["github_url"]
                avatar_url = contributor["avatar_url"]
                user_id = contributor["user_id"]
                name = contributor["name"]
                contributions = contributor["contributions"]
                contrib_unsorted.append({"name":name, "handle":handle, "github_url":github_url, "avatar_url":avatar_url, "user_id":user_id, "contributions":contributions})
            contribs = sorted(contrib_unsorted, key=lambda x: x['contributions'], reverse=True)

        if not contribs:
            contribs = "NONE"

        date_updated = repository_data.last()["date_updated"]
        date_updated_str = f"{date_updated}"
        latest_pull = f"Data updated on: {date_updated_str[:16]} UTC"
        return render(request, "git_lurker/repository.html", context={"owner":owner, "contribs":contribs, "repo": repo, "summary":summary, "latest_pull":latest_pull})
    else:
        return redirect("index")