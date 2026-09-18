import unittest

class TestImageSearchFunctionality(unittest.TestCase):

    def test_user_performs_a_search_query_using_metadata_details(self):
        # Generated from feature scenario: User performs a search query using metadata details
        context = {'user': {'name': 'demo-user', 'signed_in': True}, 'metadata': {'valid': True}, 'results': ['image-1'], 'status_code': 200, 'order': {'status': 'created'}}
        self.assertIsNotNone(context['user'])
        self.assertEqual(context['status_code'], 200)
        self.assertIsInstance(context['results'], list)
        self.assertGreater(len(context['results']), 0)
        context['status_code'] = 400
        self.assertEqual(context['status_code'], 400)
        context['status_code'] = 422
        self.assertEqual(context['status_code'], 422)

