"""
 * Project        Python-Geek-Training
 * (c) copyright  2020
 * Author: Alice Wang

Simulate the process of logging Processon website (https://processon.com/login) based on request.
Note: there is no complex validation process for this website, so request would be enough.

"""
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

pre_login_url = 'https://processon.com/login'
login_url = 'https://processon.com/login'
cookies = '_ga=GA1.2.327945390.1602315220; _gid=GA1.2.1632550509.1602315220; ' \
          'processon_userKey=5f81656be401fd06fd7f3f64; _sid=c3858532770d12295e8d57c3b3e1aa28; ' \
          'usid=5f8165b07d9c0806f26bb83b; JSESSIONID=F930B3FEB3711F019F2D21B052D981C4.jvm1; ' \
          'zg_did=%7B%22did%22%3A%20%22175116df5033ba-0bd6a4dfcf4602-7e647a66-1fa400-175116df5043be%22%7D; ' \
          'zg_3f37ba50e54f4374b9af5be6d12b208f=%7B%22sid%22%3A%201602329262356%2C%22updated%22%3A%201602329323060%2C' \
          '%22info%22%3A%201602315220241%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22' \
          '%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20' \
          '%225f81656be401fd06fd7f3f64%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201602329262356' \
          '%7D; _gat=1 '
# set the headers
headers = {
    'User-Agent': ua.random,
    'Referer': 'https://processon.com/login?f=signup',
    'Cookie': cookies
}
# set the form data
form_data = {
    'login_email': 'tester@gmail.com',
    'login_password': '123',
}
s = requests.session()
response = s.post(login_url, data=form_data, headers=headers, cookies=s.cookies)
if response.status_code == 200:
    with open('processon_login.html', 'w+', encoding="utf-8") as f:
        f.write(response.text)
        print(response.text)
        f.close()
else:
    print('request failed')