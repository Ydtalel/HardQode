from rest_framework import generics
from rest_framework import permissions
from edu_app.models import Lesson, ViewingStatus, Product
from .serializers import LessonSerializer, ProductStatsSerializer
from django.db.models import Count, Sum, F, ExpressionWrapper, FloatField, Max, Q
from django.contrib.auth.models import User


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Получаем текущего пользователя из запроса
        user = self.request.user
        # Получаем уроки, к которым у пользователя есть доступ
        accessible_lessons = Lesson.objects.filter(products__owner=user).distinct()
        lesson_status = {}
        for lesson in accessible_lessons:
            try:
                # Пытаемся получить статус просмотра для данного урока и пользователя
                viewing_status = ViewingStatus.objects.get(user=user, lesson=lesson)
                lesson_status[lesson.id] = {
                    'viewed': viewing_status.viewed,
                    'view_time_seconds': viewing_status.view_time_seconds,
                }
            except ViewingStatus.DoesNotExist:
                # Если статус просмотра не существует, устанавливаем значения по умолчанию
                lesson_status[lesson.id] = {
                    'viewed': False,
                    'view_time_seconds': 0,
                }
        # Обновляем атрибуты уроков в соответствии с их статусами просмотра
        for lesson in accessible_lessons:
            lesson.viewed = lesson_status[lesson.id]['viewed']
            lesson.view_time_seconds = lesson_status[lesson.id]['view_time_seconds']
        # Возвращаем список уроков, к которым у пользователя есть доступ
        return accessible_lessons


class ProductLessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']  # Получаем ID продукта из URL
        # Получить уроки, доступные этому пользователю и принадлежащие указанному продукту и предварительно выбрать
        # связанные ViewingStatus
        accessible_lessons = Lesson.objects.filter(products__owner=user, products__id=product_id).prefetch_related(
            'viewingstatus_set').distinct()

        # Аннотация: Получаем максимальную дату просмотра для каждого урока пользователя
        annotated_lessons = accessible_lessons.annotate( max_date_viewed=Max('viewingstatus__date_viewed'))

        lesson_status = {}
        for lesson in annotated_lessons:
            try:
                viewing_status = ViewingStatus.objects.get(user=user, lesson=lesson)
                lesson_status[lesson.id] = {
                    'viewed': viewing_status.viewed,
                    'view_time_seconds': viewing_status.view_time_seconds,
                    'date_viewed': viewing_status.date_viewed,
                }
            except ViewingStatus.DoesNotExist:
                lesson_status[lesson.id] = {
                    'viewed': False,
                    'view_time_seconds': 0,
                    'date_viewed': None,
                }

        for lesson in annotated_lessons:
            lesson.viewed = lesson_status[lesson.id]['viewed']
            lesson.view_time_seconds = lesson_status[lesson.id]['view_time_seconds']
            lesson.date_viewed = lesson_status[lesson.id]['date_viewed']

        return annotated_lessons


class ProductStatsAPIView(generics.ListAPIView):
    serializer_class = ProductStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # общее количество пользователей на платформе
        total_users_on_platform = User.objects.count()

        # Аннотация: количество уроков, время просмотра и количество пользователей для каждого продукта
        product_stats = Product.objects.annotate(
            total_viewed_lessons=Count('lesson__viewingstatus', filter=Q(lesson__viewingstatus__viewed=True)),
            total_view_time=Sum('lesson__viewingstatus__view_time_seconds',
                                filter=Q(lesson__viewingstatus__viewed=True)),
            total_users=Count('lesson__viewingstatus__user', distinct=True),
        ).distinct()

        # процент приобретения продукта
        product_stats = product_stats.annotate(
            purchase_percent=ExpressionWrapper(
                F('total_users') * 100 / total_users_on_platform,
                output_field=FloatField()
            )
        )

        return product_stats
