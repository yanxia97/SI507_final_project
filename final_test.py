import unittest
import final
import get_data

class TestGetNum(unittest.TestCase):
    def test_get_player_num(self):
        self.assertEqual(final.get_number(),1251)
    def test_get_game_num(self):
        self.assertEqual(final.get_game_number(),129)

class TestPlot(unittest.TestCase):
    def test_plot_friend(self):
        try:    
            get_data.get_player_summary("76561197960435530")
            get_data.add_player_summary("76561197960265731")
            get_data.add_player_summary("76561197960265738")        
            final.plot_friends(1)
            final.plot_friends(2)
        except:
            self.fail()

    def test_plot_category(self):
        try:
            final.plot_players_time()
            final.plot_players_privacy()
            final.plot_players_country()
        except:
            self.fail()


class TestGetPlayer(unittest.TestCase):
    def test_create_player(self):
        try:
            get_data.get_player_summary("76561197960435530")
            get_data.get_player_summary("76561197960265731")
        except:
            self.fail()

    def test_add_player(self):
        try:
            get_data.get_player_summary("76561197960435530")
            get_data.add_player_summary("76561197960265731")
            get_data.add_player_summary("76561197960265738")
        except:
            self.fail()

class TestGetFriends(unittest.TestCase):
    def test_create_friend(self):
        try:
            get_data.get_friend_list("76561197960435530")
            get_data.get_friend_list("76561197960265731")
        except:
            self.fail()

    def test_add_player(self):
        try:
            get_data.get_friend_list("76561197960435530")
            get_data.add_friend_list("76561197960265731")
            get_data.add_friend_list("76561197960265738")
        except:
            self.fail()

class TestGetGames(unittest.TestCase):
    def test_create_friend(self):
        try:
            get_data.get_game_list("76561197960435530")
            get_data.get_game_list("76561197960265731")
        except:
            self.fail()

    def test_add_player(self):
        try:
            get_data.get_game_list("76561197960435530")
            get_data.add_game_list("76561197960265731")
            get_data.add_game_list("76561197960265738")
        except:
            self.fail()

if __name__ == '__main__':
    unittest.main()