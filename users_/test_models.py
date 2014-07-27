from unittest import TestCase
from django.contrib.auth.hashers import make_password
from django.core import management

from models import *


class ModelsTest(TestCase):

    def setUp(self):
        management.call_command('loaddata', 'fixtures.json',
                                interactive=False)

    def tearDown(self):
        management.call_command('flush', interactive=False)

    def test_create_delete_UserProfile(self):
        user = User(username='test_man2', password=make_password('qwe123'),
                    is_superuser=False, email='test@test.pl')
        user.save()
        assert user.id is not None
        userprofile = UserProfile(user=user, userlvl=0)
        userprofile.save()
        assert userprofile.id is not None
        assert userprofile.userlvl == 0
        userprofile.delete()
        assert userprofile.id is None

    def test_create_delete_Tests(self):
        test = Tests(title='First Test')
        test.save()
        assert test.id is not None
        test.delete()
        assert test.id is None

    def test_create_delete_Questions(self):
        test = Tests.objects.get(title='FIRST TEST')
        question = Questions(question='test question', test=test)
        question.save()
        assert question.id is not None
        question.delete()
        assert question.id is None

    def test_create_delete_Answers(self):
        test = Tests.objects.get(title='FIRST TEST')
        question = Questions(question='test question', test=test)
        question.save()
        answer = Answers(answer='test answer', correct=False,
                         question=question)
        answer.save()
        assert answer.id is not None
        answer.delete()
        assert answer.id is None

    def test_delete_recursivly_Questions(self):
        test = Tests(title='OWN TEST')
        test.save()
        question = Questions(question='test question', test=test)
        question.save()
        answers_id = []
        answer = Answers(answer='test answer', correct=False,
                         question=question)
        answer.save()
        answer1 = Answers(answer='test answer2', correct=False,
                          question=question)
        answer1.save()
        answer2 = Answers(answer='test answer3', correct=False,
                          question=question)
        answer2.save()
        assert answer.id and answer1.id and answer2.id is not None
        answers_id.append(answer.id)
        answers_id.append(answer1.id)
        answers_id.append(answer2.id)
        question.delete()
        answers = Answers.objects.filter(id__in=answers_id).count()
        assert answers == 0

    def test_delete_recursivly_Tests(self):
        test = Tests(title='OWN TEST')
        test.save()
        questions_id = []
        answers_id = []
        
        question = Questions(question='test question', test=test)
        question.save()
        questions_id.append(question.id)
        answer = Answers(answer='test answer 1', correct=False,
                         question=question)
        answer.save()
        answer1 = Answers(answer='test answer 2', correct=True,
                          question=question)
        answer1.save()
        answer2 = Answers(answer='test answer 3', correct=False,
                          question=question)
        answer2.save()
        assert answer.id and answer1.id and answer2.id is not None
        answers_id.append(answer.id)
        answers_id.append(answer1.id)
        answers_id.append(answer2.id)

        question2 = Questions(question='test question2', test=test)
        question2.save()
        questions_id.append(question2.id)
        answer = Answers(answer='test answer 4', correct=False,
                         question=question2)
        answer.save()
        answer1 = Answers(answer='test answer 5', correct=False,
                          question=question2)
        answer1.save()
        answer2 = Answers(answer='test answer 6', correct=False,
                          question=question2)
        answer2.save()
        assert answer.id and answer1.id and answer2.id is not None
        answers_id.append(answer.id)
        answers_id.append(answer1.id)
        answers_id.append(answer2.id)
        
        test.delete()
        test.id
        questions = Questions.objects.filter(id__in=questions_id).count()
        assert questions == 0
        answers = Answers.objects.filter(id__in=answers_id).count()
        assert answers == 0

    def test_Tests_dict(self):
        test = Tests.objects.get(title='FIRST TEST')
        test_dict = test.dict()
        assert len(test_dict['questions']) == 1
        assert len(test_dict['questions'][0]['answers']) == 3

    def test_Questions_dict(self):
        # Proper question with at least 2 answers and one of them is correct
        test = Tests.objects.get(title='FIRST TEST')
        question = Questions.objects.get(test=test, question="FIRST QUESTION")
        question_dict = question.dict()
        answers = Answers.objects.filter(question=question)
        assert answers.count() == 3
        assert len(question_dict['answers']) == 3

        # Unproper question with 3 answers but none of them is correct
        test = Tests.objects.get(title='FIRST TEST')
        question = Questions.objects.get(test=test, question="SECOND QUESTION")
        question_dict = question.dict()
        answers = Answers.objects.filter(question=question)
        assert answers.count() == 3
        assert len(question_dict['answers']) == 0

        # Unproper question with 1
        test = Tests.objects.get(title='FIRST TEST')
        question = Questions.objects.get(test=test, question="THIRD QUESTION")
        question_dict = question.dict()
        answers = Answers.objects.filter(question=question)
        assert answers.count() == 1
        assert len(question_dict['answers']) == 0

    def test_Answers_dict(self):
        answer = Answers.objects.get(id=20)
        assert answer.correct == True
        assert 'correct' not in answer.dict_no_correct_field()