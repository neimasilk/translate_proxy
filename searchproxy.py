import re
import urllib.request
import urllib
import tqdm


def proxy_list_from_free_proxy_list_net():
    link = 'https://free-proxy-list.net/'
    regex = '<td>(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<\/td><td>(?P<port>\d{1,5})<\/td>'

    req = urllib.request.Request(link)
    req.add_header('User-Agent', 'Mozilla/5.0')
    content = urllib.request.urlopen(req).read().decode('ascii')

    res = re.findall(regex, content)
    return res


def validate_proxy(ip, port):
    link = 'http://www.google.com/humans.txt'
    response = b"Google is built by a large team of engineers, designers, researchers, robots, and others in many different sites across the globe. It is updated continuously, and built with more tools and technologies than we can shake a stick at. If you'd like to help us out, see careers.google.com.\n"

    proxy_handler = urllib.request.ProxyHandler({'http': f'http://{ip}:{port}/'})
    opener = urllib.request.build_opener(proxy_handler)
    try:
        res = opener.open(link, timeout=2)
        if res.read() == response:
            return True, ip, port
    except Exception as e:
        pass
    return False, ip, port


def main():
    proxy_list = proxy_list_from_free_proxy_list_net()
    good_proxy_list = []
    for ip, port in proxy_list:
        res = validate_proxy(ip, port)
        if res[0]:
            good_proxy_list.append((ip, port))
            print(f' + {ip}:{port}')

    print(len(good_proxy_list))
    
    with open('./good_proxy_list.txt', 'w') as f:
        for ip, port in good_proxy_list:
            f.write(f"{ip}:{port}\n")


if __name__ == '__main__':
    main()