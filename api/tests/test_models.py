from django.test import TestCase
from api.models import Source, Test, Introduction, LanguageModel, TestRun, Evaluation, Budget
from django.utils import timezone
from decimal import Decimal

class SourceModelTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="Test Source",
            content="This is a test source content"
        )

    def test_source_creation(self):
        self.assertEqual(self.source.name, "Test Source")
        self.assertEqual(self.source.content, "This is a test source content")
        self.assertTrue(isinstance(self.source, Source))
        self.assertEqual(str(self.source), "Test Source")

class TestModelTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(
            name="Test Model",
            description="This is a test description"
        )

    def test_test_creation(self):
        self.assertEqual(self.test.name, "Test Model")
        self.assertEqual(self.test.description, "This is a test description")
        self.assertTrue(isinstance(self.test, Test))
        self.assertEqual(str(self.test), "Test Model")

class IntroductionModelTest(TestCase):
    def setUp(self):
        self.introduction = Introduction.objects.create(
            content="This is a test introduction"
        )

    def test_introduction_creation(self):
        self.assertEqual(self.introduction.content, "This is a test introduction")
        self.assertTrue(isinstance(self.introduction, Introduction))
        self.assertEqual(str(self.introduction), f"Introduction {self.introduction.id}")

class LanguageModelTest(TestCase):
    def setUp(self):
        self.language_model = LanguageModel.objects.create(
            name="GPT-3",
            api_key="test_api_key",
            prompt_template="This is a test prompt template",
            library="openai",
            tokenizer_type="gpt2",
            input_cost_per_1k_tokens=Decimal("0.0200"),
            output_cost_per_1k_tokens=Decimal("0.0400")
        )

    def test_language_model_creation(self):
        self.assertEqual(self.language_model.name, "GPT-3")
        self.assertEqual(self.language_model.api_key, "test_api_key")
        self.assertEqual(self.language_model.prompt_template, "This is a test prompt template")
        self.assertEqual(self.language_model.library, "openai")
        self.assertEqual(self.language_model.tokenizer_type, "gpt2")
        self.assertEqual(self.language_model.input_cost_per_1k_tokens, Decimal("0.0200"))
        self.assertEqual(self.language_model.output_cost_per_1k_tokens, Decimal("0.0400"))
        self.assertTrue(isinstance(self.language_model, LanguageModel))
        self.assertEqual(str(self.language_model), "GPT-3")

class TestRunModelTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(name="Test Model", description="Test Description")
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

    def test_test_run_creation(self):
        self.assertEqual(self.test_run.test, self.test)
        self.assertEqual(self.test_run.language_model, self.language_model)
        self.assertEqual(self.test_run.status, "pending")
        self.assertTrue(isinstance(self.test_run, TestRun))
        self.assertEqual(str(self.test_run), f"{self.test.name} - {self.language_model.name} - pending")

class EvaluationModelTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(name="Test Model", description="Test Description")
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
            status="completed"
        )
        self.evaluation = Evaluation.objects.create(
            test_run=self.test_run,
            score=0.85,
            comments="This is a test evaluation"
        )

    def test_evaluation_creation(self):
        self.assertEqual(self.evaluation.test_run, self.test_run)
        self.assertEqual(self.evaluation.score, 0.85)
        self.assertEqual(self.evaluation.comments, "This is a test evaluation")
        self.assertTrue(isinstance(self.evaluation, Evaluation))
        self.assertEqual(str(self.evaluation), f"Evaluation for {self.test_run}")

class BudgetModelTest(TestCase):
    def setUp(self):
        self.budget = Budget.objects.create(
            date=timezone.now().date(),
            daily_limit=Decimal("100.00"),
            current_usage=Decimal("50.00")
        )

    def test_budget_creation(self):
        self.assertEqual(self.budget.daily_limit, Decimal("100.00"))
        self.assertEqual(self.budget.current_usage, Decimal("50.00"))
        self.assertTrue(isinstance(self.budget, Budget))
        self.assertEqual(str(self.budget), f"Budget for {self.budget.date}")