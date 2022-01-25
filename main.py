from selenium import webdriver
import time
import yagmail
import os

def get_driver():
  options=webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches",["enable-automation"])
  options.add_argument("disable-blink-features-AutomationControlled")
  driver=webdriver.Chrome(options=options)
  driver.get("https://www.amazon.com/PF-WaterWorks-PF0989-Disposal-Installation/dp/B078H38Q1M/?th=1")
  return driver
  
def email(value):
  sender="automail.ojas.python@gmail.com"
  receiver="ojasfarm31@gmail.com"
  subject="Amazon product value changed "
  yag=yagmail.SMTP(user=sender,password=os.getenv("PASS"))
  contents=f"""Hey!!
  The product value at Amazon is now: {value}
  Buy Now!!
  https://www.amazon.com/PF-WaterWorks-PF0989-Disposal-Installation/dp/B078H38Q1M/?th=1"""
  yag.send(to=receiver,subject=subject,contents=contents)

def clean_text(text):
    """Extract only the value from text"""
    output =float(text.lstrip('$'))
    return output

def main():
  driver=get_driver()
  time.sleep(2)
  element=driver.find_element(by='xpath',value='//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]')
  data = clean_text(element.text)
  print(data)
  if data<16.35:
    email(element.text)
    print("Mail sent") 
  
main()
