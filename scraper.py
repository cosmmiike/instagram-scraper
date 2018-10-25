from instaparser.agents import Agent
from instaparser.entities import Account, Media, Location, Tag, Comment

import urllib.request
import pathlib
import json
import math
import copy


def get_account_info(username, path=None):
    agent = Agent()
    agent.update(Account(username))
    account = Account(username)

    account_info = copy.copy(account)
    account_info.media = dict(account_info.media)
    account_info.follows = dict(account_info.follows)
    account_info.followers = dict(account_info.followers)
    account_dict = {"account": account_info.__dict__}
    account_json = json.dumps(account_dict, indent=2)

    if path == None:
        path = './data/' + username

    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    filename = path + '/' + username + '__account_info.json'

    with open(filename, 'w', newline='', encoding='utf8') as f:
        f.write(account_json)

    return account


def get_tag_info(tagname, path=None):
    agent = Agent()
    agent.update(Tag(tagname))
    tag = Tag(tagname)

    tag_info = copy.copy(tag)
    tag_info.media = dict(tag_info.media)
    tag_dict = {"tag": tag_info.__dict__}
    tag_json = json.dumps(tag_dict, indent=2)

    if path == None:
        path = './data/tag__' + tagname

    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    filename = path + '/tag__' + tagname + '__tag_info.json'

    with open(filename, 'w', newline='', encoding='utf8') as f:
        f.write(tag_json)

    return tag


def get_posts_by_username(username, num=None, path=None):
    agent = Agent()
    agent.update(Account(username))
    account = Account(username)

    media = set()
    pointer = None

    if num == None:
        media_count = account.media_count
    else:
        media_count = num

    limit = 50
    batch_num = math.ceil(media_count/limit)

    for i in range(batch_num):
        if i == batch_num - 1:
            count = media_count - limit * (batch_num - 1)
            batch_media, pointer = agent.get_media(account, pointer=pointer, count=count)
        else:
            batch_media, pointer = agent.get_media(account, pointer=pointer, count=limit)

        for j, item in enumerate(batch_media):
            print("Getting media: " + str(i*50+j+1) + " / " + str(media_count))
            media.add(Media(item.code))

    media_posts = {}
    for i, item in enumerate(media):
        post_info = copy.copy(item)
        post_info.owner = username
        post_info.likes = dict(post_info.likes)
        post_info.comments = dict(post_info.comments)
        media_posts[i] = post_info.__dict__

    media_dict = {"posts": media_posts}
    media_json = json.dumps(media_dict, indent=2)
    print(media_json)

    if path == None:
        path = './data/' + username

    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    filename = path + '/' + username + '__last_posts.json'

    with open(filename, 'w', newline='', encoding='utf8') as f:
        f.write(media_json)

    return media


def get_posts_by_tag_name(tagname, num=None, path=None):
    agent = Agent()
    agent.update(Tag(tagname))
    tag = Tag(tagname)

    media = set()
    pointer = None

    if num == None:
        media_count = tag.media_count
    else:
        media_count = num

    limit = 50
    batch_num = math.ceil(media_count/limit)

    for i in range(batch_num):
        if i == batch_num - 1:
            count = media_count - limit * (batch_num - 1)
            batch_media, pointer = agent.get_media(tag, pointer=pointer, count=count)
        else:
            batch_media, pointer = agent.get_media(tag, pointer=pointer, count=limit)

        for j, item in enumerate(batch_media):
            print("Getting media: " + str(i*50+j+1) + " / " + str(media_count))
            agent.update(Media(item.code))
            media.add(Media(item.code))

    media_posts = {}
    for i, item in enumerate(media):
        post_info = copy.copy(item)
        post_info.likes = dict(post_info.likes)
        post_info.comments = dict(post_info.comments)
        post_info.location = str(post_info.location)
        media_posts[i] = post_info.__dict__

    media_dict = {"posts": media_posts}
    media_json = json.dumps(media_dict, indent=2)
    print(media_json)

    if path == None:
        path = './data/tag__' + tagname

    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    filename = path + '/tag__' + tagname + '__last_posts.json'

    with open(filename, 'w', newline='', encoding='utf8') as f:
        f.write(media_json)

    return media


def get_picture(post, path):
    agent = Agent()
    name = post.owner.login
    picture = post.display_url

    pathlib.Path(path + '/pictures').mkdir(parents=True, exist_ok=True)

    picname = path + '/pictures/' + name + '__' + post.code + '.jpg'
    urllib.request.urlretrieve(picture, picname)

    return picture


def get_all_pictures(media, path):
    media = list(media)
    pictures = []

    for i, item in enumerate(media):
        picture = get_picture(media[i], path)
        pictures.append(picture)
        print("Getting pictures: " + str(i+1) + " / " + str(len(media)))

    return pictures


def get_all_posts_comments(media, path):
    media = list(media)
    for i, item in enumerate(media):
        get_post_comments(media[i], path=path)
        print("Getting comments: " + str(i+1) + " / " + str(len(media)))

    return 0


def get_post_comments(post, num=None, path=None):
    agent = Agent()

    comments = set()
    pointer = None

    if num == None:
        comments_count = int(post.comments_count)
    else:
        comments_count = num

    limit = 50
    batch_num = math.ceil(comments_count/limit)

    for i in range(batch_num):
        if i == batch_num - 1:
            count = comments_count - limit * (batch_num - 1)
            batch_comments, pointer = agent.get_comments(post, pointer=pointer, count=count)
        else:
            batch_comments, pointer = agent.get_comments(post, pointer=pointer, count=limit)

        for j, item in enumerate(batch_comments):
            comments.add(Comment(item.id))

    comments_info = {}
    for i, item in enumerate(comments):
        comment_info = copy.copy(item)
        comment_info.media = str(comment_info.media)
        comment_info.owner = str(comment_info.owner)
        comments_info[i] = comment_info.__dict__

    comments_dict = {"comments": comments_info}
    comments_json = json.dumps(comments_dict, indent=2)

    if path == None:
        path = './data'

    pathlib.Path(path + '/comments').mkdir(parents=True, exist_ok=True)
    postcode = post.code
    filename = path + '/comments/' + postcode + '__last_comments.json'

    with open(filename, 'w', newline='', encoding='utf8') as f:
        f.write(comments_json)

    return comments


def get_user_data(username, num=1000, path=None):
    if path == None:
        path = './data/' + username

    get_account_info(username)
    all_posts = get_posts_by_username(username, path=path, num=num)
    # get_all_pictures(all_posts, path=path)
    get_all_posts_comments(all_posts, path=path)

    return 0


def get_tag_data(tagname, num=1000, path=None):
    if path == None:
        path = './data/tag__' + tagname

    get_tag_info(tagname)
    last_posts = get_posts_by_tag_name(tagname, path=path, num=num)
    # get_all_pictures(last_posts, path=path)
    get_all_posts_comments(last_posts, path=path)

    return 0


def main():
    # tags_list = ['sacamain', 'handbag', 'handbagfashion', 'hermeskelly', 'boots', 'shoes', 'sneakers', 'stansmith']
    tags_list = ['stansmith']
    for item in tags_list:
        print('TAG: ' + item)
        get_tag_data(item, num=1000)

    return 0


main()
