from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SourceViewSet,
    TestViewSet,
    IntroductionViewSet,
    LanguageModelViewSet,
    TestRunViewSet,
    EvaluationViewSet,
    BudgetViewSet
)

router = DefaultRouter()
router.register(r'sources', SourceViewSet)
router.register(r'tests', TestViewSet)
router.register(r'introductions', IntroductionViewSet)
router.register(r'language-models', LanguageModelViewSet)
router.register(r'test-runs', TestRunViewSet)
router.register(r'evaluations', EvaluationViewSet)
router.register(r'budgets', BudgetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
