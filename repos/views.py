import json
import logging
import requests
import time
from json.decoder import JSONDecodeError

from django.http import JsonResponse

from .models import Repository

GITHUB_API_TEMPLATE = 'https://api.github.com/users/{username}/repos?page={page}&per_page={per_page}'
RESULTS_PER_PAGE = 100
LOGGER = logging.getLogger(__name__)


class GitHubException(Exception):
    pass


def get_github_repos(username):
    page = 1
    while True:
        LOGGER.info(f'Fetching page {page} for {username}')
        response = requests.get(GITHUB_API_TEMPLATE.format(username=username,
                                                           page=page,
                                                           per_page=RESULTS_PER_PAGE))
        data = response.json()
        if not response.ok:
            LOGGER.warning(f'Got error while trying to fetch repos for '
                           f'username {username!r}: {data["message"]!r}')
            raise GitHubException(data['message'])
        for repo in data:
            yield repo
        if not data or len(data) < RESULTS_PER_PAGE:
            break
        LOGGER.info('Sleeping for 1s...')
        time.sleep(1)
        page += 1


def repositories(request):
    if request.method == 'POST':
        try:
            username = json.loads(request.body)['username']
            repo_objects = []
            for git_repo in get_github_repos(username):
                if not Repository.objects.filter(html_url=git_repo['html_url']).exists():
                    git_repo['username'] = username
                    repo_objects.append(Repository.from_dict(git_repo))
            LOGGER.info(f'Adding {len(repo_objects)} repositories to database.')
            Repository.objects.bulk_create(repo_objects)
            return JsonResponse({'success': True, 'created_number': len(repo_objects)})
        except GitHubException as e:
            return JsonResponse({'error': f'Got error from GitHub: {str(e)}'}, status=400)
        except (JSONDecodeError, KeyError):
            return JsonResponse({'error': '`username` parameter not found'}, status=400)

    repos = Repository.objects.all()
    repos = [repo.as_dict() for repo in repos]
    return JsonResponse(repos, safe=False)


def repository(request, repo_id):
    try:
        repo = Repository.objects.get(pk=repo_id)
    except Repository.DoesNotExist:
        return JsonResponse({'error': 'Repository does not exist'}, status=404)
    return JsonResponse(repo.as_dict())
