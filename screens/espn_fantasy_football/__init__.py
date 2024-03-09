from lib.colors import COLORS
from lib.fonts import FONTS
from rgbmatrix import graphics
from screens.base_screen import BaseScreen
from .fetch_matchup import FantasyFetcher, ScoreResult


class Screen(BaseScreen):
    def __init__(self, espn_s2=None, swid=None, league_id=None, team_id=None):
        super().__init__(display_indefinitely=True)
        self.league_id = league_id
        self.team_id = team_id
        self.espn_s2 = espn_s2
        self.swid = swid
        self.fetcher = None
        self.font = FONTS["4x6"]

    def fetch_data_interval(self):
        return 30

    def fetch_data(self):
        if self.fetcher is None:
            self.fetcher = FantasyFetcher(
                self.league_id, self.team_id, self.espn_s2, self.swid
            )
        return self.fetcher.get_live_score()

    def render(self, canvas, data: ScoreResult):
        if data is not None:
            your_score = str(data.your_team.score)
            your_projected = str(data.your_team.projected)
            their_score = str(data.opponent_team.score)
            their_projected = str(data.opponent_team.projected)
        else:
            your_score = "--"
            your_projected = "--"
            their_score = "--"
            their_projected = "--"

        graphics.DrawText(canvas, self.font, 4, 10, COLORS["white"], your_score)
        graphics.DrawText(canvas, self.font, 4, 20, COLORS["gray"], your_projected)
        graphics.DrawText(canvas, self.font, 32, 10, COLORS["white"], their_score)
        graphics.DrawText(canvas, self.font, 32, 20, COLORS["gray"], their_projected)
