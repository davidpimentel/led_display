from espn_api.football import League
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TeamScore:
    name: str
    score: float
    projected: float


@dataclass
class ScoreResult:
    your_team: TeamScore
    opponent_team: TeamScore


class FantasyFetcher:
    def __init__(self, league_id, team_id, espn_s2, swid):
        self.league_id = league_id
        self.team_id = team_id
        self.espn_s2 = espn_s2
        self.swid = swid
        self.year = datetime.now().year
        self.league = League(
            league_id=league_id, espn_s2=espn_s2, swid=swid, year=self.year
        )
        self.team = self.league.get_team_data(team_id)

    def get_live_score(self):
        # Get the league scoreboard
        box_scores = self.league.box_scores(week=self.league.current_week)

        # Find your team in the scoreboard
        for box_score in box_scores:
            matchup_teams = [box_score.home_team.team_id, box_score.away_team.team_id]
            if self.team_id in matchup_teams:
                is_home_team = self.team.team_id == box_score.home_team.team_id
                # Get the opponent's team

                result = ScoreResult(
                    your_team=TeamScore(
                        name=self.team.team_name,
                        score=box_score.home_score
                        if is_home_team
                        else box_score.away_score,
                        projected=box_score.home_projected
                        if is_home_team
                        else box_score.away_projected,
                    ),
                    opponent_team=TeamScore(
                        name=box_score.away_team.team_name
                        if is_home_team
                        else box_score.home_team.team_name,
                        score=box_score.away_score
                        if is_home_team
                        else box_score.home_score,
                        projected=box_score.away_projected
                        if is_home_team
                        else box_score.home_projected,
                    ),
                )

                return result

        return None
