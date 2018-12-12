# SI507project
## The data are available by using method provided on [SteamApi](https://steamcommunity.com/dev). There are instructions on the interfaces and methods further on [ValveDeveloperWiki](https://developer.valvesoftware.com/wiki/Steam_Web_API).
## There are four tables in the database, which are games, players, friends and player-game. The player-game and friends table are tables with many-to-many relationship and has foreign key to games and players table.
## The plot functions are plot_players_privacy(), plot_players_time(), plot_players_country() and plot_friends(PlayerId). These functions can help plot the charts with information listed
## Here are the instructions to execute final.py. [help](/help.txt)