class InfoClass {
    /**
     * @description This constructor function retrieves information from a DIV element
     * with the class name ".info" and sets it as class properties for further use.
     */
    constructor() {
        this.infoDiv = document.querySelector(".info");
        if (this.infoDiv) {
            this.captainChecked = new Image();
            this.captainChecked.src = this.infoDiv.getAttribute("captain_checked");
            this.captainUnchecked = new Image();
            this.captainUnchecked.src = this.infoDiv.getAttribute("captain_unchecked");
            this.captainWarning = new Image();
            this.captainWarning.src = this.infoDiv.getAttribute("captain_warning");
            this.faceNeutral = new Image();
            this.faceNeutral.src = this.infoDiv.getAttribute("face_neutral");
            this.faceNeutralWarning = new Image();
            this.faceNeutralWarning.src = this.infoDiv.getAttribute("face_neutral_warning");
            this.tennisRacket = new Image();
            this.tennisRacket.src = this.infoDiv.getAttribute("tennis_racket");
            this.tennisRacketWarning = new Image();
            this.tennisRacketWarning.src = this.infoDiv.getAttribute("tennis_racket_warning");
            this.leagueRulesMinGamesTotal = parseInt(this.infoDiv.getAttribute("league_rules_min_games_total"));
            this.leagueRulesMaxGamesTotal = parseInt(this.infoDiv.getAttribute("league_rules_max_games_total"));
            this.leagueRulesMaxPlayersPerMatch = parseInt(this.infoDiv.getAttribute("league_rules_max_players_per_match"));
            this.leagueRulesMaxGamesWeek = parseInt(this.infoDiv.getAttribute("league_rules_max_games_week"));
            this.leagueRulesMinGamesDay = parseInt(this.infoDiv.getAttribute("league_rules_min_games_day"));
            this.leagueRulesMaxGamesDay = parseInt(this.infoDiv.getAttribute("league_rules_max_games_day"));
            this.leagueRulesMaxWeekGap = parseInt(this.infoDiv.getAttribute("league_rules_max_week_gap"));
            this.leagueRulesMaxDoubleHeaders = parseInt(this.infoDiv.getAttribute("league_rules_max_double_headers"));
            this.leagueRulesMinCaptained = parseInt(this.infoDiv.getAttribute("league_rules_min_captained"));
            this.leagueRulesMaxCaptained = parseInt(this.infoDiv.getAttribute("league_rules_max_captained"));
            this.leagueRulesMinimumSubsPerGame = parseInt(this.infoDiv.getAttribute("league_rules_minimum_subs_per_game"));
            this.leagueRulesAssumeBusy = this.infoDiv.getAttribute("league_rules_assume_busy");
            this.flightIds = [];
            const flightIdElements = this.infoDiv.querySelectorAll('[data-flight-id]');
            flightIdElements.forEach(element => {
                const flightId = parseInt(element.getAttribute('data-flight-id'));
                if (!isNaN(flightId)) {
                    this.flightIds.push(flightId);
                }
            });
        } else {
            console.error("Info div not found.");
        }
    }
}
