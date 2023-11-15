import random

from django.contrib.auth.models import User

from app.models import Tag, Profile, Question, Answer, Like, BestProfile, PopularTag

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
        questions = [
            Question(title="Question {0}".format(i),
                     text=LONG_LOREM,
                     author=random.choice(self.profiles))
            for i in range(count)
        ]
        Question.objects.bulk_create(questions)

        for tmp in questions:
            tmp.tags.add(*random.choices(self.tags, k=random.randint(1, 3)))
        self.questions.extend(questions)
        self.log_func(count, "questions")

    def _create_answers(self, count=10):
        answers = [Answer(
                author=random.choice(self.profiles),
                question=random.choice(self.questions),
                text=LONG_LOREM[:100]
            ) for i in range(count)]
        Answer.objects.bulk_create(answers)
        self.answers.extend(answers)
        self.log_func(count, "answers")

    def _create_likes(self, count=10):
        likes = []
        for i in range(count):
            if random.randint(0, 1) == 1:
                question = random.choice(self.questions)
                answer = None
            else:
                answer = random.choice(self.answers)
                question = None

            tmp = Like.objects.like(
                author=random.choice(self.profiles),
                question=question,
                answer=answer
            )
            likes.append(tmp)
        Like.objects.bulk_create(likes)
        self.likes.extend(likes)
        self.log_func(count, "likes")
