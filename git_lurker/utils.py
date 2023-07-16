# Import Libraries
import requests, markdown, pytz
from .models import release, project, repo_list, team, repo_detail, contrib
from datetime import datetime

# Time Zone localization to UTC
utc=pytz.UTC

# Get Release Info for Project
def get_release_info(endpoint, ssl, head, repo):
    """
    This function processes the API endpoint data for the latest release of a given project.
    During which it extracts the values for the following keys:
        - ["tag_name"] = the version tag name
        - ["author"]["login"] = the person responsible for publishing this version of the software
        - ["published_at"] = the date/time when the release 
        - ["body"] = the content of the release notes.
    """
    # Retrive response data through GitHub API
    response = requests.get(endpoint, headers=head, verify=ssl)
    # If a good response then process as JSON and populate DB
    if response.status_code == 200:
        releases = response.json()
        if len(releases) > 0:
            version = releases["tag_name"]
            publisher = releases["author"]["login"]
            latest_release = releases["published_at"]
            git_id = releases["id"]
            # Specifically convert release body text from markdown to HTML so that it can be formatted when rendered
            notes = markdown.markdown(releases["body"])
            if notes == "":
                notes = '<p> No Release Notes Provided. </p>'
            release_data = {"version":version, "publisher":publisher, "latest_release":latest_release, "notes":notes, "git_id":git_id}
            # Uses the GitHub ID to check if we already have a record.
            # If we don't we create a DB record, if we do we update the record
            # date_updated force changed to as the DB record is updated.
            release_obj =  release.objects.filter(git_id=git_id)
            if not release_obj:
                release.objects.create(repository=proj[0], latest_release=latest_release, publisher=publisher, version=version, notes=notes, git_id=git_id)
            else:
                release_obj.update(date_updated=utc.localize(datetime.now()) , latest_release=latest_release, publisher=publisher, version=version, notes=notes, git_id=git_id)
            return release_data
    return None

# Get Repo List info for Project
def get_repo_info(endpoint, endpoint_usr, ssl, head, proj_owner):
    """
    This function processes the API endpoint data for a bunch of repos assoicated with a given organization or user.
    During which it extracts the values for the following keys:
        - ["name"]= the name of the repository
        - ["description"] = the description for the repository
        - ["html_url"] = the URL for the repository
        - ["updated_at"] = the date/time when the repository was last updated 
        - ["id"] = the GitHub ID variable for the repository
    """
    # Retrive response data through GitHub API first as ORG then as USER
    response_org = requests.get(endpoint, headers=head, verify=ssl)
    response_usr = requests.get(endpoint_usr, headers=head, verify=ssl)
    # Check if a good response as an ORG, if not then assume USER API data
    if response_org.status_code == 200:
        response = response_org
    else:
        response = response_usr
    # If a good response then process as JSON and populate DB
    if response.status_code == 200:
        repos = []
        update_list = []
        # Loop over each repo separately and add to list
        for repo in response.json():
            name = repo["name"]
            description = repo["description"]
            if description == None:
                description = "NONE REPORTED"
            github_url = repo["html_url"]
            last_updated = repo["updated_at"]
            git_id = repo["id"]
            repos.append({"name":name, "description":description, "github_url":github_url, "last_updated":last_updated, "git_id":git_id})

            # Uses the GitHub ID variable to check if we already have a record.
            # This is useful in case the repo changed name as it keeps the ID
            # If we don't we create a DB record, if we do we update the record
            # date_updated force changed to as the DB record is updated.
            repo_list_obj = repo_list.objects.filter(git_id=git_id)
            if not repo_list_obj:
                repo_list.objects.create(owner=proj_owner[0], git_id=git_id, github_url=github_url, name=name, description=description, last_updated=last_updated)
            else:
                repo_list_obj.update(date_updated=utc.localize(datetime.now()) , github_url=github_url, name=name, description=description, last_updated=last_updated)
            # Create a list of GitHub IDs so that we can compare the current list against the DB list.
            update_list.append(git_id)

        # Get the final current list from the DB and compare against the recently updated list.
        # For any users in the current DB but not found in the latest API pull delete the records.
        if len(update_list)>0:
            current_db_list = [each['git_id'] for each in repo_list.objects.filter(owner=proj_owner[0]).values()]
            for each_id in current_db_list:
                if each_id not in update_list:
                    repo_list.objects.filter(user_id=each_id).delete()
                    print("Deleted old data from DB")
        
        # Sort the data in alphbetical order based on name 
        sorted_repos = sorted(repos, key=lambda x: x['name'].lower())
        return sorted_repos
    return None

