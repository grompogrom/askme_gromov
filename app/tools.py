from datetime import timedelta
from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count, OuterRef, Sum, Subquery
from django.db.models.functions import Coalesce

from app.models import Like, Answer, Question, Tag, PopularTag, Profile, BestProfile


def paginate(objects, request, per_page=15):
    paginator = Paginator(objects, per_page)
    last_page_number = paginator.num_pages
    try:
        page = request.GET.get('page', 1)
        if page == 'last':
            return paginator.page(last_page_number)
        else:
            page = int(page)
        return paginator.page(page)
    except EmptyPage:
        pass
    except ValueError:
        pass
    return paginator.page(last_page_number)


def get_base(request):
    is_logged = request.user.is_authenticated
    ful_url = request.get_full_path()
    user_meta = None
    if is_logged:
        user_meta = request.user
    best_members = BestProfile.objects.all()
    best_members = list(map(lambda x: x.profile.user.username, best_members))
    popular_tags = PopularTag.objects.all()
    popular_tags = list(map(lambda x: x.tag, popular_tags))
    return {
        'is_logged': is_logged,
        'user': user_meta,
        'best_members': best_members,
        'popular_tags': popular_tags,
        'continue': ful_url
    }



def like_question(author, question: Question):
    like = Like(author=author, question=question)
    like.save()
    question.likes_count += 1
    question.save()
    return like


def like_answer(author, answer: Answer):
    like = Like(author=author, answer=answer)
    like.save()
    answer.likes_count += 1
    answer.save()
    return like


def index_answers_likes():
    answers = Answer.objects.annotate(total_likes=Count('like'))
    for answer in answers:
        answer.likes_count = answer.total_likes
        answer.save()


def index_question_likes():
    questions = Question.objects.annotate(total_likes=Count('like'))
    for question in questions:
        question.likes_count = question.total_likes
        question.save()


def index_popular_tags():
    PopularTag.objects.all().delete()
    popular_tags = Tag.objects.get_most_used(20)
    popular_tags = list(map(lambda x: PopularTag(tag=x), popular_tags))
    PopularTag.objects.bulk_create(popular_tags)


def index_best_users():
    one_week_ago = timezone.now().date() - timedelta(days=7)
    last_questions = Question.objects.filter(created_at__gte=one_week_ago)
    last_answers = Answer.objects.filter(created_at__gte=one_week_ago)

    question_likes = last_questions.filter(author=OuterRef('pk')).order_by().values('author')
    question_likes = question_likes.annotate(likes=Sum('likes_count')).values('likes')
    answer_likes = last_answers.filter(author=OuterRef('pk')).order_by().values('author')
    answer_likes = answer_likes.annotate(likes=Sum('likes_count')).values('likes')

    profiles = Profile.objects.annotate(
        total_likes=Coalesce(Subquery(question_likes), 0) + Coalesce(Subquery(answer_likes), 0)
    ).order_by('-total_likes')

    best_profiles = list(map(lambda x: BestProfile(profile=x), profiles[:10]))

    BestProfile.objects.bulk_create(best_profiles)
