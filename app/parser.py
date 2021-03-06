__author__ = 'The Gibs'
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from app import convert_to_template
from datetime import datetime
import sys
import re
import csv


class ScoreBoard():
    def __init__(self, match_url, game_name, tournament_name, daylight_savings, start_time, time_zone, lol_vod,
                 youtube_vod, picks_and_bans_page):
        self.red_team = Team()
        self.blue_team = Team()
        self.tournament_name = tournament_name
        self.blue_team.score = str()
        self.red_team.score = str()
        self.match_url = match_url
        self.date_played = datetime
        self.duration = str()
        self.game_name = game_name
        self.daylight_savings = daylight_savings
        self.start_time = start_time
        self.time_zone = time_zone
        self.lol_vod = lol_vod
        self.youtube_vod = youtube_vod
        self.picks_and_bans_page = picks_and_bans_page


    def load(self, driver):
        ui.WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".scoreboard")))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source)
        try:
            driver.quit()
        except:
            pass
        self.extract_bans(soup)
        self.extract_conclusion(soup)
        self.duration = soup.find('span', class_='map-header-duration').text
        self.date_played = datetime.strptime(soup.find('span', class_='map-header-date').text, '%m/%d/%Y')
        soupy_players = soup.find_all('div', class_='player')
        blue_team = soupy_players[0:5]
        red_team = soupy_players[5:10]
        for player in blue_team:
            final_player = self.extract_player_info(player)
            self.blue_team.players.append(final_player)
        for player in red_team:
            final_player = self.extract_player_info(player)
            self.red_team.players.append(final_player)
        self.get_short_names()
        self.remove_short_names_from_player_names()


    def extract_bans(self, soup):
        soupy_bans = soup.find_all('div', class_='bans')
        blue_bans = soupy_bans[0].find_all('div', class_='champion-icon')
        red_bans = soupy_bans[1].find_all('div', class_='champion-icon')
        for ban in blue_bans:
            data = re.search("img/champion/(.*).png", str(ban.contents[0])).group(1)
            fixed_ban = ChampionName(data)
            self.blue_team.bans.append(fixed_ban.champ_name)
        for ban in red_bans:
            data = re.search("img/champion/(.*).png", str(ban.contents[0])).group(1)
            fixed_ban = ChampionName(data)
            self.red_team.bans.append(fixed_ban.champ_name)

    def extract_conclusion(self, soup):
        soupy_conclusions = soup.find_all('div', class_='game-conclusion')
        self.blue_team.conclusion = soupy_conclusions[0].text
        self.red_team.conclusion = soupy_conclusions[1].text


    def extract_player_info(self, player_element):
        player_name = player_element.find('div', class_='champion-nameplate-name').find('span').text
        level = player_element.find('span', class_='champion-nameplate-level').text
        champ_img = str(player_element.find('div', class_='champion-icon'))
        champ_name_results = re.search("champion/(.*).png", champ_img)
        champ_name = champ_name_results.group(1)
        summoner_spell_elements = player_element.find_all('div', class_='spell-icon')
        summoner_spells = []
        for summoner_spell_element in summoner_spell_elements:
            summoner_image = str(summoner_spell_element.contents[0])
            summoner_spell = re.search("spell/(.*).png", summoner_image).group(1)
            summoner_spells.append(SummonerSpell(summoner_spell))
        cs = player_element.find('div', class_='minions-col').text
        gold = re.sub("k", "", player_element.find('div', class_='gold-col').text)
        kda = player_element.find('div', class_='kda-kda').text
        kda_results = re.search("(\d*)/(\d*)/(\d*)", kda)
        kills = kda_results.group(1)
        deaths = kda_results.group(2)
        assists = kda_results.group(3)
        item_elements = player_element.find_all('div', class_='item-icon')
        items = []
        for item_element in item_elements:
            try:
                item_img = str(item_element.contents[0])
                item_img_results = re.search("item/(\d*)", item_img)
                item_number = item_img_results.group(1)
                items.append(Item(item_number))
            except:
                item = Item("")
                items.append(item)

        final_player = Player(player_name, champ_name, level, kills, deaths, assists, cs, gold, items, summoner_spells)
        return final_player


    def get_short_names(self):
        self.blue_team.short_name = re.search("(.*)\s", self.blue_team.players[0].player_name).group(1)
        self.red_team.short_name = re.search("(.*)\s", self.red_team.players[0].player_name).group(1)


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
        self.champion_name = ChampionName(champion_name)
        self.level = level
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.cs = cs
        self.gold = gold
        self.items = items
        self.trinket = items.pop()
        self.summoner_spells = summoner_spells


class ChampionName():
    def __init__(self, champion_name):
        self.champ_name = self.convert_special_names(champion_name)

    def convert_special_names(self, champion_name):
        champ_name = champ_name_dict.get(champion_name)
        if not champ_name:
            return champion_name  # Not a special champ name
        return champ_name


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
        elif unconverted_text == "SummonerHaste":
            self.summoner_spell = "Ghost"
        elif unconverted_text == "SummonerBoost":
            self.summoner_spell = "Cleanse"
        elif unconverted_text == "SummonerOdinGarrison":
            self.summoner_spell = "Garrison"
        elif unconverted_text == "SummonerClairvoyance":
            self.summoner_spell = "Clairvoyance"
        elif unconverted_text == "SummonerMana":
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


def spider(url, game_name, tournament_name, blue_score, purple_score, daylight_savings, start_time, time_zone, lol_vod,
           youtube_vod, picks_and_bans_page):
    try:
        driver = webdriver.Firefox()  # driver = webdriver.PhantomJS(executable_path='app\phantomjs.exe')
        driver.get(url)
        driver.refresh()  # bullshit workaround
        if not game_name:
            game_name = "Game 1"
        current_match = ScoreBoard(url, game_name, tournament_name, daylight_savings, start_time, time_zone, lol_vod,
                                   youtube_vod, picks_and_bans_page)
        current_match.load(driver)
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

        template = convert_to_template.convert_scoreboard_to_template(current_match)
        return template
    except:
        driver.quit()
        return "Error Parsing URL, make sure all fields are filled correctly"



def load_item_numbers():
    file = open('app/item_numbers.csv')
    csv_file = csv.reader(file)
    global item_dict
    item_dict = {}
    for row in csv_file:
        item_dict.update({int(row[1]): row[0]})


def load_special_champ_names():
    file = open('app/special_champ_names.csv')
    csv_file = csv.reader(file)
    global champ_name_dict
    champ_name_dict = {}
    for row in csv_file:
        champ_name_dict.update({row[0]: row[1]})
