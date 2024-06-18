from django.test import TestCase

# Create your tests here.

from quiz.models import Quiz, QuizQuestion
from questions.models import Chapter, Question

chapter_id = Chapter.objects.get(id='MA19')

module_total_questions = Question.objects.filter(chapter_id=chapter_id, type='MODULE').count()


question = Question.objects.get(id='MA19002')
quiz_question = QuizQuestion.objects.get(question_id=question)

answer_id = quiz_question.question_id.question_answer.first()