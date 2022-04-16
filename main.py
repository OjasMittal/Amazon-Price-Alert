from selenium import webdriver
import time
import yagmail
import os
from twilio.rest import Client



urll=input("Enter the url of the amazon site: ")
price =float(input("Enter the price below which you want to but it: "))
id=input("Enter your email: ")
no=input("Enter mobile using +country code, eg: +91 : ")
def get_driver():
  options=webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches",["enable-automation"])
  options.add_argument("disable-blink-features-AutomationControlled")
  driver=webdriver.Chrome(options=options)
  driver.get(urll)
  return driver
  
def email(value):
  sender="automail.ojas.python@gmail.com"
  receiver=id
  subject="Amazon product value changed "
  yag=yagmail.SMTP(user=sender,password=os.getenv("PASS"))
  contents=f"""Hey!!
  The product value at Amazon is now: {value}
  Buy Now!!
  {urll}"""
  yag.send(to=receiver,subject=subject,contents=contents)

def clean_text(text):
    """Extract only the value from text"""
    
    output =float(text.lstrip('$'))
    return output


def send_sms(value):
  account_sid = os.environ['TWILIO_ACCOUNT_SID']
  auth_token = os.environ['TWILIO_AUTH_TOKEN']
  client = Client(account_sid, auth_token)

  message = client.messages \
                .create(
                     body=f"""Hey!!
  The product value at Amazon is now: {value}
  Buy Now!!
  {urll}
                     """,
                     from_='+16203159923',
                     to=no
                 )

  print(message.sid)    

def main():
  driver=get_driver()
  time.sleep(2)
  element=driver.find_element(by='xpath',value='//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]')

  data = clean_text(element.text)
  print(data)
  while True:
    if data<price:
      email(element.text)
      send_sms(element.text)
      print("Mail sent")
      break
    else: 
      print("Price is high now! ")
      print("You will receive an email and a SMS when price will go down")
      time.sleep(3600)
  
main()
