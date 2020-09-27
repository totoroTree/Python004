"""
 * Project        Python-Geek-Training
 * (c) copyright  2020
 * Author: Alice Wang

Get the information of top10 movies from Maoyan website
History:
    2020/9/25 initial commit
    2020/9/26 fix issue of hover-tag found nothing
"""
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_movie(url, limit):
    """
    Send GET request to get the movie information
    :param url: the HTTP request url
    :param limit: the number of items
    :return results: the results of movies, including: name, category, release time
    """
    results = []
    if url is None:
        print('ERROR: get_movie() invalid input url')

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'
    cookies = 'uuid_n_v=v1; uuid=E8B8B530006811EB8026CDB2BA3E8FD439E453FC2C1D4123A0F9155857AECEC6; ' \
               '_csrf=8adb40d94cbf8812f196d7ddb4eb3fcb69d4a95dce6e7e04654082eb8acbd2f1; ' \
               'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1601173617; ' \
               'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1601173732; mojo-uuid=d6f71e9e9b340709e0abe0b8b5057517; ' \
               'mojo-trace-id=4; mojo-session-id={"id":"2f3a230c46c7ba400194996b7fabc5ba","time":1601173618725}; ' \
               '_lxsdk_cuid=174cd62911662-01d21c8e39ab768-4c3f247a-144000-174cd6291179e; ' \
               '_lxsdk_s=174cd629119-ac5-04e-d9f%7C%7C7; ' \
               '_lxsdk=E8B8B530006811EB8026CDB2BA3E8FD439E453FC2C1D4123A0F9155857AECEC6; ' \
               '__mta=250920249.1601173623167.1601173635796.1601173733648.3 '
    header = {'User-Agent': user_agent,
              'Cookie': cookies}
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        bs_info = bs(response.text, 'html.parser')
        for item in bs_info.select('.movie-hover-info', limit=limit):
            # name = item.select('.movie-hover-title')[0].select('.name')[0].text
            name = item.select('.name')[0].contents[0]
            category = item.select('.movie-hover-title')[1].contents[2].strip()
            release_time = item.select('.movie-hover-title')[3].contents[2].strip()
            results.append({'name': name, 'category': category, 'release_time': release_time})
    else:
        print('ERROR: get_movie() response with HTTP code: %d', response.status_code)

    if results is None:
        print('ERROR: get_movie() Not found any movies.')

    return results


if __name__ == '__main__':
    url = 'https://maoyan.com/films?showType=3'
    movies = get_movie(url, 10)
    if movies is not None:
        data = pd.DataFrame(movies)
        data.to_csv('movies.csv', encoding='utf-8', header=['name', 'category', 'release_time'])

