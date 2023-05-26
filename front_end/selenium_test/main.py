import os
import time
from selenium import webdriver
from fuzztask.fuzztask_test import check_task, submit_task, check_record, download_file, switch_record_access, \
    delete_record
from user.user_test import register, login, retrieve, getInfo, modifyInfo, modifyPass, logout
from forum.forum_test import check_forum
import configparser


class DriverClass:
    def __init__(self):
        if not os.path.exists('tmp'):
            os.mkdir('tmp')

        config = configparser.ConfigParser()
        config.read('config_test.ini')
        self.url = config['app']['url']

        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0,
                 'download.default_directory': os.path.join(os.getcwd(), 'tmp')}
        options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        self.driver = driver
        self.config = config
        self.goto_main_page()

    def goto_main_page(self):
        self.driver.get(self.url)

    def goto_task_page(self):
        self.driver.get(f'{self.url}/fuzztask')

    def goto_task1_page(self):
        self.driver.get(f'{self.url}/fuzztask/1')


class TestMain:
    @classmethod
    def setup_class(self):
        self.driver_class = DriverClass()

    # test cases
    def test_register(self):
        self.driver_class.goto_main_page()
        assert register(self.driver_class.driver, self.driver_class.config)
        time.sleep(1)

    def test_login(self):
        self.driver_class.goto_main_page()
        assert login(self.driver_class.driver, self.driver_class.config)
        time.sleep(1)

    def test_retrieve(self):
        self.driver_class.goto_main_page()
        assert retrieve(self.driver_class.driver, self.driver_class.config)
        time.sleep(1)
    
    def test_getInfo(self):
        self.driver_class.goto_main_page()
        assert getInfo(self.driver_class.driver)
        time.sleep(1)
    
    def test_modify_info(self):
        self.driver_class.goto_main_page()
        assert modifyInfo(self.driver_class.driver, self.driver_class.config)
        time.sleep(1)

    def test_modify_pass(self):
        self.driver_class.goto_main_page()
        assert modifyPass(self.driver_class.driver, self.driver_class.config)
        time.sleep(1)

    def test_check_task(self):
        self.driver_class.goto_main_page()
        assert check_task(self.driver_class.driver)
        time.sleep(1)

    def test_submit_task(self):
        self.driver_class.goto_task1_page()
        assert submit_task(self.driver_class.driver)
        time.sleep(1)

    def test_check_record(self):
        self.driver_class.goto_task1_page()
        assert check_record(self.driver_class.driver)
        time.sleep(1)

    def test_download_file(self):
        self.driver_class.goto_task1_page()
        assert download_file(self.driver_class.driver)
        time.sleep(1)

    def test_switch_record_access(self):
        self.driver_class.goto_task1_page()
        assert switch_record_access(self.driver_class.driver)
        time.sleep(1)

    def test_delete_record(self):
        self.driver_class.goto_task1_page()
        assert delete_record(self.driver_class.driver)
        time.sleep(1)

    def test_check_forum(self):
        # todo
        pass

    def test_logout(self):
        self.driver_class.goto_main_page()
        assert logout(self.driver_class.driver)
        time.sleep(1)
