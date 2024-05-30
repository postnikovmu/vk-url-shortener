import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


def is_short_link(token, link):

    url = 'https://api.vk.ru/method/utils.checkLink'
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'v': '5.236',
        'url': link,
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    result_link = ''
    api_error_msg = ''
    response_json = response.json()
    if response_json.get("response"):
        result_link = response_json.get("response").get("link")
    if response_json.get("error"):
        api_error_msg = response_json.get("error").get("error_msg")
    if link in result_link:
        return api_error_msg, False
    return api_error_msg, True


def shorten_link(token, link):

    url = 'https://api.vk.ru/method/utils.getShortLink'
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'v': '5.236',
        'url': link,
        'private': 0
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    api_error_msg = ''
    short_link = ''
    response_json = response.json()
    if response_json.get("response"):
        short_link = response_json.get("response").get("short_url")
    if response_json.get("error"):
        api_error_msg = response_json.get("error").get("error_msg")
    return api_error_msg, short_link


def count_clicks(token, link):

    parsed = urlparse(link)
    key = parsed.path.replace('/', '')

    url = 'https://api.vk.ru/method/utils.getLinkStats'
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'v': '5.236',
        'key': key,
        'interval': 'forever',
        'extended': 0
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    api_error_msg = ''
    clicks_count = 0
    response_json = response.json()
    if response_json.get("response").get("stats"):
        clicks_count = int(response_json.get("response").get("stats")[0].get("views"))
    if response_json.get("error"):
        api_error_msg = response_json.get("error").get("error_msg")
    return api_error_msg, clicks_count


def main():

    load_dotenv()
    vk_service_token = os.environ['VK_SERVICE_TOKEN']

    parser = argparse.ArgumentParser()
    parser.add_argument("link")
    args = parser.parse_args()
    link = args.link

    short_link = ''
    clicks_count = 0

    try:
        api_error_msg, is_short_link_flag = is_short_link(vk_service_token, link)
        if not api_error_msg and not is_short_link_flag:
            api_error_msg, short_link = shorten_link(vk_service_token, link)
        if not api_error_msg and is_short_link_flag:
            api_error_msg, clicks_count = count_clicks(vk_service_token, link)
    except requests.exceptions.HTTPError as e:
        print(f'Exception error: {e}')
        return

    if api_error_msg:
        print('VK API error message:', api_error_msg)
        return

    if short_link:
        print('Short link:', short_link)
    if clicks_count:
        print('Link has been clicked:', clicks_count)


if __name__ == '__main__':
    main()
