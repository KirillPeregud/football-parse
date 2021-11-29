import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.fifa.com/tournaments/mens/worldcup/2018russia/teams/"


class Fifa:

    @staticmethod
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


class NationalTeam:

    def __init__(self, id_team, country):
        self.id = id_team
        self.country = country

    def create_players(self):
        self.page = requests.get(URL + self.id)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.all_data_players = self.soup.find_all("div", "fp-squad-player-card_playerDetails__2k2Nc")

        self.all_players = []
        for player in self.all_data_players:
            number_player = player.find("div", {"class": "fp-squad-player-card_jerseyNumber__1zPwG"}).text

            div_first_name_player = player.find("div", {"class": "fp-squad-player-card_firstName__1UtW_"})
            if div_first_name_player != None:
                first_name_player = div_first_name_player.text
            else:
                first_name_player = "-"

            div_last_name_player = player.find("div", {"class": "fp-squad-player-card_lastName__3KJvd"})
            if div_last_name_player != None:
                last_name_player = div_last_name_player.text
            else:
                last_name_player = player.find("span", {"class": "fp-squad-player-card_lastName__3KJvd"}).text

            position_player = player.find("div", {"class": "fp-squad-player-card_position__17FyP"}).text
            country_player = self.country

            new_player = Player(country_player, number_player, first_name_player, last_name_player, position_player)
            self.all_players.append(new_player)

        return self.all_players


class Player:

    def __init__(self, country, number, first_name, last_name, position):
        self.country = country
        self.number = number
        self.first_name = first_name
        self.last_name = last_name
        self.position = position

class OutputData:

    @staticmethod
    def data_to_csv(countries, numbers, first_names, last_names, positions):
        df = pd.DataFrame(
        {
        'country': countries,
        'number': numbers,
        'first_name': first_names,
        'last_name': last_names,
        'position': positions,
        }
    )
        df.to_csv('players_info.csv', mode='a', index=False, sep=';')


def main():
    teams_countries = []
    teams_numbers = []
    teams_first_names = []
    teams_last_names = []
    teams_positions = []

    fifa = Fifa()
    fifa_teams = fifa.get_all_teams()

    for new_id, new_name in fifa_teams.items():
        print(f'id: {new_id}; team: {new_name}', end='...')
        new_team = NationalTeam(new_id, new_name)
        all_players_team = new_team.create_players()

        for player in all_players_team:
            teams_countries.append(player.country)
            teams_numbers.append(player.number)
            teams_first_names.append(player.first_name)
            teams_last_names.append(player.last_name)
            teams_positions.append(player.position)

        print('OK')

    OutputData().data_to_csv(teams_countries, teams_numbers, teams_first_names, teams_last_names, teams_positions)


if __name__ == '__main__':
    main()
