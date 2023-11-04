import random

LONG_LOREM = ("Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, "
              "totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta "
              "sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, "
              "sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam "
              "est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius "
              "modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, "
              "quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi "
              "consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae "
              "consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?")
TAGS = [f'tag{i}' for i in range(10)]
QUESTIONS = [{
        'id': i,
        'title': f'Question {i}',
        'likes': i * 2 + 1,
        'answers': i,
        'content': LONG_LOREM,
        'tags': [random.choice(TAGS) for i in range(random.randint(1,3))]
    } for i in range(100)]

IS_LOGGED = True
BEST_MEMBERS = ['Maslove', 'Brin', 'Page', 'Musk']
POPULAR_TAGS = [ {"name": random.choice(TAGS)} for x in range(10)]

BASE = {
    'is_logged': IS_LOGGED,
    'best_members': BEST_MEMBERS,
    'popular_tags': POPULAR_TAGS}


