from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ReviewList, ReviewDetail, ReviewComment, ReviewCommentList, ReviewBest, Reviewlike

urlpatterns = [
    path('review/', ReviewList.as_view()),
    path('review/<int:pk>/', ReviewDetail.as_view()),
    path('review/<int:pk>/comment/', ReviewCommentList.as_view()),
    path('review/<int:pk>/comment/<int:comment_pk>/', ReviewComment.as_view()),
    path('review/best/', ReviewBest.as_view()),
    path('review/best/<int:pk>/like/', Reviewlike.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)