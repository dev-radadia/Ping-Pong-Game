import pygame

from datetime import datetime

from enum import Enum

import r

import screens

import mysql.connector as scon

def main():
    global game, main_menu, player_names, pause_screen, endgame_screen, about_screen, db_con
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(22050, -16, 1, 512)
    pygame.display.set_caption(r.main.r_title_label_txt)

    default_bg=pygame.image.load("image\\bg_default.jpg")

    screen = pygame.display.set_mode((r.game.SCREEN_WIDTH, r.game.SCREEN_HEIGHT), pygame.FULLSCREEN)

    game_screen = Screen.MENU

    game=screens.game.GameScreen(screen, (r.game.SCREEN_WIDTH, r.game.SCREEN_HEIGHT), r.colors.BLACK, r.colors.WHITE, r.game.SCORE_MARGIN, r.game.FPS)
    game.setPaddleMargin(r.game.PADDLE_MARGIN)
    game.setPaddleSpeed(r.game.PADDLE_SPEED)
    game.setBallResetMargin(r.game.BALL_RESET_Y_MARGIN)
    game.setBounceBias(r.game.PADDLE_BOUNCE_BIAS)
    game.setBounceAcceleration(r.game.BALL_BOUNCE_ACC)
    game.setGameObjective(r.game.game_obj_txt)
    game.setMovables(r.game.BALL_HEIGHT, (r.game.PADDLE_WIDTH, r.game.PADDLE_HEIGHT), r.colors.WHITE, r.colors.WHITE)

    main_menu=screens.main_menu.MainMenuScreen(screen, r.main.r_title_label_txt, (r.game.SCREEN_WIDTH, r.game.SCREEN_HEIGHT), r.colors.BLACK, r.colors.WHITE, bg=default_bg)

    player_names=screens.playernames.PlayerNamesScreen(screen, r.playernames.playernames_label_txt, r.playernames.p_label_txt, r.playernames.ai_label_txt, r.playernames.p1_label_txt, r.playernames.p2_label_txt, r.playernames.name_label_txt, (r.game.SCREEN_WIDTH, r.game.SCREEN_HEIGHT), r.colors.BLACK, r.colors.WHITE, bg=default_bg)

    pause_screen=screens.pause.PauseScreen(screen, r.pause.paused_label_txt, (r.game.SCREEN_WIDTH, r.game.SCREEN_HEIGHT), r.colors.BLACK, r.colors.WHITE, bg=default_bg)

    endgame_screen=screens.endgame.EndgameScreen(screen, r.endgame.win_statement, (r.game.SCREEN_WIDTH, r.game.SCREEN_HEIGHT), r.colors.BLACK, bg=default_bg)

    about_screen=screens.about.AboutScreen(screen, r.about.text_about, (r.game.SCREEN_WIDTH, r.game.SCREEN_HEIGHT), r.colors.BLACK, r.colors.WHITE, bg=default_bg)

    initiateConnection()

    while True:
        if game_screen == Screen.MENU:
            game_screen = start_menu(screen)

        if game_screen == Screen.PLAYER1:
            game_screen = player1_details(screen)

        if game_screen == Screen.PLAYERS2:
            game_screen = players2_details(screen)

        if game_screen == Screen.PLAYGAME:

            Start_Time = datetime.now().strftime("%H:%M:%S")
            
            game_screen = start_game(screen, game)

        if game_screen == Screen.PAUSE:
            game_screen = pause_game(screen)
            
        if game_screen == Screen.ENDGAME:

            Date = datetime.now().strftime("%Y-%m-%d")
            
            End_Time = datetime.now().strftime("%H:%M:%S")
            
            Winner = game.getWinnerName()
            Loser = game.getLoserName()
            Winner_Score, Loser_Score = game.getFinalScores()
            
            saveGameInstance(Date, Start_Time, End_Time, Winner, Winner_Score, Loser, Loser_Score)

            game_screen = launch_endgame(screen)

        if game_screen == Screen.ABOUT:
            game_screen = launch_about(screen)

        if game_screen == Screen.QUIT:
            db_con.close()
            pygame.quit()
            return

def start_menu(screen):
    new_screen=main_menu.show_menu()

    game.gameReset()

    if new_screen == screens.main_menu.CB_QUIT:
        return Screen.QUIT
    if new_screen == screens.main_menu.CB_1PLAYER:
        return Screen.PLAYER1
    if new_screen == screens.main_menu.CB_2PLAYERS:
        return Screen.PLAYERS2
    if new_screen == screens.main_menu.CB_ABOUT:
        return Screen.ABOUT

    return Screen.QUIT

