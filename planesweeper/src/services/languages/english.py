from primitives.interfaces import LanguageResource


class English(LanguageResource):
    _resources = {
        "test": "en_test",
        "window_title": "Planesweeper",
        "current_best_times": "Current best times",
        "current_high_scores": "Current high scores",
        "points_by": "{0} points by {1}",
        "game_won": "Congratulations, you won the game!",
        "game_lost": "Better luck next time!",
        "challenge_level_cleared": "Great, you cleared the level! " +\
            "Next, try one larger - can you make it without hitting any planes?",
        "challenge_try_again": "Dang, you hit the plane!",
        "challenge_point_lost": "You lost one point of score, but keep trying to solve it!",
        "challenge_keep_trying":
            "Keep trying to solve it!",
        "challenge_level_downgrade":
            "Too many hits drops you to a previous level, but keep trying to solve it!",
        "enter_initials": "Please enter your initials for high-score board",
        "start_single_game": "Click here to start new single game (Alt+S or Alt+1-6 for level)",
        "start_challenge_game": "Click here to start new challenge game (Alt+C)",
        "status_radar_contacts": "Radar contacts: {0} / {1}",
        "status_playtime": "Time: {0}",
        "status_score": "Current score: {0}",
        "status_new_game":
            "Press Alt+S or Alt+[1-6] to start a new single game, Alt+C for challenge"
    }
