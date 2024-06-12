from rest_framework import serializers
from .models import Test, LiveTest, TestAttempt, TestQuestion
  
# your serializers here
  
class TestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Test
    fields = ('__all__')

class TestAttemptSerializer(serializers.ModelSerializer):
  # user_id = UserSerializer()
  test_id = TestSerializer()
  
  class Meta:
    model = TestAttempt
    fields = ('__all__')