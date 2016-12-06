#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the records from matches table"""
    db = connect()
    db_curs = db.cursor()
    qry = "DELETE FROM matches"
    db_curs.execute(qry)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the records from players table"""
    db = connect()
    db_curs = db.cursor()
    qry = "DELETE FROM players"
    db_curs.execute(qry)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    db_curs = db.cursor()
    qry = "SELECT count(id) AS num FROM players"
    db_curs.execute(qry)
    results = db_curs.fetchone()
    db.close()
    if results:
        return results[0]
    else:
        return 0


def countMatches():
    """Returns the number of matches played."""
    db = connect()
    db_curs = db.cursor()
    qry = "SELECT count(*) AS num FROM matches"
    db_curs.execute(qry)
    results = db_curs.fetchone()
    db.close()
    if results:
        return results[0]
    else:
        return 0


def registerPlayer(name):
    """Adds a player to the players table.
        The database assigns a unique serial id number for the player.
    Args:
      name: the player's full name
    """
    db = connect()
    db_curs = db.cursor()
    db_curs.execute("INSERT INTO players(name) VALUES(%s)", (name,))
    db.commit()
    db.close()


def getWinnerCount(player_id):
    """Returns count of wins for a player.
    Args:
      player_id: the player's id
    Returns:
        wins: the number of matches the player has won
    """
    db = connect()
    db_curs = db.cursor()
    db_curs.execute("SELECT count(*) FROM matches WHERE winner = (%s)", (player_id,))
    winner_result = db_curs.fetchone()
    db.close()
    return winner_result[0]


def getLoserCount(player_id):
    """Returns count of loses for a player.
    Args:
      player_id: the player's id
    Returns:
        loses: the number of matches the player has lost
    """
    db = connect()
    db_curs = db.cursor()
    db_curs.execute("SELECT count(*) FROM matches WHERE loser = (%s)", (player_id,))
    loser_result = db_curs.fetchone()
    db.close()
    return loser_result[0]


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    db_curs = db.cursor()
    db_curs.execute("INSERT INTO matches(winner,loser) VALUES(%s,%s)",  (winner,loser,))
    db.commit()
    db.close()


def getPlayerNameFromPlayers(player_id):
    """Returns player name.
    Args:
      player_id: the player's id
    Returns:
        name: the name of the player
    """
    db = connect()
    db_curs = db.cursor()
    db_curs.execute("SELECT name FROM players WHERE id = (%s)", (player_id,))
    name = db_curs.fetchone()
    db.close()
    return name[0]


def getAllIdsFromPlayersInAList():
    """Returns list of player ids
    Returns:
        id_list: return list ids of all players in the players table
    """
    db = connect()
    db_curs = db.cursor()
    qry = "SELECT players.id FROM players"
    db_curs.execute(qry)
    results = db_curs.fetchall()
    db.close()
    id_list = []
    for val in results:
        id_list.append(val[0])
    return id_list


def getAllIdsFromViewWinTotalInAList():
    """Returns list of player ids
    Returns:
        id_list: return list ids of all winners using view based on players and matches tables
    """
    db = connect()
    db_curs = db.cursor()
    qry = "SELECT * FROM view_win_total"
    db_curs.execute(qry)
    results = db_curs.fetchall()
    db.close()
    id_list = []
    for val in results:
        id_list.append(val[0])
    return id_list


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # check if there are records in matches table
    match_count = countMatches()
    if match_count == 0:
        # execute query to return id, name, winner set to 0 and total matches set to 0
        db = connect()
        db_curs = db.cursor()
        qry = "SELECT players.id, name," \
              " COALESCE(matches.winner,0), COALESCE(matches.loser,0)" \
              " FROM players LEFT JOIN matches ON players.id = matches.id"
        db_curs.execute(qry)
        results = db_curs.fetchall()
        db.close()
        if results:
            return results
        else:
            return []
    else:
        # execute query on view to return id, name and number of wins
        # also call functions to get total of wins and loses for a player
        all_winners = []
        db = connect()
        db_curs = db.cursor()
        qry = "SELECT * FROM view_win_total"
        db_curs.execute(qry)
        results = db_curs.fetchall()
        db_curs.close()
        db.close()
        if results:
            for(row) in results:
                row_list = []
                player_id = row[0]
                win_count = getWinnerCount(player_id)
                lose_count = getLoserCount(player_id)
                row_list.append(player_id)
                row_list.append(row[1])
                row_list.append(row[2])
                row_list.append(win_count + lose_count)
                all_winners.append(row_list)
            return all_winners
        else:
            return []


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # check if there are records in matches table
    match_count = countMatches()
    if match_count == 0:
        # return a default list of standings before any match has been played
        all_id_list = getAllIdsFromPlayersInAList()
        if all_id_list:
            id_pair_list = []
            for index in range (len(all_id_list)):
                if index%2 == 0:
                    tup = (all_id_list[index], all_id_list[index+1])
                    id_pair_list.append(tup)
            return id_pair_list
        else:
            return []
    else:
        # logic to get list of tuples, each of which contains (id1, name1, id2, name2)
        # get list of all players id from players table
        all_id_list = getAllIdsFromPlayersInAList()

        # get list of all winner id from view_win_total
        all_winner_id_list = getAllIdsFromViewWinTotalInAList()

        # create list of winners sorted by wins and append with id who have not won a single match
        all_won_or_lost_list = []
        for val in all_winner_id_list:
            all_won_or_lost_list.append(val)
        for val in all_id_list:
            if val in all_won_or_lost_list:
                continue
            else:
                all_won_or_lost_list.append(val)

        #now create the tuple list using player id and player name
        pair_list = []
        for index in range(len(all_won_or_lost_list)):
            if index % 2 == 0:
                player_one_id = all_won_or_lost_list[index]
                player_two_id = all_won_or_lost_list[index+1]
                player_one_name = getPlayerNameFromPlayers(player_one_id)
                player_two_name =  getPlayerNameFromPlayers(player_two_id)
                pair_tuple = (player_one_id, player_one_name, player_two_id, player_two_name)
                pair_list.append(pair_tuple)
        return pair_list