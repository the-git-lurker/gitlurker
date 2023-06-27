# Import Libraries
import requests, markdown, pytz
from .models import release, project, repo_list, team, repo_detail, contrib
from datetime import datetime

# Time Zone localization to UTC
utc=pytz.UTC

# Get Release Info for Project
def get_release_info(endpoint, ssl, head, repo):
    response = requests.get(endpoint, headers=head, verify=ssl)
    
    if response.status_code == 200:
        releases = response.json()
        if len(releases) > 0:
            version = releases["tag_name"]
            publisher = releases["author"]["login"]
            latest_release = releases["published_at"]
            notes = markdown.markdown(releases["body"])
            if notes == "":
                notes = '<p> No Release Notes Provided. </p>'
            release_data = {"version":version, "publisher":publisher, "latest_release":latest_release, "notes":notes}
            proj = project.objects.filter(repository=repo)
            release.objects.update_or_create(repository=proj[0], latest_release=latest_release, publisher=publisher, version=version, notes=notes)
            return release_data
    return None

# Get Repo List info for Project
def get_repo_info(endpoint, ssl, head, proj_owner):
    response = requests.get(endpoint, headers=head, verify=ssl)
    if response.status_code == 200:
        repos = []
        update_list = []
        for repo in response.json():
            name = repo["name"]
            description = repo["description"]
            if description == None:
                description = "NONE REPORTED"
            github_url = repo["html_url"]
            last_updated = repo["updated_at"]
            git_id = repo["id"]
            repos.append({"name":name, "description":description, "github_url":github_url, "last_updated":last_updated, "git_id":git_id})

            repo_list_obj = repo_list.objects.filter(git_id=git_id)
            if not repo_list_obj:
                repo_list.objects.create(owner=proj_owner[0], git_id=git_id, github_url=github_url, name=name, description=description, last_updated=last_updated)
            else:
                repo_list.objects.filter(git_id=git_id).update(date_updated=utc.localize(datetime.now()) , github_url=github_url, name=name, description=description, last_updated=last_updated)
            
            update_list.append(git_id)

        # Get the final current list from the DB and compare against the recently updated list.
        # For any users in the current DB but not found in the latest API pull delete the records.
        if len(update_list)>0:
            current_db_list = [each['git_id'] for each in repo_list.objects.filter(owner=proj_owner[0]).values()]
            for each_id in current_db_list:
                if each_id not in update_list:
                    repo_list.objects.filter(user_id=each_id).delete()
                    print("Deleted old data from DB")
        
        sorted_repos = sorted(repos, key=lambda x: x['name'].lower())
        return sorted_repos
    return None

# Get project Members
def get_members(endpoint, ssl, head, proj_owner):
    response = requests.get(endpoint, headers=head, verify=ssl)
    if response.status_code == 200:
        members = []
        update_list = []
        for member in response.json():
            handle = member["login"]
            github_url = member["html_url"]
            avatar_url = member["avatar_url"]
            api = member["url"]
            user_id = member["id"]
            response_u = requests.get(api, headers=head, verify=ssl)
            if response_u.status_code == 200:
                resp = response_u.json()
                name = resp["name"]
                if name == None:
                    name = "anon"
            else:
                name = "None"
            members.append({"handle":handle, "name":name, "github":github_url, "avatar":avatar_url})

            team_obj = team.objects.filter(user_id=user_id)
    
            if not team_obj:
                team.objects.create(owner=proj_owner[0], user_id=user_id, github_url=github_url, avatar_url=avatar_url, name=name, handle=handle)
            else:
                team.objects.filter(user_id=user_id).update(date_updated=utc.localize(datetime.now()) , github_url=github_url, avatar_url=avatar_url, name=name, handle=handle)

            update_list.append(user_id)
        
        # Get the final current list from the DB and compare against the recently updated list.
        # For any users in the current DB but not found in the latest API pull delete the records.
        if len(update_list)>0:
            current_db_list = [each['user_id'] for each in team.objects.filter(owner=proj_owner[0]).values()]
            for each_id in current_db_list:
                if each_id not in update_list:
                    team.objects.filter(user_id=each_id).delete()
                    print("Deleted old data from DB")

        sorted_members = sorted(members, key=lambda x: x['handle'].lower())
        return sorted_members
    return None

# Get Repo summary info
def get_repo_summary(endpoint, ssl, head, rep_id):
    
    response = requests.get(endpoint, headers=head, verify=ssl)
    if response.status_code == 200:
        info = response.json()
        name = info["full_name"]
        repo_url = info["html_url"]
        description = info["description"]
        if description == None:
            description = "NONE REPORTED"
        followers = info["subscribers_count"]
        forks = info["forks"]
        open_issues = info["open_issues"]
        summary = {"name":name, "repo_url":repo_url, "description":description, "followers":followers, "forks":forks, "open_issues":open_issues}
        repo_detail.objects.update_or_create(repository=rep_id, name=name, description=description, repo_url=repo_url, followers=followers, forks=forks, open_issues=open_issues)
        return summary
    return None

# Get project contributors
def get_contributors(endpoint, ssl, head, rep_id):
    response = requests.get(endpoint, headers=head, verify=ssl)
    if response.status_code == 200:
        contributors = []
        update_list = []
        for contributor in response.json():
            handle = contributor["login"]
            github_url = contributor["html_url"]
            avatar_url = contributor["avatar_url"]
            user_id = contributor["id"]
            contributions = contributor["contributions"]
            api = contributor["url"]
            response_u = requests.get(api, headers=head, verify=ssl)
            if response_u.status_code == 200:
                resp = response_u.json()
                name = resp["name"]
                if name == None:
                    name = "anon"
            else:
                name = "None"
            contributors.append({"user_id":user_id, "handle":handle, "name":name, "github_url":github_url, "avatar_url":avatar_url, "contributions":contributions})

            contrib_obj = contrib.objects.filter(user_id=user_id)
            if not contrib_obj:
                contrib.objects.create(repository=rep_id, user_id=user_id, github_url=github_url, avatar_url=avatar_url, name=name, handle=handle, contributions=contributions)
            else:
                contrib.objects.filter(user_id=user_id).update(date_updated=utc.localize(datetime.now()) , github_url=github_url, avatar_url=avatar_url, name=name, handle=handle, contributions=contributions)
            
            update_list.append(user_id)

        # Get the final current list from the DB and compare against the recently updated list.
        # For any users in the current DB but not found in the latest API pull delete the records.
        if len(update_list)>0:
            current_db_list = [each['user_id'] for each in contrib.objects.filter(repository=rep_id).values()]
            for each_id in current_db_list:
                if each_id not in update_list:
                    contrib.objects.filter(user_id=each_id).delete()
                    print("Deleted old data from DB")

        sorted_contributors = sorted(contributors, key=lambda x: x['contributions'], reverse=True)
        return sorted_contributors
    return None