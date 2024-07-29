from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Source, Test, LanguageModel, TestRun
from decimal import Decimal

class SourceViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.source = Source.objects.create(name="Test Source", content="Test content")
        self.url = reverse('source-detail', kwargs={'pk': self.source.pk})
        self.list_url = reverse('source-list')

    def test_get_valid_single_source(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_source(self):
        response = self.client.get(reverse('source-detail', kwargs={'pk': 30000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_source(self):
        data = {"name": "New Source", "content": "New content"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test = Test.objects.create(name="Sample Test", description="Test description")
        self.url = reverse('test-detail', kwargs={'pk': self.test.pk})
        self.list_url = reverse('test-list')

    def test_get_valid_single_test(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_test(self):
        response = self.client.get(reverse('test-detail', kwargs={'pk': 30000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_test(self):
        data = {"name": "New Test", "description": "New test description"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestRunViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test = Test.objects.create(name="Sample Test", description="Test description")
        self.language_model = LanguageModel.objects.create(
            name="GPT-3",
            api_key="test_api_key",
            prompt_template="Test template",
            library="openai",
            tokenizer_type="gpt2",
            input_cost_per_1k_tokens=Decimal("0.0200"),
            output_cost_per_1k_tokens=Decimal("0.0400")
        )
        self.test_run = TestRun.objects.create(
            test=self.test,
            language_model=self.language_model,
            status="pending"
        )
        self.url = reverse('testrun-detail', kwargs={'pk': self.test_run.pk})
        self.list_url = reverse('testrun-list')

    def test_get_valid_single_test_run(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_test_run(self):
        response = self.client.get(reverse('testrun-detail', kwargs={'pk': 30000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_test_run(self):
        data = {
            "test": self.test.id,
            "language_model": self.language_model.id,
            "status": "pending"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)