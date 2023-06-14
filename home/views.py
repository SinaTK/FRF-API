from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from home.models import Person, Question, Answer
from home.serializers import PersonSerializer, QuestionSerializer, AnswerSerializer
from permissions import IsOwnerorReadonly

class Home(APIView):
    """
    show list of peoples
    """
    # permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer

    def get(self, request):
        persons = Person.objects.all()
        ser_data = PersonSerializer(instance=persons, many=True)
        return Response(data=ser_data.data)
    
    def post(self, request):
        srz_data = PersonSerializer(data=request.POST)
        if srz_data.is_valid():
            c_data = srz_data.validated_data
            Person.objects.create(id=c_data['id'], name=c_data['name'], age=c_data['age'], email=c_data['email'])
            return Response(srz_data.data, status.HTTP_201_CREATED)
        
        return Response(srz_data.errors, status.HTTP_400_BAD_REQUEST)


class QuestionsListView(APIView):
    serializer_class = QuestionSerializer
    def get(self, request):
        questions = Question.objects.all()
        ser_data = QuestionSerializer(instance=questions, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class QuestionsCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer
    def post(self, request):
        ser_data = QuestionSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status.HTTP_201_CREATED)
        else:
            return Response(ser_data.errors, status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    permission_classes = [IsOwnerorReadonly]
    serializer_class = QuestionSerializer
    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        ser_data = QuestionSerializer(instance=question, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status.HTTP_200_OK)
        else:
            return Response(ser_data.errors, status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    permission_classes = [IsOwnerorReadonly]
    serializer_class = QuestionSerializer
    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        question.delete()
        return Response({'message': 'Question deleted seccussfully.'}, status.HTTP_200_OK)