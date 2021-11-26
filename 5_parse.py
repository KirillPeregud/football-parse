import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.fifa.com/tournaments/mens/worldcup/2018russia/teams/"


class NationalTeam:

    def __init__(self, id_team, country):
        self.id = id_team
        self.country = country
        self.page = requests.get(URL + self.id)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.all_data_players = self.soup.find_all("div", "fp-squad-player-card_playerDetails__2k2Nc")

    def create_players(self):
        self.all_players = []

        for player in self.all_data_players:
            number_player = player.find("div", {"class": "fp-squad-player-card_jerseyNumber__1zPwG"}).text

            try:
                first_name_player = player.find("div", {"class": "fp-squad-player-card_firstName__1UtW_"}).text
            except:
                first_name_player = "-"

            try:
                last_name_player = player.find("div", {"class": "fp-squad-player-card_lastName__3KJvd"}).text
            except:
                last_name_player = player.find("span", {"class": "fp-squad-player-card_lastName__3KJvd"}).text

            position_player = player.find("div", {"class": "fp-squad-player-card_position__17FyP"}).text
            country_player = self.country

            new_player = Player(country_player, number_player, first_name_player, last_name_player, position_player)
            self.all_players.append(new_player)

    def get_data_team(self):

        self.team_country = []
        self.team_numbers = []
        self.team_first_names = []
        self.team_last_names = []
        self.team_positions = []

        for player in self.all_players:
            self.team_country.append(player.country)
            self.team_numbers.append(player.number)
            self.team_first_names.append(player.first_name)
            self.team_last_names.append(player.last_name)
            self.team_positions.append(player.position)


class Player:

    def __init__(self, country, number, first_name, last_name, position):
        self.country = country
        self.number = number
        self.first_name = first_name
        self.last_name = last_name
        self.position = position


def get_all_teams():
    page_teams = requests.get(URL)
    soup_teams = BeautifulSoup(page_teams.content, "html.parser")
    info_teams = soup_teams.find_all("div", "col-6 col-lg-3")

    all_teams = {}
    for team in info_teams:
        id_team = team.find("a").get("href").split("/")[1]
        name_team = team.find("div", {"class": "ff-display-card_displayCardTeam__12mcx"}).text
        all_teams.update({id_team: name_team})

    return all_teams


def main():
    data_teams = get_all_teams()
    header_csv = True

    for new_id, new_name in data_teams.items():
        print(f'id: {new_id}; team: {new_name}', end='...')
        new_team = NationalTeam(new_id, new_name)
        new_team.create_players()
        new_team.get_data_team()

        df = pd.DataFrame(
            {
            'country': new_team.team_country,
            'number': new_team.team_numbers,
            'first_name': new_team.team_first_names,
            'last_name': new_team.team_last_names,
            'position': new_team.team_positions,
            }
        )

        df.to_csv('players_info.csv', mode='a', index=False, header=header_csv, sep=';')
        print('OK')
        header_csv = False


main()


if '__name__' == '__main__':
    main()
