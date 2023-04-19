# translate proxy  from list

from googletrans import Translator
import concurrent.futures
import re
import pickle
import random
from datasets import load_dataset
from tqdm import tqdm

def extract_proxy(address):
    return f'http://{address.split()[-1].replace(">", "")}'


def translate_tweet_to_javanese_proxy(tweet, proxy):
    with open('./googledomain.txt', "r") as f:
        wservice = [f'translate.{gdomain.strip()}' for gdomain in f.readlines()]

    translator = Translator(service_urls=wservice, proxies=proxy)
    my_translation = translator.translate(tweet, src='en', dest='jw')
    return my_translation.text


def find_translate_proxy(proxy_file='./working_proxy.txt'):
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


def save_working_proxy():
    list_working_proxy = find_translate_proxy()
    with open('./working_proxy.txt', 'w') as f:
        for item in list_working_proxy:
            f.write("%s" % item)


def translate_en_jw(tweet):
    with open('./working_proxy.txt', 'r') as f:
        working_proxies = [line for line in f.readlines()]

    for proxy in working_proxies:
        try:
            proks = extract_proxy(proxy)
            prox_dict = {"http": proks}
            translation = translate_tweet_to_javanese_proxy(tweet, prox_dict)
            return translation
        except Exception as e:
            working_proxies.remove(proxy)
            with open('./working_proxy.txt', 'w') as f:
                for item in working_proxies:
                    f.write("%s" % item)
            print(f"Removed non-working proxy: {proxy.strip()}")
    return "No working proxies found."


def translate_en_jw_worker(tweet, proxy):
    try:
        proks = extract_proxy(proxy)
        prox_dict = {"http": proks}
        translation = translate_tweet_to_javanese_proxy(tweet, prox_dict)
        return translation
    except Exception as e:
        print(f"Error with proxy {proxy.strip()}: {str(e)}")
        return None

def translate_en_jw(tweet, max_workers=5):
    with open('./working_proxy.txt', 'r') as f:
        working_proxies = [line for line in f.readlines()]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        translations = list(executor.map(translate_en_jw_worker, [tweet]*len(working_proxies), working_proxies))

    for translation, proxy in zip(translations, working_proxies):
        if translation:
            return translation
        else:
            working_proxies.remove(proxy)
            with open('./working_proxy.txt', 'w') as f:
                for item in working_proxies:
                    f.write("%s" % item)
            print(f"Removed non-working proxy: {proxy.strip()}")

    return "No working proxies found."

def main():
    tweet = "This is a test tweet"
    translated_tweet = translate_en_jw(tweet)
    print(f"Original tweet: {tweet}")
    print(f"Translated tweet: {translated_tweet}")

if __name__ == '__main__':
    main()
