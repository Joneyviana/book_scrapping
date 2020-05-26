import time

import requests

import config


def initiateCaptchaRequest(apiKey,siteKey,url):
    print("usando url: "+url)
    formData = {
    "method": 'userrecaptcha',
    "googlekey":siteKey,
    "key":apiKey,
     "pageurl":url,
    "json": 1}
    response = requests.post('http://2captcha.com/in.php',formData)
    print("returning requestId:"+response.json()["request"])
    return response.json()["request"]


def requestCaptchaResults(apiKey, requestId):
    print("using requestID: "+requestId)
    json = requests.get("http://2captcha.com/res.php?key={0}&action=get&id={1}&json=1".format(apiKey,requestId)).json()
    print("tentando passar pelo captcha")
    while(json["status"] == 0):
        json = requests.get(
            "http://2captcha.com/res.php?key={0}&action=get&id={1}&json=1".format(apiKey, requestId)).json()
        print("tentando passar pelo captcha")
        time.sleep(5)

    return json["request"]

if __name__ == '__main__':
    print(initiateCaptchaRequest(config.apiKey,config.siteKey,"https://asdfiles.com/26poh?pt=Y0VGQlJUTnVSMUpIYW1welZrc3pRelJtUlVkR1FUMDlPaDh1QlJBMWsrbUdYMTcwakhiWkMyOD0%3D"))

