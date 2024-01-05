CREATE TABLE user (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	full_name VARCHAR, 
	email VARCHAR NOT NULL, 
	password VARCHAR, 
	admin BOOLEAN, 
	role VARCHAR, 
	email_confirmed BOOLEAN, 
	user_api_key_hash VARCHAR, 
	billing_customer_id VARCHAR, 
	encrypted_totp_secret BLOB, 
	CONSTRAINT pk_user PRIMARY KEY (id)
);
CREATE TABLE club (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	email VARCHAR(255), 
	contact_number VARCHAR(50), 
	street_address VARCHAR(255), 
	state VARCHAR(100), 
	zip_code VARCHAR(15), 
	country VARCHAR(100), 
	CONSTRAINT pk_club PRIMARY KEY (id)
);
CREATE TABLE flask_dance_oauth (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	provider VARCHAR(50) NOT NULL, 
	created_at DATETIME NOT NULL, 
	token JSON NOT NULL, 
	provider_user_id VARCHAR(256) NOT NULL, 
	provider_user_login VARCHAR(256) NOT NULL, 
	user_id INTEGER NOT NULL, 
	CONSTRAINT pk_flask_dance_oauth PRIMARY KEY (id), 
	CONSTRAINT uq_flask_dance_oauth_provider UNIQUE (provider, provider_user_id), 
	CONSTRAINT fk_flask_dance_oauth_user_id_user FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE team (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	creator_id INTEGER NOT NULL, 
	name VARCHAR(255), 
	"plan" VARCHAR, 
	plan_owner_id INTEGER, 
	subscription_id VARCHAR, 
	billing_customer_id VARCHAR, 
	CONSTRAINT pk_team PRIMARY KEY (id), 
	CONSTRAINT fk_team_creator_id_user FOREIGN KEY(creator_id) REFERENCES user (id), 
	CONSTRAINT fk_team_plan_owner_id_user FOREIGN KEY(plan_owner_id) REFERENCES user (id)
);
CREATE INDEX ix_team_creator_id ON team (creator_id);
CREATE TABLE player (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	first_name VARCHAR, 
	last_name VARCHAR, 
	email VARCHAR, 
	contact_number VARCHAR, 
	communication_preference_mobile BOOLEAN, 
	communication_preference_email BOOLEAN, 
	gender VARCHAR, 
	club_ranking INTEGER, 
	club_id INTEGER, 
	CONSTRAINT pk_player PRIMARY KEY (id), 
	CONSTRAINT fk_player_club_id_club FOREIGN KEY(club_id) REFERENCES club (id) ON DELETE CASCADE
);
CREATE TABLE facility (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	type VARCHAR, 
	asset_description VARCHAR(100), 
	location_description VARCHAR(100), 
	name VARCHAR, 
	club_id INTEGER, 
	CONSTRAINT pk_facility PRIMARY KEY (id), 
	CONSTRAINT fk_facility_club_id_club FOREIGN KEY(club_id) REFERENCES club (id) ON DELETE CASCADE
);
CREATE TABLE league (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	type VARCHAR, 
	start_date DATETIME, 
	bg_color VARCHAR(7), 
	fg_color VARCHAR(7), 
	club_id INTEGER, 
	CONSTRAINT pk_league PRIMARY KEY (id), 
	CONSTRAINT fk_league_club_id_club FOREIGN KEY(club_id) REFERENCES club (id) ON DELETE CASCADE
);
CREATE TABLE team_member (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	team_id INTEGER NOT NULL, 
	user_id INTEGER, 
	invite_email VARCHAR(255), 
	role VARCHAR, 
	inviter_id INTEGER, 
	invite_secret VARCHAR(255), 
	activated BOOLEAN, 
	CONSTRAINT pk_team_member PRIMARY KEY (id), 
	CONSTRAINT fk_team_member_team_id_team FOREIGN KEY(team_id) REFERENCES team (id), 
	CONSTRAINT fk_team_member_user_id_user FOREIGN KEY(user_id) REFERENCES user (id), 
	CONSTRAINT fk_team_member_inviter_id_user FOREIGN KEY(inviter_id) REFERENCES user (id)
);
CREATE INDEX ix_team_member_team_id ON team_member (team_id);
CREATE INDEX ix_team_member_user_id ON team_member (user_id);
CREATE TABLE team_file (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	team_id INTEGER NOT NULL, 
	user_id INTEGER, 
	file_name VARCHAR, 
	description VARCHAR, 
	file_object_name VARCHAR, 
	activated BOOLEAN, 
	CONSTRAINT pk_team_file PRIMARY KEY (id), 
	CONSTRAINT fk_team_file_team_id_team FOREIGN KEY(team_id) REFERENCES team (id), 
	CONSTRAINT fk_team_file_user_id_user FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE INDEX ix_team_file_team_id ON team_file (team_id);
CREATE INDEX ix_team_file_user_id ON team_file (user_id);
CREATE TABLE facility_administrator (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	facility_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	CONSTRAINT pk_facility_administrator PRIMARY KEY (facility_id, user_id), 
	CONSTRAINT fk_facility_administrator_facility_id_facility FOREIGN KEY(facility_id) REFERENCES facility (id) ON DELETE CASCADE, 
	CONSTRAINT fk_facility_administrator_user_id_user FOREIGN KEY(user_id) REFERENCES user (id) ON DELETE CASCADE
);
CREATE TABLE league_rules (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	assume_busy BOOLEAN, 
	min_games_total INTEGER, 
	max_games_total INTEGER, 
	min_games_day INTEGER, 
	max_games_day INTEGER, 
	min_games_week INTEGER, 
	max_double_headers INTEGER, 
	max_concurrent_games INTEGER, 
	max_games_week INTEGER, 
	min_captained INTEGER, 
	max_captained INTEGER, 
	max_week_gap INTEGER, 
	players_per_match INTEGER, 
	minimum_subs_per_game FLOAT, 
	league_id INTEGER NOT NULL, 
	CONSTRAINT pk_league_rules PRIMARY KEY (id), 
	CONSTRAINT fk_league_rules_league_id_league FOREIGN KEY(league_id) REFERENCES league (id)
);
CREATE TABLE league_player_association (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	league_id INTEGER, 
	player_id INTEGER, 
	CONSTRAINT pk_league_player_association PRIMARY KEY (id), 
	CONSTRAINT fk_league_player_association_league_id_league FOREIGN KEY(league_id) REFERENCES league (id) ON DELETE CASCADE, 
	CONSTRAINT fk_league_player_association_player_id_player FOREIGN KEY(player_id) REFERENCES player (id) ON DELETE CASCADE
);
CREATE TABLE league_facility_association (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	league_id INTEGER, 
	facility_id INTEGER, 
	CONSTRAINT pk_league_facility_association PRIMARY KEY (id), 
	CONSTRAINT fk_league_facility_association_league_id_league FOREIGN KEY(league_id) REFERENCES league (id) ON DELETE CASCADE, 
	CONSTRAINT fk_league_facility_association_facility_id_facility FOREIGN KEY(facility_id) REFERENCES facility (id) ON DELETE CASCADE
);
CREATE TABLE flights (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	league_id INTEGER, 
	CONSTRAINT pk_flights PRIMARY KEY (id), 
	CONSTRAINT fk_flights_league_id_league FOREIGN KEY(league_id) REFERENCES league (id) ON DELETE CASCADE
);
CREATE TABLE timeslot (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	start_time DATETIME NOT NULL, 
	end_time DATETIME NOT NULL, 
	league_id INTEGER, 
	CONSTRAINT pk_timeslot PRIMARY KEY (id), 
	CONSTRAINT fk_timeslot_league_id_league FOREIGN KEY(league_id) REFERENCES league (id) ON DELETE CASCADE
);
CREATE TABLE player_availability (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	availability INTEGER, 
	association_id INTEGER, 
	timeslot_id INTEGER, 
	CONSTRAINT pk_player_availability PRIMARY KEY (id), 
	CONSTRAINT fk_player_availability_association_id_league_player_association FOREIGN KEY(association_id) REFERENCES league_player_association (id) ON DELETE CASCADE, 
	CONSTRAINT fk_player_availability_timeslot_id_timeslot FOREIGN KEY(timeslot_id) REFERENCES timeslot (id) ON DELETE CASCADE
);
CREATE TABLE league_game_event (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	is_captain BOOLEAN, 
	league_id INTEGER, 
	player_id INTEGER, 
	facility_id INTEGER, 
	timeslot_id INTEGER, 
	CONSTRAINT pk_league_game_event PRIMARY KEY (id), 
	CONSTRAINT fk_league_game_event_league_id_league FOREIGN KEY(league_id) REFERENCES league (id) ON DELETE CASCADE, 
	CONSTRAINT fk_league_game_event_player_id_player FOREIGN KEY(player_id) REFERENCES player (id) ON DELETE CASCADE, 
	CONSTRAINT fk_league_game_event_facility_id_facility FOREIGN KEY(facility_id) REFERENCES facility (id) ON DELETE CASCADE, 
	CONSTRAINT fk_league_game_event_timeslot_id_timeslot FOREIGN KEY(timeslot_id) REFERENCES timeslot (id) ON DELETE CASCADE
);
CREATE TABLE club_team_association (
	created DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
	deleted BOOLEAN, 
	id INTEGER NOT NULL, 
	is_admin BOOLEAN, 
	club_id INTEGER, 
	team_id INTEGER, 
	CONSTRAINT pk_club_team_association PRIMARY KEY (id), 
	CONSTRAINT fk_club_team_association_club_id_club FOREIGN KEY(club_id) REFERENCES club (id) ON DELETE CASCADE, 
	CONSTRAINT fk_club_team_association_team_id_team FOREIGN KEY(team_id) REFERENCES team (id) ON DELETE CASCADE
);
