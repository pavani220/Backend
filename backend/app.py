from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.parse
import time
import chromedriver_autoinstaller  # Auto-installs the matching ChromeDriver

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Flask server running!"

@app.route('/send', methods=['POST'])
def send():
    numbers_raw = request.form['numbers']
    message = request.form['message']
    numbers = [num.strip() for num in numbers_raw.split('\n') if num.strip()]

    # Auto-install matching chromedriver
    chromedriver_autoinstaller.install()

    # Headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Modern headless mode
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")

    # Start browser
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com")

    print("⌛ Waiting for QR code login...")
    time.sleep(25)  # Adjust as needed for login time

    for number in numbers:
        try:
            url = f"https://web.whatsapp.com/send?phone={number}&text={urllib.parse.quote(message)}"
            driver.get(url)
            time.sleep(10)  # Wait for chat to load

            send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_button.click()
            print(f"✅ Sent message to {number}")
        except Exception as e:
            print(f"❌ Failed to send to {number}: {str(e)}")
        time.sleep(5)  # Delay between messages

    driver.quit()
    return "✅ Messages sent successfully!"

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
