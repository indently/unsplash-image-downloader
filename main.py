import requests as rq
from bs4 import BeautifulSoup as bs
import image_downloader as im_do


def download_images(search_term: str = 'cat'):
    # Get html from Unsplash
    request = rq.get(f'https://unsplash.com/s/photos/{search_term}')
    html = request.content

    # Convert it into something beautifulsoups can understand
    soup = bs(html, features='html.parser')

    # Grab all the images from the html
    links = soup.findAll(itemprop="image")

    image_urls, image_ids = [], []
    for image in links:
        elements = str(image).split()
        for element in elements:
            if 'https://images.unsplash.com/photo' in element:
                if 'src' in element:
                    continue

                # Grab unique identifiers for each image
                position = element.find('photo-') + 6
                end_position = element.find('ixlib=rb')
                image_id = (element[position:end_position])
                # print(image_id)

                # Avoid downloading duplicates by checking the ids for each image
                if image_id not in image_ids:
                    image_ids.append(image_id)
                    image_urls.append(element)

    return image_urls


def get_images(term: str, amount: int):
    images = download_images(search_term=term)[:amount]

    for i, url in enumerate(images):
        im_do.save_image('downloads/', f'{term}-{i}', url)


if __name__ == '__main__':
    get_images(term='cats', amount=1)
