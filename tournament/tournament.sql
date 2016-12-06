-- Table definitions for the tournament project.

DROP VIEW view_win_total;
DROP TABLE matches;
DROP TABLE players;

-- Players table
CREATE TABLE players (id SERIAL PRIMARY KEY, name TEXT);

-- Matches table
CREATE TABLE matches (id SERIAL PRIMARY KEY, winner INTEGER REFERENCES players(id), loser INTEGER REFERENCES players(id));

-- win total view
CREATE VIEW view_win_total AS
    SELECT players.id, players,name, COUNT(players.id) AS win_total
    FROM players, matches
    WHERE players.id = matches.winner
    GROUP BY players.id
    ORDER BY win_total DESC;
