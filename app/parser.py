__author__ = 'The Gibs'
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from app import convert_to_template

import sys
import re
import csv




class ScoreBoard():
    def __init__(self):
        self.red_team = Team()
        self.blue_team = Team()
        self.match_url = str()
        self.date_played = str()
        self.duration = str()
        self.game_name = str()

    def load(self, driver):
        scoreboard = ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".scoreboard")))
        self.extract_bans(scoreboard)
        self.extract_team_score_and_conclusion(scoreboard)
        teams = scoreboard.find_elements_by_class_name("default-1-2")
        self.duration = driver.find_element_by_class_name("map-header-duration").text
        self.date_played = driver.find_element_by_css_selector(".map-header-date").text
        blue_team = teams[0].find_elements_by_css_selector(".player")
        red_team = teams[1].find_elements_by_css_selector(".player")
        for player in blue_team:
            final_player = self.extract_player_info(player)
            self.blue_team.players.append(final_player)
        for player in red_team:
            final_player = self.extract_player_info(player)
            self.red_team.players.append(final_player)
        self.get_short_names()
        self.remove_short_names_from_player_names()

    def extract_team_score_and_conclusion(self, scoreboard_element):
        team_conclusions = scoreboard_element.find_elements_by_class_name("game-conclusion")
        self.blue_team.conclusion = team_conclusions[0].text
        self.red_team.conclusion = team_conclusions[1].text


    def extract_bans(self, scoreboard_element):
        bans = scoreboard_element.find_elements_by_class_name("bans")
        blue_bans = bans[0].find_elements_by_class_name("champion-nameplate-icon")
        red_bans = bans[1].find_elements_by_class_name("champion-nameplate-icon")
        for ban in red_bans:
            ban_image = ban.find_element_by_tag_name("img").get_attribute("src")
            ban_image_results = re.search("champion/(.*).png", ban_image)
            ban_champ_name = ban_image_results.group(1)
            self.red_team.bans.append(ban_champ_name)
        for ban in blue_bans:
            ban_image = ban.find_element_by_tag_name("img").get_attribute("src")
            ban_image_results = re.search("champion/(.*).png", ban_image)
            ban_champ_name = ban_image_results.group(1)
            self.blue_team.bans.append(ban_champ_name)

    def extract_player_info(self, player_element):
        player_name = player_element.find_element_by_class_name("champion-nameplate-name").text
        level = player_element.find_element_by_class_name("champion-nameplate-level").text
        champ_img = player_element.find_element_by_tag_name("img").get_attribute("src")
        champ_name_results = re.search("champion/(.*).png", champ_img)
        champ_name = champ_name_results.group(1)
        summoner_spell_elements = player_element.find_elements_by_css_selector(".spell-icon")
        summoner_spells = []
        for summoner_spell_element in summoner_spell_elements:
            summoner_image = summoner_spell_element.find_element_by_tag_name("img").get_attribute("src")
            summoner_spell = re.search("spell/(.*).png", summoner_image).group(1)
            summoner_spells.append(SummonerSpell(summoner_spell))
        cs = player_element.find_element_by_css_selector(".cs").text
        gold = re.sub("k", "", player_element.find_element_by_css_selector(".gold").text)
        kda = player_element.find_element_by_css_selector(".kda").text
        kda_results = re.search("(\d*)/(\d*)/(\d*)", kda)
        kills = kda_results.group(1)
        deaths = kda_results.group(2)
        assists = kda_results.group(3)
        item_elements = player_element.find_elements_by_css_selector(".item-icon")
        items = []
        for item_element in item_elements:
            try:
                item_img = item_element.find_element_by_tag_name("img").get_attribute("src")
                item_img_results = re.search("item/(\d*)", item_img)
                item_number = item_img_results.group(1)
                items.append(Item(item_number))
            except:
                item = Item("")
                items.append(item)

        final_player = Player(player_name,champ_name, level, kills, deaths, assists, cs, gold, items, summoner_spells)
        return final_player


    def get_short_names(self):
        self.blue_team.short_name = re.search("(.*)\s",self.blue_team.players[0].player_name).group(1)
        self.red_team.short_name = re.search("(.*)\s",self.red_team.players[0].player_name).group(1)

    def remove_short_names_from_player_names(self):
        for player in self.blue_team.players:
            player.player_name = re.search(".*\s(.*)", player.player_name).group(1)
        for player in self.red_team.players:
            player.player_name = re.search(".*\s(.*)", player.player_name).group(1)




