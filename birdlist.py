#!/usr/bin/env python3
import argparse
from urllib.parse import urlparse

import re
import settings
from lxml import html
from twitter import Twitter


def build_argparser(default_url, default_list):
    parser = argparse.ArgumentParser(description="add WMKS Twitter users to a twitter list")
    parser.add_argument("-u", "--url", type=str, help="URL to crawl for twitter users", default=default_url)
    parser.add_argument("-a", "--archive", action='store_true',
                        help="print archived urls to crawl")
    parser.add_argument("-l", "--list", type=str, default=default_list,
                        help="Twitter list to add users to, will be created if it does not exist")
    return parser


def fetch_userlist(url):
    doc = html.parse(url)
    tw_links = doc.xpath('//a[starts-with(@href, "https://twitter") or starts-with(@href, "http://twitter")]')
    tw_urls = (a.get('href') for a in tw_links)

    r = re.compile(r'https?://twitter.*/(?P<user>[A-Za-z0-9_]+?)/?$')
    return [r.match(u).groupdict()['user'].lower() for u in tw_urls]


def fetch_archive_urls(url, location):
    doc = html.parse(url)
    archive_links = doc.xpath('//a[starts-with(@href, "/location/%s")]' % location.lower())
    uri = urlparse(url)
    is_date_test = re.compile(r'.*\d{4}-\d{2}-\d{2}$')
    return ["{uri.scheme}://{uri.netloc}{href}".format(uri=uri, href=e.get('href')) for e in archive_links
            if is_date_test.match(e.get('href'))]


def cleanup_users(raw_user_list, dummies):
    """
    remove duplicates and dummy user names
    :param raw_user_list:
    :param dummies:
    :return:
    """
    return set([entry for entry in raw_user_list if entry not in dummies])

if __name__ == '__main__':
    args = build_argparser(settings.DEFAULT_URL, settings.DEFAULT_LIST).parse_args()

    if args.archive:
        urls = fetch_archive_urls(args.url, settings.WM_LOCATION)
        print("\n".join(urls))
    else:
        raw_user_list = fetch_userlist(args.url)
        users = cleanup_users(raw_user_list, settings.DUMMY_NAMES)

        t = Twitter(settings.CONSUMER_TOKEN, settings.CONSUMER_SECRET)
        if not (settings.ACCESS_TOKEN and settings.ACCESS_TOKEN_SECRET):
            (access_token, secret) = t.generate_access_token()

            print("your access_token: %s" % access_token)
            print("your access_token_secret: %s" % secret)
        else:
            (access_token, secret) = (settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

        at = t.authenticate(access_token, secret)
        tw_list = at.get_list(args.list)

        count = at.add_missing_members(tw_list, users)
        if count > 0:
            print("added %d count users to list %s" % (count, args.list))
