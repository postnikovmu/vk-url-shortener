import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(token, link):

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
    if response.ok and response.json().get("response"):
        result_link = response.json().get("response").get("link")
    if response.ok and response.json().get("error"):
        api_error_msg = response.json().get("error").get("error_msg")
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
    if response.ok and response.json().get("response"):
        short_link = response.json().get("response").get("short_url")
    if response.ok and response.json().get("error"):
        api_error_msg = response.json().get("error").get("error_msg")
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
    if response.ok and response.json().get("response"):
        clicks_count = int(response.json().get("response").get("stats")[0].get("views"))
    if response.ok and response.json().get("error"):
        api_error_msg = response.json().get("error").get("error_msg")
    return api_error_msg, clicks_count


def main():

    load_dotenv()
    VK_SERVICE_TOKEN = os.environ.get('VK_SERVICE_TOKEN')

    link = input('Input the link: ')

    short_link = ''
    clicks_count = 0

    try:
        api_error_msg, is_shorten_link_flag = is_shorten_link(VK_SERVICE_TOKEN, link)
        if not api_error_msg and not is_shorten_link_flag:
            api_error_msg, short_link = shorten_link(VK_SERVICE_TOKEN, link)
        if not api_error_msg and is_shorten_link_flag:
            api_error_msg, clicks_count = count_clicks(VK_SERVICE_TOKEN, link)
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
