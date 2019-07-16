import re
import unittest
from unittest.mock import patch

import requests

from melisdk import Meli


class MeliTest(unittest.TestCase):

    def setUp(self):
        self.CLIENT_ID = "123"
        self.CLIENT_SECRET = "a secret"
        self.ACCESS_TOKEN = "a access_token"
        self.REFRESH_TOKEN = "a refresh_token"
        self.NEW_ACCESS_TOKEN = "a new access_token"
        self.NEW_REFRESH_TOKEN = "a new refresh_token"
        self.meli = Meli(client_id=self.CLIENT_ID,
                         client_secret=self.CLIENT_SECRET,
                         access_token=self.ACCESS_TOKEN,
                         refresh_token=self.REFRESH_TOKEN)

    def testClientId(self):
        self.assertEqual(self.meli.client_id, self.CLIENT_ID)

    def testClientSecret(self):
        self.assertEqual(self.meli.client_secret, self.CLIENT_SECRET)

    def testAccessToken(self):
        self.assertEqual(self.meli.access_token, self.ACCESS_TOKEN)

    def testRefreshToken(self):
        self.assertEqual(self.meli.refresh_token, self.REFRESH_TOKEN)

    def testAuthUrl(self):
        callback = "http://test.com/callback"
        self.assertTrue(re.search("^http",
                                  self.meli.auth_url(redirect_URI=callback)))
        self.assertTrue(re.search(
            "^https\:\/\/auth\.mercadolibre\.com\.[a-zA-Z]*\/authorization",
            self.meli.auth_url(redirect_URI=callback)))
        self.assertTrue(re.search("redirect_uri",
                                  self.meli.auth_url(redirect_URI=callback)))
        self.assertTrue(re.search(self.CLIENT_ID,
                                  self.meli.auth_url(redirect_URI=callback)))
        self.assertTrue(re.search("response_type",
                                  self.meli.auth_url(redirect_URI=callback)))

    @patch('melisdk.meli.Meli.get')
    def testGet(self, meli_get):
        meli_get.return_value.status_code = 200
        response = self.meli.get(path="/items/test1", timeout=5)
        self.assertEqual(response.status_code, requests.codes.ok)

    @patch('melisdk.meli.Meli.post')
    def testPost(self, meli_post):
        body = {"condition": "new", "warranty": "60 dias",
                "currency_id": "BRL", "accepts_mercadopago": True,
                "description": "Lindo Ray_Ban_Original_Wayfarer",
                "listing_type_id": "bronze",
                "title": "oculos Ray Ban Aviador  Que Troca As Lentes  Lancamento!",
                "available_quantity": 64, "price": 289,
                "subtitle": "Acompanha 3 Pares De Lentes!! Compra 100% Segura",
                "buying_mode": "buy_it_now", "category_id": "MLB5125",
                "pictures": [{"source": "http://upload.wikimedia.org/wikipedia/commons/f/fd/Ray_Ban_Original_Wayfarer.jpg"},
                             {"source": "http://en.wikipedia.org/wiki/File:Teashades.gif"}]}
        meli_post.return_value.status_code = 200
        response = self.meli.post(
            path="/items", body=body,
            params={'access_token': self.meli.access_token})
        self.assertEqual(response.status_code, requests.codes.ok)

    @patch('melisdk.meli.Meli.put')
    def testPut(self, meli_put):
        body = {"title": "oculos edicao especial!", "price": 1000}
        meli_put.return_value.status_code = 200
        response = self.meli.put(
            path="/items/test1", body=body,
            params={'access_token': self.meli.access_token}, timeout=5)
        self.assertEqual(response.status_code, requests.codes.ok)

    @patch('melisdk.meli.Meli.delete')
    def testDelete(self, meli_delete):
        meli_delete.return_value.status_code = 200
        response = self.meli.delete(
            path="/questions/123",
            params={'access_token': self.meli.access_token}, timeout=5)
        self.assertEqual(response.status_code, requests.codes.ok)

    @patch('melisdk.meli.Meli.get')
    def testWithoutAccessToken(self, meli_get):
        meli_get.return_value.status_code = 403
        response = self.meli.get(path="/users/me")
        self.assertEqual(response.status_code, requests.codes.forbidden)

    @patch('melisdk.meli.Meli.get')
    def testWithAccessToken(self, meli_get):
        meli_get.return_value.status_code = 200
        response = self.meli.get(
            path="/users/me",
            params={'access_token': self.meli.access_token})
        self.assertEqual(response.status_code, requests.codes.ok)

    @patch('melisdk.meli.Meli.get_refresh_token')
    def testDoRefreshToken(self, meli_refresh_token):
        meli_refresh_token.return_value = self.NEW_ACCESS_TOKEN
        new_access_token = self.meli.get_refresh_token()
        self.assertIsInstance(new_access_token, str)
        self.assertEqual(new_access_token, self.NEW_ACCESS_TOKEN)

    @patch('melisdk.meli.Meli.authorize')
    def testAuthorize(self, meli_authorize):
        self.meli.access_token = None
        self.meli.refresh_token = None
        meli_authorize.return_value.status_code = 403
        response = self.meli.authorize(code="a code from get param",
                                       redirect_URI="A redirect Uri")
        self.assertNotEqual(self.meli.access_token, self.ACCESS_TOKEN)
        self.assertNotEqual(self.meli.refresh_token, self.REFRESH_TOKEN)
        self.assertEqual(response.status_code, requests.codes.forbidden)


if __name__ == '__main__':
    unittest.main()
