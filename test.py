import requests
Text = requests.get("https://captive.apple.com", allow_redirects=True).text
print(Text)
