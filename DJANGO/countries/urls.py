from django.urls import path
from django.conf.urls.static import static
from drfproject import settings
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ReviewList, ReviewDetail, ReviewComment, ReviewCommentList, ReviewBest, Reviewlike

urlpatterns = [
    path('<str:country_code>/review/', ReviewList.as_view()),
    path('<str:country_code>/review/<int:pk>/', ReviewDetail.as_view()),
    path('<str:country_code>/review/<int:pk>/comment/', ReviewCommentList.as_view()),
    path('<str:country_code>/review/<int:pk>/comment/<int:comment_pk>/', ReviewComment.as_view()),
    path('<str:country_code>/review/best/', ReviewBest.as_view()),
    path('<str:country_code>/review/<int:pk>/like/', Reviewlike.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)