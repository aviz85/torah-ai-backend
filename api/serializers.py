from rest_framework import serializers
from .models import Source, Test, Introduction, LanguageModel, TestRun, Evaluation, Budget

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'content', 'created_at', 'updated_at']

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class IntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introduction
        fields = ['id', 'content', 'created_at', 'updated_at']

class LanguageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageModel
        fields = ['id', 'name', 'api_key', 'prompt_template', 'library', 'tokenizer_type', 
                  'input_cost_per_1k_tokens', 'output_cost_per_1k_tokens']
        extra_kwargs = {'api_key': {'write_only': True}}

    def validate(self, data):
        input_cost = data.get('input_cost_per_1k_tokens')
        output_cost = data.get('output_cost_per_1k_tokens')

        if input_cost is not None and input_cost < 0:
            raise serializers.ValidationError({"input_cost_per_1k_tokens": "Input cost per 1k tokens cannot be negative."})

        if output_cost is not None and output_cost < 0:
            raise serializers.ValidationError({"output_cost_per_1k_tokens": "Output cost per 1k tokens cannot be negative."})

        return data

class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = ['id', 'test', 'language_model', 'status', 'started_at', 'completed_at', 'result', 'cost']

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'test_run', 'score', 'comments', 'created_at']

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'date', 'daily_limit', 'current_usage']