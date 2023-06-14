from rest_framework import serializers
from home.models import Question, Answer


class UsernameEmailRelationfield(serializers.RelatedField):
    def to_representation(self, value):
        return '{} - {}'.format(value.username, value.email)


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    email = serializers.EmailField()


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True) # show __str__ method of object
    # user = serializers.SlugRelatedField(read_only=True, slug_field='email') # show any of object's fields you want
    # user = UsernameEmailRelationfield(read_only=True)   # custom related serializer
    
    class Meta:
        model = Question
        fields = ['user', 'title', 'text', 'answers']

    def get_answers(self, obj):
        results = obj.answer.all()
        return AnswerSerializer(instance=results, many=True).data

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'