def player1_details(screen):
    new_screen=player_names.Player1_Name()

    if new_screen == screens.playernames.CB_PLAY_AI:
        game.setPlayer1Name(player_names.getPlayer1Name())
        game.setPlayer2Name(player_names.getPlayer2Name())
        game.enableAi()
        game.setMovables(r.game.BALL_HEIGHT, (r.game.PADDLE_WIDTH, r.game.PADDLE_HEIGHT), player_names.getColor1(), player_names.getColor2())
        return Screen.PLAYGAME
    if new_screen == screens.playernames.CB_RETURN:
        return Screen.MENU

    return Screen.QUIT

def players2_details(screen):
    new_screen=player_names.Players2_Names()

    if new_screen == screens.playernames.CB_PLAY:
        game.setPlayer1Name(player_names.getPlayer1Name())
        game.setPlayer2Name(player_names.getPlayer2Name())
        game.setMovables(r.game.BALL_HEIGHT, (r.game.PADDLE_WIDTH, r.game.PADDLE_HEIGHT), player_names.getColor1(), player_names.getColor2())
        game.disableAi()
        return Screen.PLAYGAME
    if new_screen == screens.playernames.CB_RETURN:
        return Screen.MENU

    return Screen.QUIT

def start_game(screen,game):
    new_screen = game.play()

    if new_screen == screens.game.CB_PAUSE:
        return Screen.PAUSE
    elif new_screen == screens.game.CB_ENDGAME:
        return Screen.ENDGAME
    elif new_screen == screens.game.CB_RETURN:
        return Screen.MENU
    elif new_screen == screens.game.CB_QUIT:
        return Screen.QUIT
    
    return Screen.MENU

def pause_game(screen):
    global game,pause_screen

    pause_screen.setScores(game.getScores())
    new_screen = pause_screen.pause_game()

    if new_screen == screens.pause.CB_QUIT:
        return Screen.QUIT
    if new_screen == screens.pause.CB_PLAY:
        return Screen.PLAYGAME
    if new_screen == screens.game.CB_RETURN:
        return Screen.MENU

    return Screen.MENU

def launch_endgame(screen):
    global endgame_screen,game

    endgame_screen.setWinnerName(game.getWinnerName())
    endgame_screen.setWinnerColor(game.getWinnerColor())

    new_screen=endgame_screen.showEndScreen()

    if new_screen==screens.endgame.CB_PLAY:
        return Screen.PLAYGAME
    if new_screen==screens.endgame.CB_RETURN:
        return Screen.MENU
    if new_screen == screens.pause.CB_QUIT:
        return Screen.QUIT

    return Screen.MENU

def launch_about(screen):
    global about_screen

    new_screen=about_screen.showAbout()

    if new_screen==screens.about.CB_RETURN:
        return Screen.MENU
    if new_screen==screens.about.CB_QUIT:
        return Screen.QUIT

    return Screen.MENU

def initiateConnection():
    global db_con
    try:
        db_con=scon.connect(host=r.db_info.HostName, user=r.db_info.UserName, passwd=r.db_info.Password, database=r.db_info.DatabaseName)
    except scon.errors.ProgrammingError:
        print("No database found, initiating it now")
        createDatabase()
    finally:
        db_con=scon.connect(host=r.db_info.HostName, user=r.db_info.UserName, passwd=r.db_info.Password, database=r.db_info.DatabaseName)
        
def createDatabase():
    db=scon.connect(host=r.db_info.HostName, user=r.db_info.UserName, passwd=r.db_info.Password)
    db.cursor().execute(r.db_info.Q_CREATE_PONGDATA)

    db=scon.connect(host=r.db_info.HostName, user=r.db_info.UserName, passwd=r.db_info.Password, database=r.db_info.DatabaseName)
    db.cursor().execute(r.db_info.Q_CREATE_GAMESTATS)

    db.close()

def saveGameInstance(date, startTime, endTime, winnerName, winnerScore, loserName, loserScore):
    global db_con
    query=r.db_info.Q_ADD_GAME_DATA.format(date, startTime, endTime, winnerName, winnerScore, loserName, loserScore)

    db_con.cursor().execute(query)
    db_con.commit()

class Screen(Enum):
    QUIT=-1
    MENU=0
    PLAYGAME=1
    PAUSE=2
    ENDGAME=3
    PLAYER1=4
    PLAYERS2=5
    ABOUT=6

if __name__=="__main__":
    main()
