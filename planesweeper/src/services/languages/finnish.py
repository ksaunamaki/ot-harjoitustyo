from primitives.interfaces import LanguageResource


class Finnish(LanguageResource):
    _resources = {
        "test": "fi_test",
        "window_title": "Tutkapinta",
        "current_best_times": "Tämänhetkiset parhaat ajat",
        "current_high_scores": "Tämänhetkiset piste-ennätykset",
        "points_by": "{1} tekemät {0} pistettä",
        "game_won": "Onnittelut, voitit pelin!",
        "game_lost": "Parempaa onnea ensi kerralla!",
        "challenge_level_cleared": "Loistavaa, sait selvitettyä tämän tason! " +\
            "Yritä seuraavaksi yhtä suurempaa - pystytkö siihen osumatta lentokoneisiin?",
        "challenge_try_again": "Hitsi, osuit lentokoneeseen!",
        "challenge_point_lost": "Pisteistäsi vähennetään yksi yksikkö, mutta jatka yrittämistä!",
        "challenge_keep_trying":
            "Jatka yrittämistä!",
        "challenge_level_downgrade":
            "Liian monta osumaa tiputtaa sinut tasoa alemmaksi, mutta jatka yrittämistä!",
        "enter_initials": "Anna nimikirjaimesi ennätystaululle",
        "start_single_game":
            "Paina tästä aloittaaksesi yksittäispelin (Alt+S tai Alt+1-6 taso)",
        "start_challenge_game": "Paina tästä aloittaaksesi haastepelin (Alt+C)",
        "status_radar_contacts": "Tutkakontakteja: {0} / {1}",
        "status_playtime": "Aika: {0}",
        "status_score": "Tämänhetkiset pisteet: {0}",
        "status_new_game": "Paina Alt+S tai Alt+[1-6] uusi yksittäispeli tai Alt+C haastepeli"
    }
