import webbrowser; import pyperclip as clip; urls = ["http://127.0.0.1:5001/"]; [webbrowser.get('open -a /Applications/Google\ Chrome.app %s').open(str(url) if str(url).startswith("http") else "https://" + str(url)) for url in urls]