from django.urls import path

from participants.models import Adjudicator, Team

from . import views

urlpatterns = [
    # Overviews
    path('',
        views.FeedbackOverview.as_view(),
        name='adjfeedback-overview'),
    path('progress/',
        views.FeedbackProgress.as_view(),
        name='feedback_progress'),

    # Getting/setting values
    path('test/set/',
        views.SetAdjudicatorTestScoreView.as_view(),
        name='adjfeedback-set-adj-test-score'),
    path('breaking/set/',
        views.SetAdjudicatorBreakingStatusView.as_view(),
        name='adjfeedback-set-adj-breaking-status'),
    path('notes/test/set/',
        views.SetAdjudicatorNoteView.as_view(),
        name='adjfeedback-set-adj-note'),

    # Source
    path('latest/',
        views.LatestFeedbackView.as_view(),
        name='adjfeedback-view-latest'),
    path('source/list/',
        views.FeedbackBySourceView.as_view(),
        name='adjfeedback-view-by-source'),
    path('source/team/<int:pk>/',
        views.FeedbackFromTeamView.as_view(),
        name='adjfeedback-view-from-team'),
    path('source/adjudicator/<int:pk>/',
        views.FeedbackFromAdjudicatorView.as_view(),
        name='adjfeedback-view-from-adjudicator'),
    path('target/list/',
        views.FeedbackByTargetView.as_view(),
        name='adjfeedback-view-by-target'),
    path('target/adjudicator/<int:pk>/',
        views.FeedbackOnAdjudicatorView.as_view(),
        name='adjfeedback-view-on-adjudicator'),

    # Adding
    path('add/',
        views.AdminAddFeedbackIndexView.as_view(),
        name='adjfeedback-add-index'),
    path('add/team/<int:source_id>/',
        views.AdminAddFeedbackView.as_view(model=Team),
        name='adjfeedback-add-from-team'),
    path('add/adjudicator/<int:source_id>/',
        views.AdminAddFeedbackView.as_view(model=Adjudicator),
        name='adjfeedback-add-from-adjudicator'),

]
