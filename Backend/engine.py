import trafilatura

def get_article(url):
    download = trafilatura.fetch_url(url)
    if download is None:
        return "Error: Unable to fetch the URL."
    text = trafilatura.extract(download)
    return text

if __name__ == "__main__":
    url = "https://www.bbc.co.uk/news/articles/c1kpnxvpgy2o"
    print(get_article(url))