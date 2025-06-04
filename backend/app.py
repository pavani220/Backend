from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.parse
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Flask server running!"

@app.route('/send', methods=['POST'])
def send():
    numbers_raw = request.form['numbers']
    message = request.form['message']
    numbers = [num.strip() for num in numbers_raw.split('\n') if num.strip()]

    # Configure headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Chrome binary path on Render

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://web.whatsapp.com")
    print("Waiting for QR code login...")
    time.sleep(25)  # Give user time to scan QR

    for number in numbers:
        try:
            url = f"https://web.whatsapp.com/send?phone={number}&text={urllib.parse.quote(message)}"
            driver.get(url)
            time.sleep(10)

            send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_button.click()
            print(f"✅ Sent message to {number}")
        except Exception as e:
            print(f"❌ Failed to send to {number}: {str(e)}")
        time.sleep(5)

    driver.quit()
    return "✅ Messages sent successfully!"

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
