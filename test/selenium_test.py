from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

# Flask 서버 접속 (Render 배포된 도메인)
driver.get("https://www.example.com")

# 로그인 시도
driver.find_element(By.NAME, "username").send_keys("user")
driver.find_element(By.NAME, "password").send_keys("userpass")
driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

time.sleep(2)

# JWT 토큰 확인 (쿠키에서 가져오기)
token = driver.get_cookie("access_token")["value"]
print("[+] JWT Token:", token)

driver.quit()
