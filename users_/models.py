from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    userlvl = models.IntegerField()

class Tests(models.Model):
    title = models.CharField(max_length=20, null=False)

    def delete(self, *args, **kwargs):
        questions = Questions.objects.filter(test=self)
        for question in questions:
            answers = Answers.objects.filter(question=question)
            for answer in answers:
                answer.delete()
            question.delete()
        super(Tests, self).delete(*args, **kwargs)

    def dict(self):
        questions = Questions.objects.filter(test=self)
        return dict(id=self.id, title=self.title,
                    questions=[question.dict() for question in
                               Questions.objects.filter(test=self) if
                               len(question.dict()['answers']) > 0])

class Questions(models.Model):
    test = models.ForeignKey(Tests)
    question = models.CharField(max_length=100, null=False)

    def delete(self, *args, **kwargs):
        answers = Answers.objects.filter(question=self)
        for answer in answers:
            answer.delete()
        super(Questions, self).delete(*args, **kwargs)

    def dict(self):
        all_answers = Answers.objects.filter(question=self)
        return dict(id=self.id, question=self.question,
                    answers=[answer.dict_no_correct_field() for answer in
                             all_answers if
                             (Answers.objects.filter(question=self,
                              correct=True).count() > 0 and
                              Answers.objects.filter(question=self).count() >
                              1)])

class Answers(models.Model):
    question = models.ForeignKey(Questions)
    answer = models.CharField(max_length=50, null=False)
    correct = models.BooleanField(default=False)

    def dict_no_correct_field(self):
        return dict(id=self.id, answer=self.answer)