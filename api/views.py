from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Source, Test, Introduction, LanguageModel, TestRun, Evaluation, Budget
from .serializers import (
    SourceSerializer, 
    TestSerializer, 
    IntroductionSerializer, 
    LanguageModelSerializer, 
    TestRunSerializer, 
    EvaluationSerializer, 
    BudgetSerializer
)

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class IntroductionViewSet(viewsets.ModelViewSet):
    queryset = Introduction.objects.all()
    serializer_class = IntroductionSerializer

class LanguageModelViewSet(viewsets.ModelViewSet):
    queryset = LanguageModel.objects.all()
    serializer_class = LanguageModelSerializer

class TestRunViewSet(viewsets.ModelViewSet):
    queryset = TestRun.objects.all()
    serializer_class = TestRunSerializer

    @action(detail=True, methods=['post'])
    def run_test(self, request, pk=None):
        test_run = self.get_object()
        today = timezone.now().date()
        budget = Budget.objects.filter(date=today).first()

        if not budget or budget.current_usage >= budget.daily_limit:
            return Response({"error": "Daily budget exceeded"}, status=status.HTTP_400_BAD_REQUEST)

        # כאן תיישם את הלוגיקה להרצת המבחן
        # זהו מקום להחלפה עם הלוגיקה האמיתית של הרצת המבחן
        test_run.status = 'in_progress'
        test_run.save()

        # עדכן חלק זה עם הלוגיקה האמיתית של הרצת המבחן
        # לעת עתה, נסמן אותו פשוט כהושלם
        test_run.status = 'completed'
        test_run.completed_at = timezone.now()
        test_run.save()

        return Response({"status": "Test run started"}, status=status.HTTP_200_OK)

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        budget = Budget.objects.filter(date=today).first()
        if not budget:
            budget = Budget.objects.create(date=today, daily_limit=0, current_usage=0)
        serializer = self.get_serializer(budget)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_usage(self, request):
        today = timezone.now().date()
        budget = Budget.objects.filter(date=today).first()
        if not budget:
            budget = Budget.objects.create(date=today, daily_limit=0, current_usage=0)
        
        usage = request.data.get('usage', 0)
        budget.current_usage += usage
        budget.save()
        
        serializer = self.get_serializer(budget)
        return Response(serializer.data)