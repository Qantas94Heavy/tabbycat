from django.utils.translation import gettext as _

from draw.models import Debate
from participants.models import Team
from utils.misc import reverse_tournament
from utils.tables import TabbycatTableBuilder


class ResultsTableBuilder(TabbycatTableBuilder):
    """Painfully construct the edit links; this is the only case where
    a cell has multiple links; hence the creating HTML directly"""

    def get_status_meta(self, debate):
        if any(team.type == Team.TYPE_BYE for team in debate.teams):
            return "fast-forward", "", 5, _("Bye Debate")
        elif debate.result_status == Debate.STATUS_NONE:
            return "x", "text-danger", 0, _("No Ballot")
        elif debate.result_status == Debate.STATUS_DRAFT:
            return "circle", "text-info", 2, _("Ballot is Unconfirmed")
        elif debate.result_status == Debate.STATUS_CONFIRMED:
            return "check", "text-success", 3, _("Ballot is Confirmed")
        elif debate.result_status == Debate.STATUS_POSTPONED:
            return "pause", "", 4, _("Debate was Postponed")
        else:
            raise ValueError('Debate has no discernable status')

    def add_ballot_check_in_columns(self, debates, key):

        status_header = {
            'key': key,
            'tooltip': _("Whether this debate's ballot has been checked-in"),
            'icon': "compass",
        }
        status_cells = []
        for debate in debates:
            cell = {
                'icon': 'check' if debate.checked_in else 'x',
                'sort': 1 if debate.checked_in else 0,
                'tooltip': debate.checked_tooltip
            }
            status_cells.append(cell)
        self.add_column(status_header, status_cells)

    def add_ballot_status_columns(self, debates, key):

        status_header = {
            'key': key,
            'tooltip': _("Status of this debate's ballot"),
            'icon': "crosshair",
        }
        status_cells = []
        for debate in debates:
            meta = self.get_status_meta(debate)
            cell = {
                'icon': meta[0],
                'class': meta[1],
                'sort': meta[2],
                'tooltip': meta[3]
            }
            status_cells.append(cell)
        self.add_column(status_header, status_cells)

    def get_ballot_text(self, debate):
        ballotsubs_info = " "

        # These are prefetched, so sort using Python rather than generating an SQL query
        ballotsubmissions = sorted(debate.ballotsubmission_set.all(), key=lambda x: x.version)

        for ballotsub in ballotsubmissions:
            if not self.admin and ballotsub.discarded:
                continue

            link = reverse_tournament('results-ballotset-edit' if self.admin else 'results-assistant-ballotset-edit',
                                      self.tournament,
                                      kwargs={'pk': ballotsub.id})
            ballotsubs_info += "<a href=" + link + " class='text-nowrap'>"

            if ballotsub.confirmed:
                edit_status = _("Re-edit v%(version)d") % {'version': ballotsub.version}
            elif self.admin:
                edit_status = _("Edit v%(version)d") % {'version': ballotsub.version}
            else:
                edit_status = _("Review v%(version)d") % {'version': ballotsub.version}

            if ballotsub.discarded:
                ballotsubs_info += "<strike class='text-muted'>" + edit_status + "</strike></a>"
                ballotsubs_info += "<small class='d-block text-nowrap'>"
                # Translators: This comes after a link to edit the ballot and before the line indicating its author. Please mind the leading and trailing spaces.
                ballotsubs_info += _(" discarded; ")
            else:
                ballotsubs_info += edit_status + "</a><small class='d-block text-nowrap'>"

            if ballotsub.submitter_type == ballotsub.SUBMITTER_TABROOM:
                ballotsubs_info += _(" added by %(user)s") % {'user': ballotsub.submitter.username}
            elif ballotsub.submitter_type == ballotsub.SUBMITTER_PUBLIC:
                ballotsubs_info += _(" a public submission from %(ip_address)s") % {'ip_address': ballotsub.ip_address}

            ballotsubs_info += "</small>"

        if all(x.discarded for x in ballotsubmissions):
            link = reverse_tournament('results-ballotset-new' if self.admin else 'results-assistant-ballotset-new',
                                      self.tournament,
                                      kwargs={'debate_id': debate.id})
            ballotsubs_info += "<a href=" + link + ">" + _("Enter Ballot")  + "</a>"

        return ballotsubs_info

    def add_ballot_entry_columns(self, debates):

        entry_header = {'key': 'EB', 'icon': "plus-circle"}
        entry_cells = [{'text': self.get_ballot_text(d)} for d in debates]
        self.add_column(entry_header, entry_cells)

        if self.tournament.pref('enable_postponements'):
            postpones_header = {'title': _("Postpone"), 'key': "postpone"}
            postpones_cells = []
            for debate in debates:
                if debate.result_status == Debate.STATUS_POSTPONED:
                    text = '<a href="#" class="unpostpone-link" debate-id="{:d}">' + _("Unpostpone") + '</a>'
                else:
                    text = '<a href="#" class="postpone-link" debate-id="{:d}">' + _("Postpone") + '</a>'
                postpones_cells.append(text.format(debate.id))
            self.add_column(postpones_header, postpones_cells)
