from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Introduction(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Introduction {self.id}"

class LanguageModel(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    prompt_template = models.TextField()
    library = models.CharField(max_length=100)
    tokenizer_type = models.CharField(max_length=100)
    input_cost_per_1k_tokens = models.DecimalField(max_digits=10, decimal_places=4)
    output_cost_per_1k_tokens = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name

class TestRun(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    language_model = models.ForeignKey(LanguageModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.test.name} - {self.language_model.name} - {self.status}"

class Evaluation(models.Model):
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    score = models.FloatField()
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation for {self.test_run}"

class Budget(models.Model):
    date = models.DateField(unique=True)
    daily_limit = models.DecimalField(max_digits=10, decimal_places=2)
    current_usage = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Budget for {self.date}"