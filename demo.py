from github import Github
from github.Issue import Issue
from github.Repository import Repository
import os
import time

user: Github
ghiblog: Repository
cur_time: str


def format_issue(issue: Issue):
    return '- [%s](%s)  %s  \t :alarm_clock:%s \n' % (
        issue.title, issue.html_url, sup('%s :speech_balloon:' % issue.comments), sub(issue.created_at))


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


def login():
    global user
    username = os.environ.get('GITHUB_LOGIN')
    password = os.environ.get('GITHUB_PASSWORD')
    user = Github(username, password)


def get_ghiblog():
    global ghiblog
    ghiblog = user.get_repo('%s/ghiblog' % user.get_user().login)


def bundle_summary_section():
    global ghiblog
    global cur_time
    global user

    total_label_count = ghiblog.get_labels().totalCount
    total_issue_count = ghiblog.get_issues().totalCount
    labels_html_url = 'https://github.com/%s/ghiblog/labels' % user.get_user().login
    issues_html_url = 'https://github.com/%s/ghiblog/issues' % user.get_user().login

    summary_section = '''
# GitHub Issues Blog :tada::tada::tada:
    
> :alarm_clock: 上次更新: %s
    
共 [%s](%s) 个标签, [%s](%s) 篇博文.
    ''' % (cur_time, total_label_count, labels_html_url, total_issue_count, issues_html_url)

    return summary_section


def bundle_pinned_issues_section():
    global user
    global ghiblog

    pinned_label = ghiblog.get_label(':+1:  置顶')
    pinned_issues = ghiblog.get_issues(labels=(pinned_label,))

    pinned_issues_section = '## 置顶 :thumbsup: \n'

    for issue in pinned_issues:
        pinned_issues_section += format_issue(issue)

    return pinned_issues_section


def execute():
    global cur_time
    # common
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 1. login
    login()

    # 2. get ghiblog
    get_ghiblog()

    # 3. summary section
    summary_section = bundle_summary_section()
    print(summary_section)

    # 4. pinned issues section
    pinned_issues_section = bundle_pinned_issues_section()
    print(pinned_issues_section)

    # 4. get issues

    pass


if __name__ == '__main__':
    execute()
