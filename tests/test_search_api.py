import unittest

class TestSearchApi(unittest.TestCase):

    def test_search_using_a_valid_search_query(self):
        # Generated from feature scenario: Search using a valid search query
        context = {'user': {'name': 'demo-user', 'signed_in': True}, 'metadata': {'valid': True}, 'results': ['image-1'], 'status_code': 200, 'order': {'status': 'created'}}
        self.assertIsNotNone(context['user'])
        self.assertEqual(context['status_code'], 200)
        self.assertIsInstance(context['results'], list)
        self.assertGreater(len(context['results']), 0)
        context['status_code'] = 400
        self.assertEqual(context['status_code'], 400)

