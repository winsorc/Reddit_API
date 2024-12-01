import os
import requests
import praw

reddit = praw.Reddit("bot1")
sub_name = 'UFOs'
subreddit = reddit.subreddit(sub_name)
folder = 'images'
os.makedirs(folder, exist_ok=True)

def check_extension(image_url: str) -> bool:
    extensions = ('.png', '.jpeg', '.gif', '.svg')
    return image_url.lower().endswith(extensions)

def download_image(urls: list, folder = 'images', image_name = sub_name):
    for count, url in enumerate(urls, start=1):
        extension = os.path.splitext(url)[-1].lower()
        if extension not in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
            print(f'Skipping file. Format unsupported: {url}')
            continue
        image_name = os.path.join(folder, f"{sub_name}_{count}{extension}")

        try:
            r = requests.get(url)
            r.raise_for_status()
            with open(image_name, 'wb') as handler:
                handler.write(r.content)
            print(f'Downloaded: {"image_name"} successfully!')
        except Exception as e:
            print(f'Error downloading {url}: {e}')

def get_urls(subreddit: str) -> list:
    urls = []
    for submission in subreddit.hot(limit=100):
        # For gallery posts
        if hasattr(submission, "media_metadata"):
            for item_id, item in submission.media_metadata.items():
                # Check if the item contains the 's' key with a 'u' URL
                if 's' in item and 'u' in item['s']:
                    image_url = item['s']['u']
                    if check_extension(image_url):
                        urls.append(image_url)
                else:
                    print(f"Skipping item {item_id}: Missing 's' or 'u' keys.")
        # For direct image posts
        elif check_extension(submission.url):
            urls.append(submission.url)
    return urls

if __name__ == '__main__':
    image_urls = get_urls(subreddit)
    print(f'Found {len(image_urls)} image URLs.')
    download_image(image_urls, folder, sub_name)
    