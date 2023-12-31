import random

from django.contrib.auth.models import User

from app.models import Tag, Profile, Question, Answer, Like, BestProfile, PopularTag
from app.tools import index_question_likes, index_answers_likes, index_popular_tags, index_best_users

LONG_LOREM = ("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, "
              "totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta "
              "sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, "
              "sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam "
              "est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius "
              "modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, "
              "quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi "
              "consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae "
              "consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?")

NICKNAMES = ['Maslove', 'Brin', 'Page', 'Musk']


class TestDataProvider:
    def __init__(self, start_count):
        self.count = start_count
        self.tags = []
        self.profiles = []
        self.questions = []
        self.answers = []
        self.likes = []
        self.log_func = [None, None]

    def fill(self, users_count=None):

        users_count = self.count if users_count is None else users_count

        questions_count = users_count * 10
        answers_count = questions_count * 10
        tags_count = users_count
        likes_count = users_count * 200

        self._create_tags(tags_count)
        self._create_profiles(users_count)
        self._create_questions(questions_count)
        self._create_answers(answers_count)
        self._create_likes(likes_count)
        index_question_likes()
        index_answers_likes()
        index_popular_tags()
        index_best_users()

    def set_callbacks(self, log_func):
        self.log_func = log_func

    def _create_tags(self, count=10):
        tags = [Tag(name="tag{0}".format(i)) for i in range(count)]
        Tag.objects.bulk_create(tags)
        self.tags.extend(tags)
        self.log_func(count, "tags")

    def _create_profiles(self, count=10):
        users = [User(username="{0}{1}".format(random.choice(NICKNAMES), i),) for i in range(count)]
        User.objects.bulk_create(users)

        profiles = [Profile(user=users[i]) for i in range(count)]
        Profile.objects.bulk_create(profiles)
        self.profiles.extend(profiles)
        self.log_func(count, "profiles")

    def _create_questions(self, count=10):
        chunck = 10000
        parts_count = int(count / chunck)
        for i in range(parts_count):
            index = chunck * i
            questions = [
                Question(title="Question {0}".format(index + i),
                         text=LONG_LOREM,
                         author=random.choice(self.profiles))
                for i in range(chunck)
            ]
            Question.objects.bulk_create(questions)

            for tmp in questions:
                tmp.tags.add(*random.choices(self.tags, k=random.randint(1, 3)))
            self.questions.extend(questions)
            self.log_func(index + chunck, "questions")

    def _create_answers(self, count=10):
        chunck = 100000
        parts_count = int(count / chunck)
        for i in range(parts_count):
            index = chunck * i
            answers = [Answer(
                    author=random.choice(self.profiles),
                    question=random.choice(self.questions),
                    text=LONG_LOREM[:100]
                ) for _ in range(chunck)]
            Answer.objects.bulk_create(answers)
            self.answers.extend(answers)
            self.log_func(index + chunck, "answers")

    def _create_likes(self, count):
        i = 0
        for profile in self.profiles:
            likes = []
            i += 1
            for question in random.choices(self.questions, k=100):
                likes.append(Like(author=profile, question=question))
            for answer in random.choices(self.answers, k=100):
                likes.append(Like(author=profile, answer=answer))
            self.likes.extend(likes)
            Like.objects.bulk_create(likes)
            self.log_func(200 * i, "likes")
