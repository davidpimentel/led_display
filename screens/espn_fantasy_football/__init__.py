from dataclasses import dataclass

from lib.colors import COLORS
from lib.fonts import FONTS
from rgbmatrix import graphics
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
        self.font = FONTS["4x6"]

    def setup(self):
        self.create_interval(self._fetch_scores, seconds=30)

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

    def render(self, canvas, state: FantasyFootballState):
        graphics.DrawText(canvas, self.font, 4, 10, COLORS["white"], state.your_score)
        graphics.DrawText(
            canvas, self.font, 4, 20, COLORS["gray"], state.your_projected
        )
        graphics.DrawText(
            canvas, self.font, 32, 10, COLORS["white"], state.their_score
        )
        graphics.DrawText(
            canvas, self.font, 32, 20, COLORS["gray"], state.their_projected
        )