# Get project Members
def get_members(endpoint, ssl, head, proj_owner):
    """
    This function processes the API endpoint data for member of a given organisation (if any).
    During which it extracts the values for the following keys:
        - ["login"] = the GitHub handle of the user
        - ["avatar_url"] = the user's avatar image
        - ["html_url"] = the URL for the user on GitHub
        - ["url"] = the API endpoint for the user's profile (to access the name key)
        - ["id"] = the GitHub ID variable for the user
        - ["name"] = the user's name (if provided, otherwise "anon")
    """
    # Retrive response data through GitHub API
    response = requests.get(endpoint, headers=head, verify=ssl)
    # If a good response then process as JSON and populate DB
    if response.status_code == 200:
        members = []
        update_list = []
        for member in response.json():
            handle = member["login"]
            github_url = member["html_url"]
            avatar_url = member["avatar_url"]
            api = member["url"]
            user_id = member["id"]
            # User specific API endpoint pulled form json and used
            # This will try to retrive Name data from their GitHub page
            response_u = requests.get(api, headers=head, verify=ssl)
            if response_u.status_code == 200:
                resp = response_u.json()
                name = resp["name"]
                if name == None:
                    name = "anon"
            else:
                name = "None"
            members.append({"handle":handle, "name":name, "github":github_url, "avatar":avatar_url})

            # Uses the GitHub ID variable to check if we already have a record.
            # If we don't we create a DB record, if we do we update the record
            # date_updated force changed to as the DB record is updated.
            team_obj = team.objects.filter(owner=proj_owner[0], user_id=user_id)
            if not team_obj:
                team.objects.create(owner=proj_owner[0], user_id=user_id, github_url=github_url, avatar_url=avatar_url, name=name, handle=handle)
            else:
                team_obj.update(date_updated=utc.localize(datetime.now()) , github_url=github_url, avatar_url=avatar_url, name=name, handle=handle)

            update_list.append(user_id)
        
        # Get the final current list from the DB and compare against the recently updated list.
        # For any users in the current DB but not found in the latest API pull delete the records.
        if len(update_list)>0:
            current_db_list = [each['user_id'] for each in team.objects.filter(owner=proj_owner[0]).values()]
            for each_id in current_db_list:
                if each_id not in update_list:
                    team.objects.filter(user_id=each_id).delete()
                    print("Deleted old data from DB")

        # Sort the data in alphbetical order based on handle 
        sorted_members = sorted(members, key=lambda x: x['handle'].lower())
        return sorted_members
    return None

# Get Repo summary info
def get_repo_summary(endpoint, ssl, head, rep_id):
    """
    This function processes the API endpoint for a given repository.
    During which it extracts the values for the following keys:
        - ["full_name"] = the name of the repository
        - ["description"] = the description of the repository
        - ["html_url"] = the URL for the repository
        - ["subscribers_count"] = the number of subscribers for a repository
        - ["forks"] = the number of forks of a repository
        - ["open_issues"] = the number of open issues on a repository)
    """
    # Retrive response data through GitHub API
    response = requests.get(endpoint, headers=head, verify=ssl)
    # If a good response then process as JSON and populate DB
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
        # Uses the repository to check if we already have a record.
        # If we don't we create a DB record, if we do we update the record
        # date_updated force changed to as the DB record is updated.
        repo_obj = repo_detail.objects.filter(repository=rep_id)
        if not repo_obj:
            repo_detail.objects.create(repository=rep_id, name=name, description=description, repo_url=repo_url, followers=followers, forks=forks, open_issues=open_issues)
        else:
            repo_obj.update(date_updated=utc.localize(datetime.now()) ,repository=rep_id, name=name, description=description, repo_url=repo_url, followers=followers, forks=forks, open_issues=open_issues)
        return summary
    return None

# Get project contributors
def get_contributors(endpoint, ssl, head, rep_id):
    """
    This function processes the API endpoint of contributors for a given repository 
    During which it extracts the values for the following keys:
        - ["login"] = the handle of the contributor
        - ["avatar_url"] = the contributor's avatar image
        - ["html_url"] = the URL for the contributor on GitHub
        - ["url"] = the API endpoint for the contributor's profile (to access the name key)
        - ["id"] = the GitHub ID variable for the contributor
        - ["contributions"] = the number of contibutions they have made to the repository
        - ["name"] = the contributor's name (if provided, otherwise "anon")
    """
    # Retrive response data through GitHub API
    response = requests.get(endpoint, headers=head, verify=ssl)
    # If a good response then process as JSON and populate DB
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
            # User specific API endpoint pulled form json and used
            # This will try to retrive Name data from their GitHub page
            response_u = requests.get(api, headers=head, verify=ssl)
            if response_u.status_code == 200:
                resp = response_u.json()
                name = resp["name"]
                if name == None:
                    name = "anon"
            else:
                name = "None"
            contributors.append({"user_id":user_id, "handle":handle, "name":name, "github_url":github_url, "avatar_url":avatar_url, "contributions":contributions})

            # Uses the GitHub ID variable to check if we already have a record.
            # If we don't we create a DB record, if we do we update the record
            # date_updated force changed to as the DB record is updated.
            contrib_obj = contrib.objects.filter(repository=rep_id, user_id=user_id)
            if not contrib_obj:
                contrib.objects.create(repository=rep_id, user_id=user_id, github_url=github_url, avatar_url=avatar_url, name=name, handle=handle, contributions=contributions)
            else:
                contrib_obj.update(date_updated=utc.localize(datetime.now()) , github_url=github_url, avatar_url=avatar_url, name=name, handle=handle, contributions=contributions)
            
            update_list.append(user_id)

        # Get the final current list from the DB and compare against the recently updated list.
        # For any users in the current DB but not found in the latest API pull delete the records.
        if len(update_list)>0:
            current_db_list = [each['user_id'] for each in contrib.objects.filter(repository=rep_id).values()]
            for each_id in current_db_list:
                if each_id not in update_list:
                    contrib.objects.filter(user_id=each_id).delete()
                    print("Deleted old data from DB")

        # Sort the data in descending order of contributions  
        sorted_contributors = sorted(contributors, key=lambda x: x['contributions'], reverse=True)
        return sorted_contributors
    return None