class Team():
    def __init__(self):
        self.short_name = str()
        self.players = []
        self.bans = []
        self.conclusion = str()
        self.score = str()

class Player():
    def __init__(self, player_name, champion_name, level, kills, deaths, assists, cs, gold, items, summoner_spells):
        self.player_name = player_name
        self.champion_name = champion_name
        self.level = level
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.cs = cs
        self.gold = gold
        self.items = items
        self.trinket = items.pop()
        self.summoner_spells = summoner_spells

class SummonerSpell():

    def __init__(self, unconverted_text):
        self.summoner_spell = str()
        if unconverted_text == "SummonerTeleport":
            self.summoner_spell = "Teleport"
        elif unconverted_text == "SummonerFlash":
            self.summoner_spell = "Flash"
        elif unconverted_text == "SummonerDot":
            self.summoner_spell = "Ignite"
        elif unconverted_text == "SummonerHeal":
            self.summoner_spell = "Heal"
        elif unconverted_text == "SummonerSmite":
            self.summoner_spell = "Smite"
        elif unconverted_text == "SummonerBarrier":
            self.summoner_spell = "Barrier"
        elif unconverted_text == "SummonerExhaust":
            self.summoner_spell = "Exhaust"
        elif unconverted_text == "SummonerRevive":
            self.summoner_spell = "Revive"
        elif unconverted_text == "SummonerGhost":
            self.summoner_spell = "Ghost"
        elif unconverted_text == "SummonerCleanse":
            self.summoner_spell = "Cleanse"
        elif unconverted_text == "SummonerGarrison":
            self.summoner_spell = "Garrison"
        elif unconverted_text == "SummonerClairvoyance":
            self.summoner_spell = "Clairvoyance"
        elif unconverted_text == "SummonerClarity":
            self.summoner_spell = "Clarity"
        else:
            self.summoner_spell = "Error Reading Summoner Spells"


class Item():
    def __init__(self, item_number):
        self.item_name = str()
        if item_number is not '':
            self.item_name = self.convert_item_number_to_text(item_number)
        else:
            self.item_name = " "
    def convert_item_number_to_text(self, item_number):
        int_item_number = int(item_number)
        item_name = item_dict.get(int_item_number)
        if not item_name:
            item_name = "Item Not Currently in Database"
        return item_name


def spider(url, game_name, blue_score, purple_score):
    driver = webdriver.Firefox()
    driver.get(url)
    current_match = ScoreBoard()
    current_match.match_url = url
    if game_name:
        current_match.game_name = game_name
    else:
        current_match.game_name = "Game 1"
    if blue_score and purple_score:
        current_match.blue_team.score = blue_score
        current_match.red_team.score = purple_score
    else:
        if current_match.blue_team.conclusion == "VICTORY":
            current_match.blue_team.score = "1"
            current_match.red_team.score = "0"
        else:
            current_match.blue_team.score = "0"
            current_match.red_team.score = "1"


    current_match.load(driver)
    template = convert_to_template.convert_scoreboard_to_template(current_match)
    driver.quit()
    return template

def load_item_numbers():
    file = open('app/item_numbers.csv')
    csv_file = csv.reader(file)
    global item_dict
    item_dict = {}
    for row in csv_file:
        item_dict.update({int(row[1]):row[0]})
