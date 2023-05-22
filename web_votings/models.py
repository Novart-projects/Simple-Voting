from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class AllVotings(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    type = models.IntegerField()
    creator_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="votings")
    number_of_questions = models.IntegerField()
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name[:15]


class Answers(models.Model):
    answer_variant = models.CharField(max_length=100)
    question = models.ForeignKey(AllVotings, null=True, on_delete=models.CASCADE, related_name="answer")
    number_of_p_chosen = models.IntegerField()
    def __str__(self):
        return self.answer_variant

class Complaint(models.Model):
    theme = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    vote = models.ForeignKey(AllVotings, null=True, on_delete=models.CASCADE)
    stat = models.IntegerField()
    ans = models.CharField(max_length=500, blank=True, null=True)


class UsersAnswers(models.Model):
    answer = models.ForeignKey(Answers, null=True, on_delete=models.CASCADE, related_name="variant_chosen")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user_answer")


"""class Questions(models.Model):
    question = models.CharField(AllVotings, max_length=100)"""

