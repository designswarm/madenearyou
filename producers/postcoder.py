import json
import requests


API_URL = "http://api.postcodes.io/postcodes/"


class PostcoderException(Exception):
    pass


class Postcoder(object):

    def geolocate(self, postcode):
        """
        Gets the latitude and longitude of a postcode.
        eg:
            latlon = Postcoder().geolocate('CM8 2BT')

        postcode is a string, the postcode, eg 'CM8 2BT'.

        Returns a dict with 'latitude' and 'longitude' elements.

        Throws PostcoderException if something goes wrong.
        """
        postcode = self._tidy_postcode(postcode)

        response = self._send_request('%s%s' % (API_URL, postcode))

        return {'latitude': response['latitude'],
                'longitude': response['longitude'],
                }

    def _send_request(self, url):
        """
        Sends a request to Postcodes.io and, if all goes well, returns
        a dict of data from the API.

        url is the URL to request data from.
            eg, 'http://api.postcodes.io/postcodes/BS31QP'

        Throws PostcoderException if something goes wrong.
        """

        error_message = ''

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            error_message = "Can't connect to domain."
        except requests.exceptions.Timeout as e:
            error_message = "Connection timed out."
        except requests.exceptions.TooManyRedirects as e:
            error_message = "Too many redirects."
        except requests.exceptions.RequestException as e:
            error_message = "Something went wrong with the request."

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # 4xx or 5xx errors:
            error_message = "HTTP Error: %s" % response.status_code
        except NameError:
            if error_message == '':
                error_message = "Something unusual went wrong."

        if error_message:
            raise PostcoderException(error_message)
        else:
            results = json.loads(response.text)
            if 'result' in results:
                return results['result']
            else:
                raise PostcoderException(
                                    'No result found in Postcoder response.')

    def _tidy_postcode(self, postcode):
        return postcode.replace(' ', '')

