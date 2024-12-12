from django.test import TestCase, Client
from django.urls import reverse

client = Client()

class SimpleTestCases(TestCase):
    def test_ping(self):
        print("TEST PING\n")
        response = client.get(reverse('ping'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'pong')


class APITests(TestCase):
    def test_get_most_recent_ten(self):
        print("TEST GET MOST RECENT TEN\n")
        response = client.get(reverse('get_most_recent_ten'))
        self.assertEqual(len(response.json()), 10)

    def test_get_most_recent_ten_dev(self):
        print("TEST GET MOST RECENT TEN DEV\n")
        response = client.get(reverse('get_most_recent_ten_dev'))
        self.assertEqual(len(response.json()), 10)

    def test_result_contains_thumbnail(self):
        print("TEST RESULT CONTAINS THUMBNAIL\n")
        response = client.get(reverse('get_most_recent_ten'))
        entities = response.json()
        entity = entities[0]

        self.assertIs('thumbnail_url' in entity, True)

    def test_result_contains_images(self):
        print("TEST RESULT CONTAINS IMAGES\n")
        response = client.get(reverse('get_most_recent_ten'))
        entities = response.json()
        entity = entities[0]

        self.assertIs('images' in entity, True)
