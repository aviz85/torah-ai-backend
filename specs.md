# אפיון מערכת להערכת מודלי שפה בהקשר של מקורות תורניים

## תיאור כללי

המערכת המתוארת היא פלטפורמה שיתופית להערכת יכולות של מודלי שפה בהבנת מקורות תורניים ביהדות. המערכת מאפשרת למשתמשים להעלות מקורות, ליצור מבחנים, להוסיף הקדמות, ולהריץ מבחנים על מודלי שפה שונים. התוצאות מאפשרות השוואה בין מודלים ובחינת השפעת הקדמות על ביצועי המודלים.

## מרכיבי המערכת העיקריים

1. **מקורות**: טקסטים תורניים מסוגים שונים.
2. **מבחנים**: שאלות סגורות או פתוחות על המקורות.
3. **הקדמות**: מידע נוסף להבנת המקורות.
4. **מודלי שפה**: מודלים שונים שניתן לבחון את ביצועיהם.
5. **משתמשים**: בעלי תפקידים שונים במערכת.

## תהליכי עבודה עיקריים

1. העלאת מקורות
2. יצירת מבחנים
3. הוספת הקדמות
4. הרצת מבחנים על מודלים
5. בדיקת תוצאות (עבור שאלות פתוחות)
6. ניתוח וצפייה בסטטיסטיקות

## ארכיטקטורה טכנית

### Backend (Django)

#### Models

```python:backend/models.py
from django.db import models
from django.contrib.auth.models import User

class Source(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=5000)
    tags = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Test(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('closed', 'Closed'), ('open', 'Open')])
    questions = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Introduction(models.Model):
    content = models.TextField()
    sources = models.ManyToManyField(Source)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class LanguageModel(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    prompt_template = models.TextField()
    library = models.CharField(max_length=100)  # e.g., 'openai', 'anthropic', etc.
    tokenizer_type = models.CharField(max_length=100)  # e.g., 'gpt2', 'cl100k_base', etc.
    input_cost_per_1k_tokens = models.DecimalField(max_digits=10, decimal_places=4)
    output_cost_per_1k_tokens = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name

class TestRun(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    language_model = models.ForeignKey(LanguageModel, on_delete=models.CASCADE)
    introductions = models.ManyToManyField(Introduction)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ])
    result = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class Evaluation(models.Model):
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Views

```python:backend/views.py
from django.shortcuts import render
from rest_framework import viewsets
from .models import Source, Test, Introduction, LanguageModel, TestRun, Evaluation
from .serializers import SourceSerializer, TestSerializer, IntroductionSerializer, LanguageModelSerializer, TestRunSerializer, EvaluationSerializer

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

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

# יש להוסיף views נוספים לפי הצורך, כגון לסטטיסטיקות ודוחות
```

#### URLs

```python:backend/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SourceViewSet, TestViewSet, IntroductionViewSet, LanguageModelViewSet, TestRunViewSet, EvaluationViewSet

router = DefaultRouter()
router.register(r'sources', SourceViewSet)
router.register(r'tests', TestViewSet)
router.register(r'introductions', IntroductionViewSet)
router.register(r'language-models', LanguageModelViewSet)
router.register(r'test-runs', TestRunViewSet)
router.register(r'evaluations', EvaluationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # יש להוסיף נתיבים נוספים לפי הצורך
]
```

### Frontend (React)

#### מסכים עיקריים

1. דף הבית
2. רשימת מקורות
3. יצירה/עריכת מקור
4. רשימת מבחנים
5. יצירה/עריכת מבחן
6. רשימת הקדמות
7. יצירה/עריכת הקדמה
8. הרצת מבחן
9. הערכת תוצאות מבחן
10. דוחות וסטטיסטיקות

## ייצוא נתונים

המערכת תאפשר ייצוא נתונים בפורמטים הבאים:
- CSV
- JSON
- Excel

## אנליטיקות

המערכת תספק אנליטיקות מגוונות, כולל:

1. השוואת ביצועים בין מודלי שפה שונים
2. ניתוח השפעת הקדמות על ביצועי המודלים
3. ביצועים לפי סוגי מקורות (על פי תגיות)
4. מגמות שיפור או הידרדרות בביצועי מודלים לאורך זמן
5. סטטיסטיקות משתמשים (תרומות, פעילות)

## אבטחה ופרטיות

1. הרשאות משתמשים מדורגות
2. הצפנת מידע רגיש (כגון מפתחות API)
3. תיעוד פעולות משתמשים

## סיכום

מערכת זו מספקת פלטפורמה מקיפה להערכת יכולות מודלי שפה בהקשר של מקורות תורניים. היא מאפשרת שיתוף פעולה בין משתמשים, ניהול מקורות ומבחנים, והפקת תובנות משמעותיות על ביצועי המודלים השונים.