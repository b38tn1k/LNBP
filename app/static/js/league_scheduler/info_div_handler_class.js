class InfoClass {
    /**
     * @description This constructor function retrieves information from a DIV element
     * with the class name ".info" and sets it as class properties for further use.
     */
    constructor() {
        // Get the info div element by its class name
        this.infoDiv = document.querySelector(".info");

        // Check if the info div exists
        if (this.infoDiv) {
            this.captainChecked = new Image();
            this.captainChecked.src = this.infoDiv.getAttribute("captain_checked");

            this.captainUnchecked = new Image();
            this.captainUnchecked.src = this.infoDiv.getAttribute("captain_unchecked");

            this.faceNeutral = new Image();
            this.faceNeutral.src = this.infoDiv.getAttribute("face_neutral");

            this.faceNeutralWarning = new Image();
            this.faceNeutralWarning.src = this.infoDiv.getAttribute("face_neutral_warning");

            this.tennisRacket = new Image();
            this.tennisRacket.src = this.infoDiv.getAttribute("tennis_racket_warning");

            this.tennisRacketWarning = new Image();
            this.tennisRacketWarning.src = this.infoDiv.getAttribute("tennis_racket");

            // Additional attributes
            this.leagueRulesMinGamesTotal = this.infoDiv.getAttribute("league_rules_min_games_total");
            this.leagueRulesMaxGamesTotal = this.infoDiv.getAttribute("league_rules_max_games_total");
            this.leagueRulesMaxPlayersPerMatch = this.infoDiv.getAttribute("league_rules_max_players_per_match");
            this.leagueRulesMaxGamesWeek = this.infoDiv.getAttribute("league_rules_max_games_week");
            this.leagueRulesMinGamesDay = this.infoDiv.getAttribute("league_rules_min_games_day");
            this.leagueRulesMaxGamesDay = this.infoDiv.getAttribute("league_rules_max_games_day");
            this.leagueRulesMaxWeekGap = this.infoDiv.getAttribute("league_rules_max_week_gap");
            this.leagueRulesMaxDoubleHeaders = this.infoDiv.getAttribute("league_rules_max_double_headers");
            this.leagueRulesMinCaptained = this.infoDiv.getAttribute("league_rules_min_captained");
            this.leagueRulesMinimumSubsPerGame = this.infoDiv.getAttribute("league_rules_minimum_subs_per_game");
            this.leagueRulesAssumeBusy = this.infoDiv.getAttribute("league_rules_assume_busy");
        } else {
            console.error("Info div not found.");
        }
    }
}
