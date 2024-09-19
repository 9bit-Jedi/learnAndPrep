from questions.models import *

def check_answer(question_id, body):

    if body['status'].lower()=='skipped':
        return False
    
    question = Question.objects.get(id=question_id)

    # Single Correct
    if question.type == 'SMCQ':
        answer = AnswerSmcq.objects.get(question_id=question)
        is_correct = True if body['marked_option'] == answer.correct_option else False
        return is_correct

    # Multiple Correct 
    elif question.type == 'MMCQ':
        answer = AnswerMmcq.objects.get(question_id=question)
        is_correct = True
        if body['is_O1_marked'] != answer.is_O1_correct:
            is_correct = False 
        if body['is_O2_marked'] != answer.is_O2_correct:
            is_correct = False 
        if body['is_O3_marked'] != answer.is_O3_correct:
            is_correct = False 
        if body['is_O4_marked'] != answer.is_O4_correct:
            is_correct = False 
        return is_correct

    # Integer type
    elif question.type == 'INT':
        answer = AnswerIntegerType.objects.get(question_id=question)
        is_correct = True if body['marked_answer'] == answer.correct_answer else False
        return is_correct
        
    # Subjective Type 
    elif question.type == 'SUBJ':
        answer = AnswerSubjective.objects.get(question_id=question)
        return True
    
    else:
        print('Invalid question type!')
        raise ValueError('Invalid question type!')