from datetime import timedelta
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count, OuterRef, Sum, Subquery
from django.db.models.functions import Coalesce

from app.models import Like, Answer, Question, Tag, PopularTag, Profile, BestProfile


def paginate(objects, request, per_page=15):
    paginator = Paginator(objects, per_page)
    try:
        page = int(request.GET.get('page', 1))
        return paginator.page(page)
    except EmptyPage:
        pass
    except ValueError:
        pass
    return paginator.page(1)


def get_base():
    best_members = BestProfile.objects.all()
    best_members = list(map(lambda x: x.profile.user.username, best_members))
    popular_tags = PopularTag.objects.all()
    popular_tags = list(map(lambda x: x.tag, popular_tags))
    return {
    'is_logged': False,
    'best_members': best_members,
    'popular_tags': popular_tags}


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


def calculate_likes():
    likes = Like.objects.all()
    for like in likes:
        if like.question is not None:
            question = like.question
            question.likes_count += 1
            question.save()
        elif like.answer is not None:
            answer = like.answer
            answer.likes_count += 1
            answer.save()


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

