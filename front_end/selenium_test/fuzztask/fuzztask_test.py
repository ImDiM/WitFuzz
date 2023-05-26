import os.path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


def check_task(driver: webdriver.Chrome):
    """
    TC2-1 查看评测任务功能测试
    :return:
    """
    try:
        fuzztask_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(('xpath', '//*[@id="app"]/div/section/section/aside/ul/a[2]'))
        )
        fuzztask_bt.click()

        card_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div/div/div[1]/a'))
        )
        card_bt.click()

        submit_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/ul/a[2]'))
        )
        submit_bt.click()
        time.sleep(1)
        board_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/ul/a[3]'))
        )
        board_bt.click()
        time.sleep(1)
        record_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/ul/a[4]'))
        )
        record_bt.click()
        return True
    except Exception:
        return False


def submit_task(driver: webdriver.Chrome):
    """
    TC2-2 提交评测功能测试
    :return:
    """
    try:
        submit_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/ul/a[2]'))
        )
        submit_url.click()

        submit_description = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div[2]/div[4]/textarea')
            )
        )
        driver.execute_script("arguments[0].scrollIntoView();", submit_description)

        submit_description.send_keys('Test submit description.')

        uploader = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div[2]/div[8]/div[1]/input')
            )
        )
        uploader.send_keys(os.path.join(os.getcwd(), 'fuzztask/test.c'))

        submit_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/div/div[2]/button')
            )
        )
        submit_bt.click()
        return True
    except Exception:
        return False


def check_record(driver: webdriver.Chrome):
    """
    TC2-3 查看提交记录功能
    :return:
    """
    try:
        board_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/ul/a[3]'))
        )
        board_url.click()

        board_record = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]')
            )
        )
        board_record.click()
        time.sleep(1)
        close_record_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div/div[4]/div/header/button')
            )
        )
        close_record_bt.click()

        record_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/ul/a[4]'))
        )
        record_url.click()

        record2 = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[2]')
            )
        )
        record2.click()
        time.sleep(1)

        close_record_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div/div[4]/div/header/button')
            )
        )
        close_record_bt.click()
        return True
    except Exception:
        return False


def download_file(driver: webdriver.Chrome):
    """
    TC2-4 下载提交记录文件功能
    :return:
    """
    try:
        record_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/section/section/main/div[2]/div/ul/a[4]'))
        )
        record_url.click()
        time.sleep(0.5)

        record2 = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[2]')
            )
        )
        record2.click()
        time.sleep(0.5)

        download_result_file = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div/div[4]/div/div/button[1]')
            )
        )
        download_result_file.click()
        time.sleep(0.5)

        download_submit_file = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div/div[4]/div/div/button[2]')
            )
        )
        download_submit_file.click()
        time.sleep(0.5)

        close_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div/div[4]/div/header/button')
            )
        )
        close_bt.click()
        return True
    except Exception:
        return False


def switch_record_access(driver: webdriver.Chrome):
    """
    TC2-5 切换提交记录权限功能
    :return:
    """
    try:
        record_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/ul/a[4]')
            )
        )
        record_url.click()
        time.sleep(0.5)
        record_switch_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[1]/td[8]/div/button[2]')
            )
        )
        record_switch_bt.click()
        return True
    except Exception:
        return False


def delete_record(driver: webdriver.Chrome):
    """
    TC2-6 删除提交记录功能
    :return:
    """
    try:
        record_url = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/ul/a[4]')
            )
        )
        record_url.click()
        time.sleep(0.5)

        delete_bt = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '/html/body/div[1]/div/section/section/section/main/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[2]/td[8]/div/button[1]')
            )
        )
        delete_bt.click()
        time.sleep(0.5)

        # ok_bt = WebDriverWait(driver, 10, 1).until(
        #     expected_conditions.presence_of_element_located(
        #         ('xpath', '//*[@id="el-id-2049-42"]/div/div[2]/button[2]')
        #     )
        # )
        # ok_bt.click()
        # time.sleep(0.5)

        title = WebDriverWait(driver, 10, 1).until(
            expected_conditions.presence_of_element_located(
                ('xpath', '//*[@id="app"]/div/section/header/div/div[1]/div/div[2]/span'))
        )
        title.click()
        return True
    except Exception:
        return False
