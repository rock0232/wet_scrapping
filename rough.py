import time

from selenium import webdriver

driver = webdriver.Chrome()

# Open the first tab
driver.get("https://uatb2c.cloudd.live")

time.sleep(10)

# Open a new tab
driver.execute_script("window.open('', '_blank');")

# Switch to the new tab
window_handles = driver.window_handles
driver.switch_to.window(window_handles[1])

# Perform actions in the new tab
driver.get("https://devb2c.cloudd.live")

# Switch back to the original tab
driver.switch_to.window(window_handles[0])

# Perform more actions in the original tab if needed
time.sleep(10)
# Close the browser
driver.quit()
