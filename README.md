# vk-url-shortener
VK URL shortener

This is simple URL shortener and stats viewer, that uses VK API. 

### How to install

Python 3 has to be already installed.

Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use

At first, you have to register at VK.com and get your service token for API requests 
(please check the [documentation](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/tokens/service-token)).
This script uses [python-dotenv](https://github.com/theskumar/python-dotenv) module to import VK's token from ```.env``` file,
so you need to create a new file named ".env" in the same folder with script and save your token there like that:
```
VK_SERVICE_TOKEN==tkkmuftjhqv7s36tb6qprppt9sdddoxno6v4yd5gw7wh6ncmb4axwri3b5mynb9jqwptey0
```

The only and required parameter after the run of the script is url.
If you want to shorten url, just input it right after the 'Input the link:'
```
$ python main.py 
Input the link: http://example.com/
Short link: https://vk.cc/LVYnP
```

Or if you want to see the stats of how many times your short link was clicked, type a shortlink:
```
$ python main.py
Input the link: https://vk.cc/LVYnP
Link has been clicked: 1
```
