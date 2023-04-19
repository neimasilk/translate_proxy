# translate proxy  from list
import os
from googletrans import Translator
import concurrent.futures
import re

current_directory = os.path.dirname(os.path.abspath(__file__))

def extract_proxy(address):
    return f'http://{address.split()[-1].replace(">", "")}'


def translate_tweet_to_javanese_proxy(tweet, proxy):
    with open('./googledomain.txt', "r") as f:
        wservice = [f'translate.{gdomain.strip()}' for gdomain in f.readlines()]

    translator = Translator(service_urls=wservice, proxies=proxy)
    my_translation = translator.translate(tweet, src='en', dest='jw')
    return my_translation.text

def find_translate_proxy(proxy_file=None):
    if proxy_file is None:
        proxy_file = os.path.join(current_directory, 'good_proxy_list.txt')

    with open(proxy_file, "r") as f:
        proxy_list = [line for line in f.readlines()]

    working_proxy = []
    for alamat in proxy_list:
        try:
            proks = extract_proxy(alamat)
            prox_dict = {"http": proks}
            item = "Hi my name is Amien"
            translation = translate_tweet_to_javanese_proxy(item, prox_dict)
            working_proxy.append(alamat)
            # print(translation)

        except Exception as e:
            print(str(e))
            continue

    return working_proxy

def save_working_proxy(working_proxy_file=None):
    if working_proxy_file is None:
        working_proxy_file = os.path.join(current_directory, 'working_proxy.txt')

    list_working_proxy = find_translate_proxy()
    with open(working_proxy_file, 'w') as f:
        for item in list_working_proxy:
            f.write("%s" % item)


def translate_en_jw(tweet):
    working_proxy_file = os.path.join(current_directory, 'working_proxy.txt')
    with open(working_proxy_file, 'r') as f:
        working_proxies = [line for line in f.readlines()]

    for proxy in working_proxies:
        try:
            proks = extract_proxy(proxy)
            prox_dict = {"http": proks}
            translation = translate_tweet_to_javanese_proxy(tweet, prox_dict)
            return translation
        except Exception as e:
            working_proxies.remove(proxy)
            with open(working_proxy_file, 'w') as f:
                for item in working_proxies:
                    f.write("%s" % item)
            print(f"Removed non-working proxy: {proxy.strip()}")
    return "No working proxies found."


def main():
    # save_working_proxy()
    tweet = "This is a test tweet"
    translated_tweet = translate_en_jw(tweet)
    print(f"Original tweet: {tweet}")
    print(f"Translated tweet: {translated_tweet}")

if __name__ == '__main__':
    main()
