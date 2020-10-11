"""
 * Project        Python-Geek-Training
 * (c) copyright  2020
 * Author: Alice Wang

simulate the process of logining the website processon based on webDriver
Steps:
1. create a client of WebDriver, be it Chrome or Firefox, please set the API file if it's Chrome
2. get the source website
3. click Login
4. input the user name and password
5. login
6. save the cookie

Note: Need to deal with different Exceptions from WebDriver
1. If get(url) takes too much time, then there is TimeoutException
2. If find_element_by_id or find_element_by_xpath failed, there is NoSuchElementException
3. If invalid username or password, then no Exception raised by WebDriver, but we need to take care it, so raise a
    Exception by ourself, to alter that the "login" button click failed since invalid user or password

4. How to deal with wait in WebDriver, please refer to: https://selenium-python.readthedocs.io/waits.html
    4.1 Implicit wait based on implicit_wait
    4.2 Explicit wait based on WebDriverWait
"""
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(browser, login_url, form_data, excepted_title) -> []:
    """
    :param
        browser:
        url:
        form_data:
        excepted_title:
    :exception NoSuchElementException from WeDriver
    :return return the cookie in str format if login successed
    """
    cookies = []

    # retry 10 times if there is timeout happens when get the login website
    retry_cnt = 0
    while retry_cnt < 10:
        retry_cnt += 1
        try:
            browser.get( login_url )
        except TimeoutException as ex:
            print( ex )
            continue
        else:
            break

    time.sleep(5)
    try:
        browser.find_element_by_xpath( '/html/body/header/ul/li[5]/a' ).click()
    except NoSuchElementException as ex:
        raise ex

    try:
        # clear any previous context
        login_email = browser.find_element_by_id( "login_email" )
        login_pw = browser.find_element_by_id( "login_password" )
    except Exception as ex:
        raise ex
    # clear any previous context before login
    login_email.clear()
    login_pw.clear()
    # login with user information
    time.sleep( 3 )
    login_email.send_keys( form_data['user'] )
    login_pw.send_keys( form_data['passwd'] )
    time.sleep( 3 )

    try:
        login_btn = browser.find_element_by_id( "signin_btn" )
    except Exception as ex:
        raise ex
    login_btn.click()

    try:
        WebDriverWait( browser, 20 ).until( EC.title_is( excepted_title ) )
        cookies = browser.get_cookies()
    except TimeoutException as e:
        print('TimeoutException: possible invalid user or password')
        raise e

    browser.quit()
    return cookies


if __name__ == '__main__':
    url = 'https://processon.com/'
    excepted_title = 'ProcessOn - Diagrams'
    form_data = {
        'user': 'tester@gmail.com',
        'passwd': '123'
    }

    try:
        browser = webdriver.Chrome(
            executable_path='D:\\01_Projects\\Github\\Python004\\Week02\\homework2\\chromedriver_win32\\chromedriver.exe' )
        try:
            cookies = login( browser, url, form_data, excepted_title )
            with open( 'processon_cookie.text', 'w+', encoding='utf8' ) as f:
                f.write( "\n".join( str( item ) for item in cookies ) )
            # quit the browser if everything finished
            browser.quit()

        except Exception as ex:
            print( ex )
    except Exception as ex:
        print( ex )
