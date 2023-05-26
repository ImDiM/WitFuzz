from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


def register(driver: webdriver.Chrome, config):
    """
    TC1-1 用户注册功能测试
    :return:
    """
    try:
        register_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/header/div/div[2]/a[2]')
            )
        )
        register_url.click()

        name = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form/div[1]/div/div/div/input')
            )
        )
        name.send_keys(config['app']['name'])

        e_mail = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form/div[2]/div/div/div/input')
            )
        )
        e_mail.send_keys(config['app']['email'])

        pwd = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form/div[3]/div/div/div/input')
            )
        )
        pwd.send_keys(config['app']['password'])

        pwd_re = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form/div[4]/div/div/div/input')
            )
        )
        pwd_re.send_keys(config['app']['password'])

        submit_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div/div/div/div[2]/div[4]/button[1]')
            )
        )
        submit_bt.click()
        time.sleep(1)

        return True
    except Exception:
        return False


def login(driver: webdriver.Chrome, config):
    """
    TC1-2 用户登录功能测试
    :return:
    """
    try:
        login_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/header/div/div[2]/a[1]')
            )
        )
        login_url.click()

        e_mail = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form/div[1]/div/div/div/input')
            )
        )
        e_mail.send_keys(config['app']['email'])
        pwd = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form/div[2]/div/div/div/input')
            )
        )
        pwd.send_keys(config['app']['password'])

        login_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div/div/div/div[2]/div[4]/button')
            )
        )
        login_bt.click()
        time.sleep(1)

        return True
    except Exception:
        return False
    

def retrieve(driver: webdriver.Chrome, config):
    """
    TC1-3 用户找回密码功能测试
    :return:
    """
    try:
        login_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/header/div/div[2]/a[1]')
            )
        )
        login_url.click()

        retrieve_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div/div/div/div[2]/a/div')
            )
        )
        retrieve_url.click()

        e_mail = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form[1]/div[1]/div/div/div/input')
            )
        )
        e_mail.send_keys(config['app']['email'])

        send_code_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div/div/div/div[2]/form[1]/div[2]/div/button')
            )
        )
        send_code_bt.click()

        code = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form[2]/div[1]/div/div/div/input')
            )
        )
        code.send_keys(config['app']['code'])

        verify_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div/div/div/div[2]/form[2]/div[2]/div/button')
            )
        )
        verify_bt.click()

        pwd = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form[3]/div[1]/div/div/div/input')
            )
        )
        pwd.send_keys(config['app']['password'])

        pwd_re = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/div/div/div/div[2]/form[3]/div[3]/div/div/div/input')
            )
        )
        pwd_re.send_keys(config['app']['password'])

        submit_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div/div/div/div[2]/div[6]/button')
            )
        )
        submit_bt.click()

        time.sleep(1)

        return True
    except Exception:
        return False


def getInfo(driver: webdriver.Chrome):
    """
    TC1-4 查看用户信息功能测试
    :return:
    """
    try:
        user_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/header/div/div[2]/div')
            )
        )
        user_bt.click()

        info_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[2]/div/div/div[1]/div/ul/li[2]')
            )
        )
        info_bt.click()
        time.sleep(1)
        return True
    except Exception:
        return False
    

def modifyInfo(driver: webdriver.Chrome, config):
    """
    TC1-5 修改用户信息功能测试
    :return:
    """
    try:
        user_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/header/div/div[2]/div')
            )
        )
        user_bt.click()

        info_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[2]/div/div/div[1]/div/ul/li[2]')
            )
        )
        info_bt.click()

        name = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/form[1]/div[1]/div/div[1]/div/input')
            )
        )
        name.send_keys(config['app']['new_name'])

        submit_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/button[1]')
            )
        )
        submit_bt.click()

        time.sleep(1)
        return True
    except Exception:
        return False
    

def modifyPass(driver: webdriver.Chrome, config):
    """
    TC1-5 修改用户密码功能测试
    :return:
    """
    try:
        user_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/header/div/div[2]/div')
            )
        )
        user_bt.click()

        info_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[2]/div/div/div[1]/div/ul/li[2]')
            )
        )
        info_bt.click()

        pwd = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/form[2]/div[1]/div/div/div/input')
            )
        )
        pwd.send_keys(config['app']['new_password'])

        re_pwd = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div/div/section/section/section/main/form[2]/div[2]/div/div/div/input')
            )
        )
        re_pwd.send_keys(config['app']['new_password'])

        submit_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/button[2]')
            )
        )
        submit_bt.click()

        time.sleep(1)
        return True
    except Exception:
        return False
    

def logout(driver: webdriver.Chrome):
    try:
        user_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/header/div/div[2]/div')
            )
        )
        user_bt.click()

        logout_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[2]/div/div/div[1]/div/ul/li[3]')
            )
        )
        logout_bt.click()
        time.sleep(1)
        return True
    except Exception:
        return False
