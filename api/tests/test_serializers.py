from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from api.models import Source, Test, LanguageModel, Introduction, TestRun, Evaluation, Budget
from api.serializers import (
    SourceSerializer, TestSerializer, LanguageModelSerializer,
    IntroductionSerializer, TestRunSerializer, EvaluationSerializer, BudgetSerializer
)
from rest_framework.exceptions import ValidationError

class SourceSerializerTest(TestCase):
    def setUp(self):
        self.source_attributes = {
            'name': 'מקור לדוגמה',
            'content': 'זהו תוכן המקור לדוגמה'
        }
        self.source = Source.objects.create(**self.source_attributes)
        self.serializer = SourceSerializer(instance=self.source)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'content', 'created_at', 'updated_at']))

    def test_content_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['content'], self.source_attributes['content'])

class TestSerializerTest(TestCase):
    def setUp(self):
        self.test_attributes = {
            'name': 'בדיקה לדוגמה',
            'description': 'זהו תיאור הבדיקה לדוגמה'
        }
        self.test = Test.objects.create(**self.test_attributes)
        self.serializer = TestSerializer(instance=self.test)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'description', 'created_at', 'updated_at']))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.test_attributes['name'])

class LanguageModelSerializerTest(TestCase):
    def setUp(self):
        self.language_model_attributes = {
            'name': 'מודל שפה לדוגמה',
            'api_key': 'api_key_123',
            'prompt_template': 'תבנית פרומפט לדוגמה',
            'library': 'ספריה לדוגמה',
            'tokenizer_type': 'סוג טוקנייזר לדוגמה',
            'input_cost_per_1k_tokens': 0.0001,
            'output_cost_per_1k_tokens': 0.0002
        }
        self.language_model = LanguageModel.objects.create(**self.language_model_attributes)
        self.serializer = LanguageModelSerializer(instance=self.language_model)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = set(['id', 'name', 'prompt_template', 'library', 'tokenizer_type', 'input_cost_per_1k_tokens', 'output_cost_per_1k_tokens'])
        self.assertEqual(set(data.keys()), expected_fields)

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.language_model_attributes['name'])

    def test_api_key_write_only(self):
        serializer = LanguageModelSerializer()
        self.assertTrue(serializer.fields['api_key'].write_only)

class IntroductionSerializerTest(TestCase):
    def setUp(self):
        self.introduction_attributes = {
            'content': 'זוהי הקדמה לדוגמה'
        }
        self.introduction = Introduction.objects.create(**self.introduction_attributes)
        self.serializer = IntroductionSerializer(instance=self.introduction)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'content', 'created_at', 'updated_at']))

    def test_content_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['content'], self.introduction_attributes['content'])

class TestRunSerializerTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(name='בדיקה', description='תיאור הבדיקה')
        self.language_model = LanguageModel.objects.create(
            name='מודל שפה',
            api_key='api_key_123',
            prompt_template='תבנית פרומפט',
            library='ספריה',
            tokenizer_type='סוג טוקנייזר',
            input_cost_per_1k_tokens=Decimal('0.0001'),
            output_cost_per_1k_tokens=Decimal('0.0002')
        )
        self.test_run_attributes = {
            'test': self.test,
            'language_model': self.language_model,
            'status': 'pending',
            'started_at': timezone.now(),
            'completed_at': None,
            'result': None,
            'cost': None
        }
        self.test_run = TestRun.objects.create(**self.test_run_attributes)
        self.serializer = TestRunSerializer(instance=self.test_run)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = set(['id', 'test', 'language_model', 'status', 'started_at', 'completed_at', 'result', 'cost'])
        self.assertEqual(set(data.keys()), expected_fields)

    def test_status_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['status'], self.test_run_attributes['status'])

    def test_invalid_status(self):
        invalid_data = self.test_run_attributes.copy()
        invalid_data['status'] = 'invalid_status'
        serializer = TestRunSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class EvaluationSerializerTest(TestCase):
    def setUp(self):
        test = Test.objects.create(name='בדיקה', description='תיאור הבדיקה')
        language_model = LanguageModel.objects.create(
            name='מודל שפה',
            api_key='api_key_123',
            prompt_template='תבנית פרומפט',
            library='ספריה',
            tokenizer_type='סוג טוקנייזר',
            input_cost_per_1k_tokens=Decimal('0.0001'),
            output_cost_per_1k_tokens=Decimal('0.0002')
        )
        test_run = TestRun.objects.create(test=test, language_model=language_model, status='completed')
        self.evaluation_attributes = {
            'test_run': test_run,
            'score': 0.85,
            'comments': 'הערות לדוגמה'
        }
        self.evaluation = Evaluation.objects.create(**self.evaluation_attributes)
        self.serializer = EvaluationSerializer(instance=self.evaluation)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = set(['id', 'test_run', 'score', 'comments', 'created_at'])
        self.assertEqual(set(data.keys()), expected_fields)

    def test_score_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['score'], self.evaluation_attributes['score'])

    def test_invalid_score(self):
        invalid_data = self.evaluation_attributes.copy()
        invalid_data['score'] = 2.0  # ציון לא חוקי
        serializer = EvaluationSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class BudgetSerializerTest(TestCase):
    def setUp(self):
        self.budget_attributes = {
            'date': timezone.now().date(),
            'daily_limit': Decimal('100.00'),
            'current_usage': Decimal('50.00')
        }
        self.budget = Budget.objects.create(**self.budget_attributes)
        self.serializer = BudgetSerializer(instance=self.budget)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = set(['id', 'date', 'daily_limit', 'current_usage'])
        self.assertEqual(set(data.keys()), expected_fields)

    def test_daily_limit_field_content(self):
        data = self.serializer.data
        self.assertEqual(Decimal(data['daily_limit']), self.budget_attributes['daily_limit'])

    def test_current_usage_field_content(self):
        data = self.serializer.data
        self.assertEqual(Decimal(data['current_usage']), self.budget_attributes['current_usage'])

    def test_invalid_negative_daily_limit(self):
        invalid_data = self.budget_attributes.copy()
        invalid_data['daily_limit'] = Decimal('-100.00')
        serializer = BudgetSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_negative_current_usage(self):
        invalid_data = self.budget_attributes.copy()
        invalid_data['current_usage'] = Decimal('-50.00')
        serializer = BudgetSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class SourceSerializerValidationTest(TestCase):
    def test_empty_name(self):
        invalid_data = {'name': '', 'content': 'תוכן תקין'}
        serializer = SourceSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_empty_content(self):
        invalid_data = {'name': 'שם תקין', 'content': ''}
        serializer = SourceSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class TestSerializerValidationTest(TestCase):
    def test_empty_name(self):
        invalid_data = {'name': '', 'description': 'תיאור תקין'}
        serializer = TestSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_empty_description(self):
        invalid_data = {'name': 'שם תקין', 'description': ''}
        serializer = TestSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class LanguageModelSerializerValidationTest(TestCase):
    def test_negative_input_cost(self):
        invalid_data = {
            'name': 'מודל שפה',
            'api_key': 'api_key_123',
            'prompt_template': 'תבנית פרומפט',
            'library': 'ספריה',
            'tokenizer_type': 'סוג טוקנייזר',
            'input_cost_per_1k_tokens': Decimal('-0.0001'),
            'output_cost_per_1k_tokens': Decimal('0.0002')
        }
        serializer = LanguageModelSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertIn('input_cost_per_1k_tokens', str(context.exception))

    def test_negative_output_cost(self):
        invalid_data = {
            'name': 'מודל שפה',
            'api_key': 'api_key_123',
            'prompt_template': 'תבנית פרומפט',
            'library': 'ספריה',
            'tokenizer_type': 'סוג טוקנייזר',
            'input_cost_per_1k_tokens': Decimal('0.0001'),
            'output_cost_per_1k_tokens': Decimal('-0.0002')
        }
        serializer = LanguageModelSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertIn('output_cost_per_1k_tokens', str(context.exception))