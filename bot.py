import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from constants import passKey, email, loginUrl, itemUrl, stockStatus, itemNameSubstring, phoneNumber

browser = webdriver.Chrome('chromedriver.exe')
browser.get(loginUrl)

loginBtn = browser.find_element_by_class_name('loginLink')
loginBtn.click()

usernameInput = browser.find_element_by_id(
    'ctl00_ContentPlaceHolderColMain_txtlogin')
passwordInput = browser.find_element_by_id(
    'ctl00_ContentPlaceHolderColMain_txtpassword')
signInBtn = browser.find_element_by_id(
    'ctl00_ContentPlaceHolderColMain_btnSignIn')

usernameInput.send_keys(email)
passwordInput.send_keys(passKey)
signInBtn.click()

browser.get(itemUrl)
browser.implicitly_wait(7)

closePopupBtn = browser.find_element_by_id('ltkpopup-close-button')
closePopupBtn.click()
time.sleep(1)

inStockItems = []

areItemsAvailable = False
isCheckingOut = False


while not areItemsAvailable:
    itemsList = browser.find_elements_by_id('wrap')
    for item in itemsList:
        # status = item.find_element_by_css_selector(
        #     '[itemprop="availability"]').get_attribute('innerText')

        status = item.get_attribute('data-status')


        itemName = item.find_element_by_css_selector(
            '[itemprop="name"]').get_attribute('innerText')
        print (f'{itemName} stock status is: {status}')
        print (f'type of status is: {type(status)}')
        if status == stockStatus and itemNameSubstring in itemName:
            inStockItems.append(item)

    if not inStockItems:
        print("partsList is empty")
        print("will refresh page")
        time.sleep(1)
        browser.refresh()
    elif inStockItems:
        print(f'List of parts available: {inStockItems}')
        areItemsAvailable = True

def handleCheckout():
    try:
        checkOutBtn = browser.find_element_by_id('cmHdrCheckoutLink')
        if checkOutBtn:
            print(f'ischeckingout before checkout click bool is {isCheckingOut}')

            checkOutBtn.click()
    except:
        browser.refresh()
        time.sleep(1)
        handleCheckout()

if areItemsAvailable:
    for item in inStockItems:
        itemName = item.find_element_by_css_selector(
            '[itemprop="name"]').get_attribute('innerText')
        print(f"adding {itemName} to cart")

        addToCartBtn = addBtn = item.find_element_by_id('btnAdd')
        addToCartBtn.click()
        time.sleep(1)
        try:
            alert = browser.switch_to.alert
            if alert:
                alert.accept()
                addToCartBtn.click()

        except:
            print("no alert")
    handleCheckout()
    isCheckingOut = True


print(f'ischeckingout AFTER checkout click bool is {isCheckingOut}')
if isCheckingOut:
    print("checking out now")

    browser.implicitly_wait(10)
    shippingOptions = Select(browser.find_element_by_id('ShippingOption'))
    shippingOptions.select_by_index(3);

    # enterCouponBtn = browser.find_element_by_id('aCouponPromoCode')
    # enterCouponBtn.click()

    # couponInputField = browser.find_element_by_id('txtCouponPromo')
    # couponInputField.send_keys('sae')

    # applyCouponBtn = browser.find_element_by_id('btnCouponPromo')
    # applyCouponBtn.click()




    continueToPaymentBtn = browser.find_element_by_id('btnSaveAndContinue')
    continueToPaymentBtn.click()


    time.sleep(10)
    phoneInput = browser.find_element_by_id('txtPhone')
    shippingOptions = Select(browser.find_element_by_id('ShippingOption'))
    phoneInput.clear()
    phoneInput.send_keys(phoneNumber)
    print(f'phoneInput text is: {phoneInput.get_attribute("innerText")}')
    shippingOptions.select_by_index(0);

    time.sleep(1)

    orderReviewBtn = browser.find_element_by_id('btnSaveAndContinue')
    orderReviewBtn.click()