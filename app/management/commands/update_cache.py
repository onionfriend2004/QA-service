from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from app.models import Question, Answer, Tag, Profile

class Command(BaseCommand):
    help = 'Update cache for popular tags and top users'

    def handle(self, *args, **kwargs):
        self.update_popular_tags()
        self.update_top_users()

    def update_popular_tags(self):
        three_months_ago = timezone.now() - timedelta(days=90)
        popular_tags = Tag.objects.filter(question__created_at__gte=three_months_ago).annotate(num_questions=Count('question')).order_by('-num_questions')[:10]
        cache.set('popular_tags', list(popular_tags.values('tag', 'num_questions')), timeout=None)

    def update_top_users(self):
        one_week_ago = timezone.now() - timedelta(days=7)
        top_users = Profile.objects.filter(
            Q(question__created_at__gte=one_week_ago) | Q(answer__created_at__gte=one_week_ago)
        ).annotate(
            num_questions=Count('question'),
            num_answers=Count('answer')
        ).order_by('-num_questions', '-num_answers')[:10]
        cache.set('top_users', list(top_users.values('user_id__username', 'num_questions', 'num_answers')), timeout=None)
