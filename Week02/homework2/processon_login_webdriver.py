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

"""
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def login(browser, url, form_data, excepted_title) -> []:
    """
    :param
        browser:
        url:
        form_data:
        excepted_title:
    :exception NoSuchElementException from WeDriver
    :return return the cookie in str format if login successed
    """
    cookies = ''

    # retry 10 times if there is timeout happens when get the login website
    retry_cnt = 0
    while retry_cnt < 10:
        retry_cnt += 1
        try:
            browser.get( url )
        except TimeoutException as ex:
            print(ex)
            continue
        else:
            break

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
    login_email.send_keys(form_data['user'])
    login_pw.send_keys(form_data['passwd'])
    time.sleep( 2 )

    try:
        login_btn = browser.find_element_by_id( "signin_btn" )
    except Exception as ex:
        raise ex
    login_btn.click()
    time.sleep(5)

    if browser.title == excepted_title:
        # login success, then to get cookies
        cookies = browser.get_cookies()
        print( cookies )
    return cookies


if __name__ == '__main__':
    url = 'https://processon.com/'
    excepted_title = 'ProcessOn - Diagrams'
    form_data = {
        'user': 'felicity.uestc@gmail.com',
        'passwd': '123'
    }

    try:
        browser = webdriver.Chrome(
            executable_path='D:\\01_Projects\\Github\\Python004\\Week02\\homework2\\chromedriver_win32\\chromedriver.exe' )
        try:
            cookies = login(browser, url, form_data, excepted_title)
            with open( 'processon_cookie.text', 'w+', encoding='utf8' ) as f:
                f.write("\n".join(str(item) for item in cookies))
            # quit the browser if everything finished
            browser.quit()

        except Exception as ex:
            print(ex)
    except Exception as ex:
        print(ex)


