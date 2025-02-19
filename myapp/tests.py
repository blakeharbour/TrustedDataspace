from django.test import TestCase

class SampleTestCase(TestCase):
    def test_example(self):
        # 这是一个简单的测试用例
        self.assertEqual(1 + 1, 2)

    def test_home_page(self):
        # 测试首页是否可以访问
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)