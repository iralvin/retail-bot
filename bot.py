import time
from selenium import webdriver
from bs4 import BeautifulSoup
from constants import passKey, email, loginUrl, itemUrl

browser = webdriver.Chrome('chromedriver.exe')


browser.get(loginUrl)


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

inStockParts = []

partsAvailable = False
isCheckingOut = False

 

while not partsAvailable:
    partsList = browser.find_elements_by_id('wrap')

    for part in partsList:
        status = part.find_element_by_css_selector('.mfr[itemprop="availability"]').get_attribute('innerText')
        if status == 'In Stock':
            inStockParts.append(part)

    if not inStockParts:
        print("partsList is empty")
        time.sleep(2)
        browser.refresh()
    elif inStockParts:
        print(f'List of parts available: {inStockParts}')
        partsAvailable = True
        # addItemsToCart()

    


if partsAvailable:
    for part in inStockParts:
        itemName = part.find_element_by_css_selector('[itemprop="name"]').get_attribute('innerText')
        print(f"adding {itemName} to cart")

        # print(part.get_attribute('innerHTML'))

        # print(part.find_element_by_id('ctl00_ContentPlaceHolderColMain_ucSKUList_rptSkuList_ctl01_divAddToCart').get_attribute('innerHTML'))

        addToCartBtn = addBtn = part.find_element_by_id('btnAdd')
        addToCartBtn.click()
        time.sleep(1)
        try:
            alert = browser.switch_to.alert
            if alert:
                alert.accept()
                addToCartBtn.click()

        except:
            print("no alert")

    try:
        checkOutBtn = browser.find_element_by_id('cmHdrCheckoutLink')
        if checkOutBtn:
            isCheckingOut = True
            checkOutBtn.click()
    except:
        print("error with checkout button")
            



    
    


# if isCheckingOut:
#     enterCouponBtn = browser.find_element_by_id('aCouponPromoCode')
#     enterCouponBtn.click()

#     couponInputField = browser.find_element_by_id('txtCouponPromo')
#     couponInputField.send_keys('sae')

#     applyCouponBtn = browser.find_element_by_id('btnCouponPromo')
#     applyCouponBtn.click()

#     continueToPaymentBtn = browser.find_element_by_id('btnSaveAndContinue')
#     continueToPaymentBtn.click()



# while not buyButton:
#     try:
#         addToCartBtn = browser.find_element_by_class_name('single_add_to_cart_button')
#         addToCartBtn.click()
#         print("added to cart")
#         buyButton = true
#     except:
#         print("can't buy")
#         time.sleep(5)
