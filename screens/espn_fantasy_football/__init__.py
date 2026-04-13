from dataclasses import dataclass

from lib.colors import Colors
from lib.ui import Positioned, Stack, Text
from screens.base_screen import BaseScreen

from .fetch_matchup import FantasyFetcher


@dataclass
class FantasyFootballState:
    your_score: str = "--"
    your_projected: str = "--"
    their_score: str = "--"
    their_projected: str = "--"


class Screen(BaseScreen[FantasyFootballState]):
    def __init__(self, espn_s2=None, swid=None, league_id=None, team_id=None):
        super().__init__(
            initial_state=FantasyFootballState(), display_indefinitely=True
        )
        self.league_id = league_id
        self.team_id = team_id
        self.espn_s2 = espn_s2
        self.swid = swid
        self.fetcher = None

    def setup(self):
        self.run_on_interval(self._fetch_scores, seconds=30)

    def _fetch_scores(self):
        if self.fetcher is None:
            self.fetcher = FantasyFetcher(
                self.league_id, self.team_id, self.espn_s2, self.swid
            )
        result = self.fetcher.get_live_score()
        if result is not None:
            self.set_state(
                your_score=str(result.your_team.score),
                your_projected=str(result.your_team.projected),
                their_score=str(result.opponent_team.score),
                their_projected=str(result.opponent_team.projected),
            )

    def build(self, state: FantasyFootballState):
        return Stack(children=[
            Positioned(x=4, y=4, child=Text(state.your_score, font="4x6", color=Colors.white)),
            Positioned(x=4, y=14, child=Text(state.your_projected, font="4x6", color=Colors.gray)),
            Positioned(x=32, y=4, child=Text(state.their_score, font="4x6", color=Colors.white)),
            Positioned(x=32, y=14, child=Text(state.their_projected, font="4x6", color=Colors.gray)),
        ])
