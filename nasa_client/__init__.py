import json
from urllib import request


class NasaPictureOfTheDay(object):
    """
    Data object representing result of NASA apod API
    """

    def __init__(self, copyright=None, explanation=None, hd_url=None, media_type=None, service_version=None, title=None,
                 url=None):
        self.copyright = copyright
        self.explanation = explanation
        self.hd_url = hd_url
        self.media_type = media_type
        self.service_version = service_version
        self.title = title
        self.url = url

    def __str__(self):
        return 'copyright = %s, explanation = %s, hd_url = %s, media_type = %s, service_version = %s, title = %s, url = %s' % (
            self.copyright, self.explanation, self.hd_url, self.media_type, self.service_version, self.title, self.url)


class NasaClient(object):
    def get_picture_of_the_day(self) -> NasaPictureOfTheDay:
        """
        Get picture of the day from NASA using the DEMO_KEY, api definition here: https://api.nasa.gov/api.html#apod
        :return: The src of the picture of the day
        """
        req = request.Request(url='https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')

        try:
            with request.urlopen(req, timeout=10) as resp:
                result = resp.read()
                return json.loads(result, object_hook=lambda j: NasaPictureOfTheDay(copyright=j['copyright'],
                                                                                    explanation=j['explanation'],
                                                                                    hd_url=j['hdurl'],
                                                                                    media_type=j['media_type'],
                                                                                    service_version=j[
                                                                                        'service_version'],
                                                                                    title=j['title'],
                                                                                    url=j['url']))
        except Exception as e:
            print(e)
            """
            If cannot get picture of the day from NASA api, then use the 404.jpg from http.cat
            """
            pic_404 = NasaPictureOfTheDay()
            pic_404.title = 'You can\'t see me, Meow~~!'
            pic_404.url = 'https://http.cat/404.jpg'
            pic_404.explanation = 'Failed to get picture of the day from NASA api, so here is a little cute cat for you, see you tomorrow!'
            return pic_404
