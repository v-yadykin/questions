from rest_framework import serializers
from questions_api import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'tg_login', 'tg_name', 'type')

    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'
        read_only_fields = ('created_on', 'resource_id')


class GetResourceSerializer(serializers.Serializer):
    model = models.Question
    
    question_id = serializers.IntegerField()
    batch_start = serializers.IntegerField(min_value=0)
    batch_size = serializers.IntegerField(min_value=1)
        
    def __init__(self, **kwargs):
        self.question = None
        super().__init__(**kwargs)

    def validate_question_id(self, value):

        try:
            self.question = self.model.objects.get(id=value)
        except self.model.DoesNotExist:
            raise serializers.ValidationError("Question not found")
        
        return value