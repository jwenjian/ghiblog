from github import Github
from github.Issue import Issue
from github.Repository import Repository
import os
import time


def test():
    print('hello  circle ci')


def format_issue(issue: Issue):
    return '- [%s](%s)  %s   %s \n' % (
        issue.title, issue.html_url, sup('%s comments' % issue.comments), issue.created_at)


def sup(text: str):
    return '<sup>%s</sup>' % text


def sub(text: str):
    return '<sub>%s</sub>' % text


def save_md_file(contents):
    read_me = open('README.md', 'w')
    read_me.write('updated at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
    read_me.writelines(contents)
    read_me.flush()
    read_me.close()


def list_repos():
    login = os.environ.get('GITHUB_LOGIN')
    password = os.environ.get('GITHUB_PASSWORD')

    for key in os.environ:
        print(key + ':' + os.environ[key])

    u = Github(login, password)
    for repo in u.get_user().get_repos():
        print(repo.name)

    # list issues
    r: Repository = u.get_repo('jwenjian/jwenjian.github.io')
    issues = r.get_issues()

    print(issues.totalCount)

    contents: list = []

    for issue in issues:
        contents.append(format_issue(issue))

    save_md_file(contents)


if __name__ == '__main__':
    test()
    list_repos()
