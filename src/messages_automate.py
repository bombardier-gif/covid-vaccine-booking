from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def getOTP(driver):

    #get first message into view
    message = driver.find_elements_by_tag_name('mws-conversation-list-item')
    message = message[0]
    message.click()

    time.sleep(3)

    all_messages = driver.find_elements_by_tag_name('mws-message-part-content')
    otp = []
    for each in all_messages:
        sub = each.find_element_by_tag_name('div')
        sub2 = sub.find_element_by_tag_name('div')
        otp.append(sub2.get_attribute('innerHTML')[37:43])

    print("OTP is:", otp[-1])
    return otp[-1]
