from django.conf.urls import *

from django.core.urlresolvers import reverse

from debate import models as m

urlpatterns = patterns('debate.views',
    url(r'^$', 'tournament_home', name='tournament_home'),
    url(r'^config/$', 'tournament_config', name='tournament_config'),
    url(r'^draw/$', 'draw_index', name='draw_index'),
    url(r'^round/(?P<round_seq>\d+)/$',
        'round_index', name='round_index'),
    url(r'^feedback_progress/$', 'feedback_progress', name='feedback_progress'),

    url(r'^public/$', 'public_index', name='public_index'),
    url(r'^public/draw/$', 'public_draw', name='public_draw'),
    url(r'^public/add_ballot/$', 'public_ballot_submit', name='public_ballot_submit'),
    url(r'^public/add_ballot/adjudicator/(?P<adj_id>\d+)/$', 'public_new_ballots',
        name='public_new_ballots'),
    url(r'^public/add_feedback/team/(?P<source_id>\d+)/$', 'public_enter_feedback',
        { 'source_type': m.Team }, name='public_enter_feedback_team'),
    url(r'^public/add_feedback/adjudicator/(?P<source_id>\d+)/$', 'public_enter_feedback',
        { 'source_type': m.Adjudicator }, name='public_enter_feedback_adjudicator'),
    url(r'^public/add_feedback/$', 'public_feedback_submit', name='public_feedback_submit'),
    url(r'^public/feedback_progress/$', 'public_feedback_progress', name='public_feedback_progress'),
    url(r'^public/participants/$', 'public_participants', name='public_participants'),

    url(r'^public/tab/team_tab/$', 'public_team_tab', name='public_team_tab'),
    url(r'^public/tab/speaker_tab/$', 'public_speaker_tab', name='public_speaker_tab'),
    url(r'^public/tab/replies_tab/$', 'public_replies_tab', name='public_replies_tab'),
    url(r'^public/tab/motions_tab/$', 'public_motions_tab', name='public_motions_tab'),
    url(r'^public/tab/feedback_tab/$', 'public_feedback_tab', name='public_feedback_tab'),

    url(r'^round/(?P<round_seq>\d+)/venues/$',
        'availability', { 'model': 'venue', 'context_name': 'venues' }, 'venue_availability'),
    url(r'^round/(?P<round_seq>\d+)/venues/update/$',
        'update_availability', { 'active_attr': 'venue', 'active_model': m.ActiveVenue, 'update_method': 'set_available_venues' }, 'update_venue_availability'),

    url(r'^round/(?P<round_seq>\d+)/adjudicators/$',
        'availability', { 'model': 'adjudicator', 'context_name': 'adjudicators' }, 'adjudicator_availability'),
    url(r'^round/(?P<round_seq>\d+)/adjudicators/update/$',
        'update_availability', { 'active_attr': 'adjudicator', 'active_model': m.ActiveAdjudicator, 'update_method': 'set_available_adjudicators' }, 'update_adjudicator_availability'),

    url(r'^round/(?P<round_seq>\d+)/people/$',
        'checkin_results', { 'model': 'person', 'context_name': 'people' }, 'people_availability'),
    url(r'^round/(?P<round_seq>\d+)/people/update/$',
        'checkin_update', { 'active_attr': None, 'active_model': None, 'update_method': 'set_available_people' }, 'update_people_availability'),

    url(r'^round/(?P<round_seq>\d+)/teams/$',
        'availability', { 'model': 'team', 'context_name': 'teams' }, 'team_availability'),
    url(r'^round/(?P<round_seq>\d+)/teams/update/$',
        'update_availability', { 'active_attr': 'team', 'active_model': m.ActiveTeam, 'update_method': 'set_available_teams' }, 'update_team_availability'),

    url(r'^round/(?P<round_seq>\d+)/checkin/$', 'checkin', name='checkin'),
    url(r'^round/(?P<round_seq>\d+)/checkin/post/$', 'post_checkin', name='post_checkin'),

    url(r'^round/(?P<round_seq>\d+)/draw/$', 'draw', name='draw'),
    url(r'^round/(?P<round_seq>\d+)/draw_display_by_venue/$', 'draw_display_by_venue',
        name='draw_display_by_venue'),
    url(r'^round/(?P<round_seq>\d+)/draw_display_by_team/$', 'draw_display_by_team',
        name='draw_display_by_team'),
    url(r'^round/(?P<round_seq>\d+)/draw/create/$', 'create_draw',
        name='create_draw'),
    url(r'^round/(?P<round_seq>\d+)/draw/confirm/$', 'confirm_draw',
        name='confirm_draw'),
    url(r'^round/(?P<round_seq>\d+)/draw/release/$', 'release_draw',
        name='release_draw'),
    url(r'^round/(?P<round_seq>\d+)/draw/unrelease/$', 'unrelease_draw',
        name='unrelease_draw'),

    url(r'^round/(?P<round_seq>\d+)/draw/venues/$', 'draw_venues_edit',
        name='draw_venues_edit'),
    url(r'^round/(?P<round_seq>\d+)/draw/venues/save/$', 'save_venues',
        name='save_venues'),

    url(r'^round/(?P<round_seq>\d+)/draw/adjudicators/$', 'draw_adjudicators_edit',
        name='draw_adjudicators_edit'),
    url(r'^round/(?P<round_seq>\d+)/draw/adjudicators/_get/$',
        'draw_adjudicators_get',
        name='draw_adjudicators_get'),
    url(r'^round/(?P<round_seq>\d+)/draw/adjudicators/save/$', 'save_adjudicators',
        name='save_adjudicators'),
    url(r'^round/(?P<round_seq>\d+)/_update_importance/$',
        'update_debate_importance',
        name='update_debate_importance'),

    url(r'^round/(?P<round_seq>\d+)/confirm_increment/$', 'confirm_increment',
        name='confirm_increment'),
    url(r'^round/(?P<round_seq>\d+)/increment_round/$', 'increment_round',
        name='increment_round'),

    url(r'^round/(?P<round_seq>\d+)/adj_allocation/create/$',
        'create_adj_allocation',
        name='create_adj_allocation'),
    url(r'^round/(?P<round_seq>\d+)/motions/$', 'motions',
        name='motions'),
    url(r'^round/(?P<round_seq>\d+)/motions/edit/$', 'motions_edit',
        name='motions_edit'),
    url(r'^round/(?P<round_seq>\d+)/results/$', 'results',
        name='results'),
    url(r'^round/(?P<round_seq>\d+)/team_standings/$', 'team_standings',
        name='team_standings'),
    url(r'^round/(?P<round_seq>\d+)/speaker_standings/$', 'speaker_standings',
        name='speaker_standings'),
    url(r'^round/(?P<round_seq>\d+)/reply_standings/$', 'reply_standings',
        name='reply_standings'),
    url(r'^ballots/(?P<ballots_id>\d+)/edit/$', 'edit_ballots',
        name='edit_ballots'),
    url(r'^debate/(?P<debate_id>\d+)/new_ballots/$', 'new_ballots',
        name='new_ballots'),
    url(r'^round/(?P<round_seq>\d+)/ballot_checkin/$', 'ballot_checkin',
        name='ballot_checkin'),
    url(r'^round/(?P<round_seq>\d+)/ballot_checkin/get_details/$', 'ballot_checkin_get_details',
        name='ballot_checkin_get_details'),
    url(r'^round/(?P<round_seq>\d+)/ballot_checkin/post/$', 'post_ballot_checkin',
        name='post_ballot_checkin'),

    url(r'^round/(?P<round_seq>\d+)/adjudicators/conflicts/$', 'adj_conflicts', name='adj_conflicts'),
    url(r'^adjudicators/scores/$', 'adj_scores', name='adj_scores'),
    url(r'^adjudicators/feedback/$', 'adj_feedback', name='adj_feedback'),
    url(r'^adjudicators/feedback/get/$', 'get_adj_feedback', name='get_adj_feedback'),
    url(r'^adjudicators/feedback/(?P<adjudicator_id>\d+)/$',
        'enter_feedback', name='enter_feedback'),
    )