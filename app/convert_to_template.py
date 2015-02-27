__author__ = 'The Gibs'

import re


def convert_scoreboard_to_template(scoreboard):
    template = str()
    header = "{{MatchRecapS4/Header|" + scoreboard.blue_team.short_name + "|" + scoreboard.red_team.short_name + "}}\n{{MatchRecapS4|gamename=" + scoreboard.game_name
    teams = "|team1=" + scoreboard.blue_team.short_name + "|team2=" + scoreboard.red_team.short_name
    scores = "|team1score=" + scoreboard.blue_team.score + "|team2score=" + scoreboard.red_team.score
    winner = "|winner="
    tournament_name = "|tournament=" + scoreboard.tournament_name
    lol_vod = "|lolvod=" + scoreboard.lol_vod
    youtube_vod = "|youtubevod=" + scoreboard.youtube_vod
    picks_and_bans_page = "|picksandbanspage=" + scoreboard.picks_and_bans_page
    if scoreboard.blue_team.conclusion == "  VICTORY  ":
        winner += "1"
    elif scoreboard.red_team.conclusion == "  VICTORY  ":
        winner += "2"
    team1bans = str()
    for i in range(0, scoreboard.blue_team.bans.__len__()):
        team1bans += "|team1ban" + str(i + 1) + "=" + scoreboard.blue_team.bans[i]
    team2bans = str()
    for i in range(0, scoreboard.red_team.bans.__len__()):
        team2bans += "|team2ban" + str(i + 1) + "=" + scoreboard.red_team.bans[i]
    date = "|date=" + scoreboard.date_played.strftime(
        '%Y-%m-%d') + "\n" + "|dst=" + scoreboard.daylight_savings + "|" + scoreboard.time_zone + "=" + scoreboard.start_time

    duration = "|gamelength=" + scoreboard.duration

    blue_players = str()
    for i in range(0, scoreboard.blue_team.players.__len__()):
        player_string = convert_player_info_to_template("blue", i, scoreboard.blue_team.players[i])
        blue_players += player_string + '\n'
    red_players = str()
    for i in range(0, scoreboard.red_team.players.__len__()):
        player_string = convert_player_info_to_template("purple", i, scoreboard.red_team.players[i])
        red_players += player_string + '\n'

    footer = "}}"

    template += header + teams + scores + winner + tournament_name + '\n' + lol_vod + youtube_vod + picks_and_bans_page + '\n' + team1bans + '\n' + team2bans + '\n' + date + '\n' + duration + '\n' + blue_players + '\n' + red_players + footer
    return template


def convert_player_info_to_template(team_color, player_number, player):
    player_intro = "|" + team_color + str(
        player_number + 1) + "={{MatchRecapS4/Player|champion=" + player.champion_name.champ_name + "|name=" + player.player_name + '\n'
    player_kda = "\t|kills=" + player.kills + "|deaths=" + player.deaths + "|assists=" + player.assists
    player_game_info = "|gold=" + player.gold + "|cs=" + player.cs + "|summonerspell1=" + player.summoner_spells[
        0].summoner_spell + "|summonerspell2=" + player.summoner_spells[1].summoner_spell + '\n'
    player_items = "\t|item1=" + player.items[0].item_name + "|item2=" + player.items[1].item_name + "|item3=" + \
                   player.items[2].item_name + "|item4=" + player.items[3].item_name + "|item5=" + player.items[
                       4].item_name + "|item6=" + player.items[5].item_name + "|trinket=" + player.trinket.item_name
    player_string = player_intro + player_kda + player_game_info + player_items + " }}"
    return player_string
