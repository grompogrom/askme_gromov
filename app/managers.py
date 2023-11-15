from django.core.checks import Tags
from django.db import models
from django.db.models import Count


class QuestionManager(models.Manager):

    def all_hot(self):
        return self.order_by('-likes_count')

    def all_new(self):
        return self.order_by('-created_at')

    def all_with_answers(self):
        new = self.order_by('created_at')
        return map(lambda x: x.as_dict(), new)


class AnswerManager(models.Manager):

    def count_by_question(self, question_id):
        return len(self.filter(question=question_id))


class TagManager(models.Manager):

    def get_most_used(self, count):
        tag_counts = self.annotate(question_count=Count('question'))
        top_tags = tag_counts.order_by('-question_count')[:count]
        return top_tags


class LikeManager(models.Manager):

    def _is_like_exit(self, profile, question=None, answer=None):
        if question is not None:
            return self.get(author=profile, question=question).exists()
        elif answer is not None:
            return self.get(author=profile, answer=answer).exists()
        return


    def like(self, author, question=None, answer=None):
        if question is not None:
            return self.create(author=author, question=question)
        elif answer is not None:
            return self.create(author=author, answer=answer)
        return

    def unlike(self, profile, question=None, answer=None):
        if question is not None:
            return self.get(author=profile, question=question).delete()
        elif answer is not None:
            return self.get(author=profile, answer=answer).delete()
        return
