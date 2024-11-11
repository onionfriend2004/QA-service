from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from random import choice, sample, randint
from faker import Faker

f = Faker()

class Command(BaseCommand):
    help = 'Fill the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.fill_profile(ratio)
        self.fill_tag(ratio)
        self.fill_questions(ratio * 10)
        self.fill_answers(ratio * 100)
        self.fill_likes_questions(ratio * 200)
        self.fill_likes_answers(ratio * 200)
        self.stdout.write(self.style.SUCCESS('Data creation was successful'))

    @staticmethod
    def fill_profile(cnt):
        for i in range(cnt):
            user = User.objects.create_user(
                username=f.user_name(),
                email=f.email(),
                password="1"
            )
            Profile.objects.create(
                user_id=user,
                avatar="img/ava" + str(i % 7) + ".png",
            )

    @staticmethod
    def fill_tag(cnt):
        for i in range(cnt):
            tag = f.word()
            while Tag.objects.filter(tag=tag).exists():
                tag = f.word()
            Tag.objects.create(tag=tag)

    @staticmethod
    def fill_questions(cnt):
        profiles = list(Profile.objects.all())
        tags = list(Tag.objects.all())
        for i in range(cnt):
            profile = choice(profiles)
            q = Question.objects.create(
                profile_id=profile,
                title=f.sentence(),
                content=f.text(),
            )
            q.tags.set(sample(tags, k=randint(1, 3)))

    @staticmethod
    def fill_answers(cnt):
        profiles = list(Profile.objects.all())
        questions = list(Question.objects.all())
        for i in range(cnt):
            Answer.objects.create(
                profile_id=choice(profiles),
                question_id=choice(questions),
                content=f.text(),
            )

    @staticmethod
    def fill_likes_questions(cnt):
        profiles = list(Profile.objects.all())
        questions = list(Question.objects.all())
        count = 0
        for question in questions:
            for profile in sample(profiles, k=randint(1, len(profiles))):
                if not QuestionLike.objects.filter(question_id=question, profile_id=profile).exists():
                    QuestionLike.objects.create(
                        question_id=question,
                        profile_id=profile,
                        is_like=choice([True, False]),
                    )
                    count += 1
                if count >= cnt:
                    break
            if count >= cnt:
                break

    @staticmethod
    def fill_likes_answers(cnt):
        profiles = list(Profile.objects.all())
        answers = list(Answer.objects.all())
        count = 0
        for answer in answers:
            for profile in sample(profiles, k=randint(1, len(profiles))):
                if not AnswerLike.objects.filter(answer_id=answer, profile_id=profile).exists():
                    AnswerLike.objects.create(
                        answer_id=answer,
                        profile_id=profile,
                        is_like=choice([True, False]),
                    )
                    count += 1
                if count >= cnt:
                    break
            if count >= cnt:
                break
            