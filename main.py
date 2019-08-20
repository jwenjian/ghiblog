#!/usr/bin/python
# -*- coding: utf-8 -*-

from github import Github
from github.Issue import Issue
from github.Repository import Repository
import os
import time
import urllib.parse
import codecs
from nasa_client import NasaClient
from word_cloud import WordCloudGenerator

user: Github
ghiblog: Repository
cur_time: str


def format_issue(issue: Issue):
    return '- [%s](%s)  %s  \t \n' % (
        issue.title, issue.html_url, sup('%s :speech_balloon:' % issue.comments))


def sup(text: str):
    return '<sup>%s</sup>' % text


def sub(text: str):
    return '<sub>%s</sub>' % text


def update_readme_md_file(contents):
    with codecs.open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(contents)
        f.flush()
        f.close()


def login():
    global user
    username = os.environ.get('GITHUB_LOGIN')
    password = os.environ.get('GITHUB_TOKEN')
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

    user_login = user.get_user().login
    pic_of_the_day = NasaClient().get_picture_of_the_day()

    summary_section = '''
<p align='center'>
    <a href="#"><img src="assets/ghiblog.png" width="50%"/></a>
</p>

<p align='center'>
    <img src="https://badgen.net/circleci/github/{0}/ghiblog"/>
    <img src="https://badgen.net/badge/labels/{1}"/>
    <img src="https://badgen.net/github/issues/{0}/ghiblog"/>
    <img src="https://badgen.net/badge/last-commit/{2}"/>
    <img src="https://badgen.net/github/forks/{0}/ghiblog"/>
    <img src="https://badgen.net/github/stars/{0}/ghiblog"/>
    <img src="https://badgen.net/github/watchers/{0}/ghiblog"/>
    <img src="https://badgen.net/github/release/{0}/ghiblog"/>
</p>

<p align='center'>
    <a href="https://github.com/jwenjian/visitor-count-badge">
        <img src="https://visitor-count-badge.herokuapp.com/total.svg?repo_id={0}.ghiblog"/>
    </a>
    <a href="https://github.com/jwenjian/visitor-count-badge">
        <img src="https://visitor-count-badge.herokuapp.com/today.svg?repo_id={0}.ghiblog"/>
    </a>
</p>

## :artificial_satellite:今日图片

<p align="center"><b>{3}</b></p>

<p align="center">
    <img src="{4}" alt="{3}" title="{5}" width="50%"/>
</p>

'''.format(user_login, total_label_count, cur_time, pic_of_the_day.title, pic_of_the_day.url,
           pic_of_the_day.explanation)

    return summary_section


def bundle_pinned_issues_section():
    global ghiblog

    pinned_label = ghiblog.get_label(':+1:置顶')
    pinned_issues = ghiblog.get_issues(labels=(pinned_label,))

    pinned_issues_section = '\n## 置顶 :thumbsup: \n'

    for issue in pinned_issues:
        pinned_issues_section += format_issue(issue)

    return pinned_issues_section


def format_issue_with_labels(issue: Issue):
    global user

    labels = issue.get_labels()
    labels_str = ''

    for label in labels:
        labels_str += '[%s](https://github.com/%s/ghiblog/labels/%s), ' % (
            label.name, user.get_user().login, urllib.parse.quote(label.name))

    if '---' in issue.body:
        body_summary = issue.body[:issue.body.index('---')]
    else:
        body_summary = issue.body[:150]

    return '''
#### [{0}]({1}) {2} \t {3}

:label: : {4}

{5}

[更多>>>]({1})

---

'''.format(issue.title, issue.html_url, sup('%s :speech_balloon:' % issue.comments), issue.created_at, labels_str[:-2],
           body_summary)


def bundle_new_created_section():
    global ghiblog

    new_5_created_issues = ghiblog.get_issues()[:5]

    new_created_section = '## 最新 :new: \n'

    for issue in new_5_created_issues:
        new_created_section += format_issue_with_labels(issue)

    return new_created_section


def bundle_list_by_labels_section():
    global ghiblog
    global user

    # word cloud
    wordcloud_image_url = WordCloudGenerator(ghiblog).generate()

    list_by_labels_section = """
## 分类  :card_file_box: 

<details open="open">
    <summary>
        <img src="%s" title="词云, 点击展开详细分类" alt="词云， 点击展开详细分类">
        <p align="center">:cloud: 词云 :cloud: <sub>点击词云展开详细分类:point_down: </sub></p>
    </summary>

""" % (wordcloud_image_url,)

    all_labels = ghiblog.get_labels()

    for label in all_labels:
        temp = ''
        # 这里的count是用来计算该label下有多少issue的, 按理说应该是取issues_in_label的totalCount, 但是不知道为什么取出来的一直都是
        # 所有的issue数量, 之后再优化.
        count = 0
        issues_in_label = ghiblog.get_issues(labels=(label,))
        for issue in issues_in_label:
            temp += format_issue(issue)
            count += 1

        list_by_labels_section += '''
<details>
<summary>%s\t<sup>%s:newspaper:</sup></summary>

%s

</details>
''' % (label.name, count, temp)

    list_by_labels_section += """

</details>    
"""
    return list_by_labels_section


def bundle_about_me_section():
    global user

    about_me_section = '''
## 关于:boy: 

[<img alt="%s" src="%s" width="233"/>](%s)

**%s**

:round_pushpin: %s

:black_flag: %s
''' % (user.get_user().name, user.get_user().avatar_url, user.get_user().html_url, user.get_user().name,
       user.get_user().location,
       user.get_user().bio)

    return about_me_section


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

    # 5. new created section
    new_created_section = bundle_new_created_section()
    print(new_created_section)

    # 6. list by labels section
    list_by_labels_section = bundle_list_by_labels_section()
    print(list_by_labels_section)

    # 7. about me section
    about_me_section = bundle_about_me_section()
    print(about_me_section)

    contents = [summary_section, pinned_issues_section, new_created_section, list_by_labels_section, about_me_section]
    update_readme_md_file(contents)

    print('README.md updated successfully!!!')


if __name__ == '__main__':
    execute()
