from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from random import choice, sample, randint
from faker import Faker
from django.db import transaction

f = Faker()

class Command(BaseCommand):
    help = 'Fill the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(self.style.SUCCESS(f'Starting data generation with ratio {ratio}'))

        self.stdout.write(self.style.SUCCESS('Filling profiles...'))
        self.fill_profile(ratio)
        self.stdout.write(self.style.SUCCESS('Profiles filled successfully'))

        self.stdout.write(self.style.SUCCESS('Filling tags...'))
        self.fill_tag(ratio)
        self.stdout.write(self.style.SUCCESS('Tags filled successfully'))

        self.stdout.write(self.style.SUCCESS('Filling questions...'))
        self.fill_questions(ratio * 10)
        self.stdout.write(self.style.SUCCESS('Questions filled successfully'))

        self.stdout.write(self.style.SUCCESS('Filling answers...'))
        self.fill_answers(ratio * 100)
        self.stdout.write(self.style.SUCCESS('Answers filled successfully'))

        self.stdout.write(self.style.SUCCESS('Filling question likes...'))
        self.fill_likes_questions(ratio * 100)
        self.stdout.write(self.style.SUCCESS('Question likes filled successfully'))

        self.stdout.write(self.style.SUCCESS('Filling answer likes...'))
        self.fill_likes_answers(ratio * 100)
        self.stdout.write(self.style.SUCCESS('Answer likes filled successfully'))

        self.stdout.write(self.style.SUCCESS('Data creation was successful'))

    @staticmethod
    def fill_profile(cnt):
        users = []
        profiles = []
        for i in range(cnt):
            user = User(
                username=f'user{i}',
                email=f'email{i}@mail.ru',
                password="1"
            )
            user.set_password(user.password)
            users.append(user)
            profiles.append(Profile(
                user_id=user,
            ))
        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)

    @staticmethod
    def fill_tag(cnt):
        tags = []
        for i in range(cnt):
            tags.append(Tag(tag=f'tag{i}'))

        Tag.objects.bulk_create(tags)

    @staticmethod
    def fill_questions(cnt):
        profiles = list(Profile.objects.all())
        tags = list(Tag.objects.all())
        questions = []
        for i in range(cnt):
            profile = choice(profiles)
            q = Question(
                profile_id=profile,
                title=f.sentence(),
                content=f.text(),
            )
            questions.append(q)
        Question.objects.bulk_create(questions)
        for q in questions:
            q.tags.set(sample(tags, k=randint(1, 3)))

    @staticmethod
    def fill_answers(cnt):
        profiles = list(Profile.objects.all())
        questions = list(Question.objects.all())
        answers = []
        for _ in range(cnt):
            answers.append(Answer(
                profile_id=choice(profiles),
                question_id=choice(questions),
                content=f.text(),
            ))
        Answer.objects.bulk_create(answers)

        question_answer_counts = {}
        for answer in answers:
            question_id = answer.question_id.id
            if question_id in question_answer_counts:
                question_answer_counts[question_id] += 1
            else:
                question_answer_counts[question_id] = 1

        for question_id, count in question_answer_counts.items():
            question = Question.objects.get(id=question_id)
            question.answer_count += count
            question.save()
                
    @staticmethod
    def fill_likes_questions(cnt):
        profiles = list(Profile.objects.all())
        questions = list(Question.objects.all())
        likes = []
        unique_pairs = set()
        count = 0

        while count < cnt:
            uFrom = choice(profiles)
            qTo = choice(questions)
            if (uFrom.id, qTo.id) not in unique_pairs:
                is_like = choice([True, False])
                likes.append(QuestionLike(
                    profile_id=uFrom,
                    question_id=qTo,
                    is_like=is_like,
                ))
                unique_pairs.add((uFrom.id, qTo.id))
                count += 1

        QuestionLike.objects.bulk_create(likes)
        for like in likes:
            if like.is_like:
                like.question_id.rating += 1
            else:
                like.question_id.rating -= 1
            like.question_id.save()

    @staticmethod
    def fill_likes_answers(cnt):
        profiles = list(Profile.objects.all())
        answers = list(Answer.objects.all())
        likes = []
        unique_pairs = set()
        count = 0

        while count < cnt:
            uFrom = choice(profiles)
            aTo = choice(answers)
            if (uFrom.id, aTo.id) not in unique_pairs:
                is_like = choice([True, False])
                likes.append(AnswerLike(
                    profile_id=uFrom,
                    answer_id=aTo,
                    is_like=is_like,
                ))
                unique_pairs.add((uFrom.id, aTo.id))
                count += 1

        AnswerLike.objects.bulk_create(likes)
        for like in likes:
            if like.is_like:
                like.answer_id.rating += 1
            else:
                like.answer_id.rating -= 1
            like.answer_id.save()
