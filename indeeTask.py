from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# This is used for disabling the gpu to avoid black screen issue during recording the demo video
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-accelerated-2d-canvas")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized")

# Open the Chrome browser
service = Service(r"C:\Users\Srini\OneDrive\Desktop\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 20)

# Open the Website
driver.get("https://indeedemo-fyc.watch.indee.tv")

# Step 1. Sign in to the Platform by entering the PIN
print("Signing in with PIN")
pin_input = wait.until(EC.visibility_of_element_located((By.ID, "pin")))
pin_input.send_keys("WVMVHWBS")
pin_input.submit()

# Step 2. Navigating to All Titles
time.sleep(5)
project_button = wait.until(EC.visibility_of_element_located(
    (By.XPATH, "//button[@class='brand-card' and @aria-label='All Titles']")))
project_button.click()

# Step 2. Click Test automation project
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "indee-wds-title-card")))
wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//div[contains(@title,'Test automation project')]"))).click()

# Step 3. Playing the video
play_button = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, ".icon-width-gen.wds-cursor-pointer")))
play_button.click()
print("Clicked Play Button")

# Step 3. Searching for the iframe containing the video
print("----> Searching for iframe containing video...")
time.sleep(7)  
iframes = driver.find_elements(By.TAG_NAME, "iframe")
print(f"----> Found {len(iframes)} iframe(s)")

video_found = False
for i, frame in enumerate(iframes):
    driver.switch_to.default_content()
    driver.switch_to.frame(frame)
    try:
        video_present = driver.execute_script("return document.querySelector('video') != null;")
        if video_present:
            print(f"===> Switched to iframe #{i+1} containing video.")
            video_found = True
            break
    except Exception as e:
        continue

if not video_found:
    print("----- Could not find video in any iframe. Exiting.-----")
    driver.quit()
    exit()

# Step 3. video playing for 10secs
time.sleep(10)

# Pause the video
driver.execute_script("""
    const v = document.querySelector('video');
    if (v && !v.paused) {
        v.pause();
        console.log("---> Paused by JS");
    }
""")
print("---> Video paused")

time.sleep(5)

# Step 4. Resume video
driver.execute_script("""
    const v = document.querySelector('video');
    if (v && v.paused) {
        v.play();
        console.log("---> Resumed by JS");
    }
""")
print("===> Video resumed")

time.sleep(10)

# Pause the video
driver.execute_script("""
    const v = document.querySelector('video');
    if (v && !v.paused) {
        v.pause(); 
        console.log("---> Paused by ");
    }
""")
print("---> Video paused")

time.sleep(5)   

# Step 5. Go Back
print("----- Going back twice to exit project -----")
driver.back()
time.sleep(5)
driver.back()

# Step 6. Search for SideBar and Finding the SignOut Button
try:
    sidebar = wait.until(EC.presence_of_element_located((By.ID, "SideBar")))
    ActionChains(driver).move_to_element(sidebar).perform()
    print("===> Hovered over sidebar to expand")
    time.sleep(2) 
except Exception as e:
    print("!!!! Sidebar hover failed:", e)
    driver.quit()
    exit()

# Click Signout Button
try:
    sign_out_btn = wait.until(EC.element_to_be_clickable((By.ID, "signOutSideBar")))
    sign_out_btn.click()
    print("====> Signout clicked successfully")
except Exception as e:
    print("----> Could not click Sign Out:", e)
    driver.quit()
    exit()

# Wait for Sometime 
time.sleep(5)

# Closing the browser
driver.quit()

print("---------------------THANK YOU-----------------------")A