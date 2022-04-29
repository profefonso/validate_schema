from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

main_url = 'https://www.linkedin.com' # URL A
tab_url = 'https://www.google.com' # URL B

# Open main window with URL A
browser= webdriver.Chrome('/System/Volumes/Data/Users/alfonsocaro/.wdm/drivers/chromedriver')
browser.get(main_url)


  
# All windows related to driver instance will quit
#print the current url

#print(browser.current_url)
# open tab_url in new window
#browser.execute_script("window.open(tab_url)")
# switch to the new window
#browser.switch_to.window(browser.window_handles[0])
# check if the url is equals to tab_url
#print(browser.current_url)
#if browser.current_url == tab_url:
    #print(browser.current_url + " - Passed.")
    
    #browser.close()
# close the window
#browser.close()