import requests

if __name__ == "__main__":
    url = "https://registry.verra.org/uiapi/resource/resource/search?$skip=0&count=true&$format=csv&$exportFileName=allprojects.csv"

    headers = {
        "Accept": "text/csv",
        "Content-Type": "application/json",
        "Origin": "https://registry.verra.org",
        "Referer": "https://registry.verra.org/app/search/VCS/All%20Projects",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0",
    }

    data = {
        # same as the JSON payload sent in the POST
        # I can extract this next if you want
    }

    response = requests.post(url, headers=headers, json=data)

    with open("allprojects.csv", "wb") as f:
        f.write(response.content)
