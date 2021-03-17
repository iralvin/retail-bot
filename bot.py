import time
from selenium import webdriver
from bs4 import BeautifulSoup
from constants import passKey, email, loginUrl, itemUrl

browser = webdriver.Chrome('chromedriver')


browser.get(loginUrl)

buyButton = False

loginBtn = browser.find_element_by_class_name('loginLink')

loginBtn.click();

usernameInput = browser.find_element_by_id('ctl00_ContentPlaceHolderColMain_txtlogin')
passwordInput = browser.find_element_by_id('ctl00_ContentPlaceHolderColMain_txtpassword')
signInBtn = browser.find_element_by_id('ctl00_ContentPlaceHolderColMain_btnSignIn')

usernameInput.send_keys(email)
passwordInput.send_keys(passKey)
signInBtn.click()


browser.get(itemUrl)
time.sleep(10)

closePopupBtn = browser.find_element_by_id('ltkpopup-close-button')
closePopupBtn.click()
time.sleep(1)
partsList = browser.find_elements_by_id('wrap')

inStockParts = []

partsAvailable = False

while not partsAvailable:

    for part in partsList:
        status = part.find_element_by_css_selector('.mfr[itemprop="availability"]').get_attribute('innerText')
        if status == 'In Stock':
            inStockParts.append(part)


    # print(inStockParts)

    for part in inStockParts:
        # print("adding to cart")

        # print(part.get_attribute('innerHTML'))

        # print(part.find_element_by_id('ctl00_ContentPlaceHolderColMain_ucSKUList_rptSkuList_ctl01_divAddToCart').get_attribute('innerHTML'))

        addToCartBtn = addBtn = part.find_element_by_id('btnAdd')
        addToCartBtn.click()
        time.sleep(1)
        try:
            alert = browser.switch_to.alert
            if alert:
                alert.accept()
        except:
            print("no alert")

    try:
        checkOutBtn = browser.find_element_by_id('cmHdrCheckoutLink')
        if checkOutBtn:
            partsAvailable = True
            checkOutBtn.click()
    except:
        print("no items added")
        browser.refresh()



    
    



enterCouponBtn = browser.find_element_by_id('aCouponPromoCode')
enterCouponBtn.click()

couponInputField = browser.find_element_by_id('txtCouponPromo')
couponInputField.send_keys('sae')

applyCouponBtn = browser.find_element_by_id('btnCouponPromo')
applyCouponBtn.click()

continueToPaymentBtn = browser.find_element_by_id('btnSaveAndContinue')
continueToPaymentBtn.click()
# while not buyButton:
#     try:
#         addToCartBtn = browser.find_element_by_class_name('single_add_to_cart_button')
#         addToCartBtn.click()
#         print("added to cart")
#         buyButton = true
#     except:
#         print("can't buy")
#         time.sleep(5)
