from instaparser.agents import Agent
from instaparser.entities import Account, Media, Location, Tag, Comment

import urllib.request
import pathlib
import json
import csv


def GetLastPostsByUserName(username, num=50):
    agent = Agent()
    account = Account(username)
    media, pointer = agent.get_media(account, count=num)
    media_data = []

    pathlib.Path('./data/' + username).mkdir(parents=True, exist_ok=True)

    filename = './data/' + username + '/' + username + '__last_posts.csv'
    with open(filename, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'code', 'caption', 'owner', 'date', 'location', 'likes_count', 'comments_count', 'comments_disabled', 'is_video', 'video_url', 'is_ad', 'display_url'])

        for i, item in enumerate(media):
            print("Getting media: " + str(i+1) + " / " + str(num))
            media_data.append(list([item.id, item.code, item.caption, item.owner, item.date, item.location, item.likes_count, item.comments_count, item.comments_disabled, item.is_video, item.video_url, item.is_ad, item.display_url]))
        writer.writerows(media_data)

    return media


def GetPicture(post, path):
    agent = Agent()
    name = post.owner.login
    picture = post.display_url

    pathlib.Path(path + '/pictures').mkdir(parents=True, exist_ok=True)

    picname = path + '/pictures/' + name + '__' + post.code + '.jpg'
    urllib.request.urlretrieve(picture, picname)

    return picture


def GetAllPictures(media, path):
    pictures = []
    for i, item in enumerate(media):
        picture = GetPicture(media[i], path)
        pictures.append(picture)
        print("Getting pictures: " + str(i+1) + " / " + str(len(media)))

    return pictures


def GetComments(post, path, num=50):
    agent = Agent()
    comments, pointer = agent.get_comments(post, count=num)

    pathlib.Path(path + '/comments').mkdir(parents=True, exist_ok=True)

    comments_data = []

    postcode = post.code
    filename = path + '/comments/' + postcode + '__last_comments.csv'
    with open(filename, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'media', 'owner', 'text', 'created_at'])
        for item in comments:
            comments_data.append(list([item.id, item.media, item.owner, item.text, item.created_at]))
        writer.writerows(comments_data)

    return comments_data


def GetAllComments(media, path):
    for i, item in enumerate(media):
        GetComments(media[i], path, 50)
        print("Getting comments: " + str(i+1) + " / " + str(len(media)))

    return 0


def GetAccountInfo(username):
    agent = Agent()
    agent.update(Account(username))
    account = Account(username)

    pathlib.Path('./data/' + username).mkdir(parents=True, exist_ok=True)

    filename = './data/' + username + '/' + username + '__account_info.csv'
    with open(filename, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'login', 'full_name', 'profile_pic_url', 'profile_pic_url_hd', 'fb_page', 'biography', 'follows_count', 'followers_count', 'media_count', 'is_private', 'is_verified', 'country_block'])
        writer.writerow(list([account.id, account.login, account.full_name, account.profile_pic_url, account.profile_pic_url_hd, account.fb_page, account.biography, account.follows_count, account.followers_count, account.media_count, account.is_private, account.is_verified, account.country_block]))

    return account


def GetTagInfo(tagname):
    agent = Agent()
    agent.update(Tag(tagname))
    tag = Tag(tagname)

    pathlib.Path('./data/tag__' + tagname + '/').mkdir(parents=True, exist_ok=True)

    filename = './data/tag__' + tagname + '/tag__' + tagname + '__tag_info.csv'
    with open(filename, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'media_count'])
        writer.writerow(list([tag.name, tag.media_count]))

    return tag


def GetPostByCode(code):
    agent = Agent()

    return agent.update(Media(code))


def GetTopPostsByTagName(tagname):
    agent = Agent()
    agent.update(Tag(tagname))
    tag = Tag(tagname)

    media = list(tag.top_posts)
    for item in media:
        agent.update(Media(item))

    media_data = []

    pathlib.Path('./data/tag__' + tagname).mkdir(parents=True, exist_ok=True)

    filename = './data/tag__' + tagname + '/tag__' + tagname + '__top_posts.csv'
    with open(filename, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'code', 'caption', 'owner', 'date', 'location', 'likes_count', 'comments_count', 'comments_disabled', 'is_video', 'video_url', 'is_ad', 'display_url'])

        for i, item in enumerate(media):
            print("Getting media: " + str(i+1) + " / " + str(len(media)))
            media_data.append(list([item.id, item.code, item.caption, item.owner, item.date, item.location, item.likes_count, item.comments_count, item.comments_disabled, item.is_video, item.video_url, item.is_ad, item.display_url]))
        writer.writerows(media_data)

    return media


def jprint(tag, data_dict):
    # print(json.dumps(data_dict, indent=4))
    pathlib.Path('./data/tag__' + tag).mkdir(parents=True, exist_ok=True)
    f = open('./data/tag__' + tag + '/tag__' + tag + '.json','w+')
    f.write(json.dumps(data_dict, indent=4))


def GetLastPostsByTagName(tagname):
    agent = Agent()
    agent.update(Tag(tagname))
    tag = Tag(tagname)

    # jprint(tagname, xx)

    media = list(tag.last_media)
    for item in media:
        agent.update(Media(item))

    media_data = []

    pathlib.Path('./data/tag__' + tagname).mkdir(parents=True, exist_ok=True)

    filename = './data/tag__' + tagname + '/tag__' + tagname + '__last_posts.csv'
    with open(filename, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'code', 'caption', 'owner', 'date', 'location', 'likes_count', 'comments_count', 'comments_disabled', 'is_video', 'video_url', 'is_ad', 'display_url'])

        for i, item in enumerate(media):
            print("Getting media: " + str(i+1) + " / " + str(len(media)))
            media_data.append(list([item.id, item.code, item.caption, item.owner, item.date, item.location, item.likes_count, item.comments_count, item.comments_disabled, item.is_video, item.video_url, item.is_ad, item.display_url]))
        writer.writerows(media_data)

    return media


def GetUserData(username, path):
    GetAccountInfo(username)
    last_50_posts = GetLastPostsByUserName(username, 50)
    GetAllPictures(last_50_posts, path)
    GetAllComments(last_50_posts, path)

    return 0


def GetTagData(tagname, path):
    GetTagInfo(tagname)
    top_posts = GetTopPostsByTagName(tagname)
    last_posts = GetLastPostsByTagName(tagname)
    GetAllPictures(last_posts, path + 'last__')
    GetAllComments(last_posts, path + 'last__')

    return 0


def main():
    username = 'schonmagazine'
    path = './data/' + username
    GetUserData(username, path)

    # tag = 'vetementsxswear'
    # path = './data/tag__' + tag
    # GetTagData(tag, path)

    return 0

if__name__== "__main__:
    main()
