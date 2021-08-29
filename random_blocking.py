from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import shelve, time, random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys 

class Booking:
    def __init__(self):
        self._url_ = 'https://web.bet9ja.com/Sport/Default.aspx'
        self.browser = None
        self.all_available_games = []
        self.stake = 0
        self.globalLoop = True
        self.gamePlayCount = 0
        self.cancelPopUp = False
        # open self.db games_to_watch
        self.games_already_played = []
        self.temp_game_cache = []
        # self.game_cache_title = []
        self.perm_game_cache_market = []
        
        self.db = shelve.open("db")
        self.start()

        
    def start(self):
        # self.browser = webdriver.Chrome()
        options = webdriver.ChromeOptions() 
        self.ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.browser = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')
        self.initiate()


    def initiate(self): 
        choice = self.ask_for_input("1. Do you want to start the Random booking \n2. Do you want to activate autobet \n3. input maximum autobet stake \n4. Do you want to play all games except those that have the selected markets \n5. view all saved games \n6. clear all saved games \n7. See all games the bot should watch out for \n8. Add the market the bot should watch out for e.g 1, 1X\n9. clear all market the bot should watch out for\n10. Select whether you want strict matching or not e.g in yes 1 will only be valid for over 1 and and over1.5.\n11. Max odd each game should have on a betslip e.g 1.80\n12. Set today's booking code\n13. Reset ur bet9ja username \n14. Reset ur bet9ja password \n15. input minimum autobet stake\n16. input the minimum games to select\n17. Set the maximum total odds the bot can play\n18. Set the minimum total odds the bot can play\n", 18)
        if choice == 1:
            self.booking_code = self.db.get("latest_booking")

            if not self.db.get("autobet"):
                self.autobet()
            else:
                self.autoBet = self.db.get("autobet")

            # if self.autoBet == 1:
            # set all
            if not self.db.get("maximumStake"):
                self.setMaximumStake()
            else:
                self.maximumStake = self.db.get("maximumStake")
            
            
            if not self.db.get("minimumStake"):
                self.setMinimumStake()
            else:
                self.minimumStake = self.db.get("minimumStake")

            if not self.db.get("TotalOdds"):
                self.setTotalOdds()
            else:
                self.TotalOdds = self.db.get("TotalOdds")


            if not self.db.get("minimumGames"):
                self.setMinimumGames()
            else:
                self.minimumGames = self.db.get("minimumGames")

            if not self.db.get("MinimumOdds"):
                self.setMinimumOdds()
            else:
                self.MinimumOdds = self.db.get("MinimumOdds")
                    
            if not self.db.get("watch_type"):
                self.watch_type()
            else:
                self.watchType = self.db.get("watch_type")

            
            if not self.db.get("save_games"):
                self.db["save_games"] = []
                # print(self.db.get("save_games"))
            
            
            if not self.db.get("strict_matching"):
                self.strict_matching()
            else:
                self.strict = self.db.get("strict_matching")
            
            if not self.db.get("max_odds"):
                self.max_odds()
            else:
                self.maxOdds = self.db.get("max_odds")
            
            if not self.db.get("games_to_watch"):
                self.add_market_to_watch()
            else:
                self.gamesMarket = self.db.get("games_to_watch")

            if self.db.get("latest_booking"):
                booking_time = self.db.get("latest_booking_time")
                
                if not booking_time:
                    booking_time = 0

                if time.time() > int(booking_time + 86400):
                    booking_code = input("WHAT is the current booking code for today?\n")
                    self.booking_code = booking_code
                    self.db['latest_booking'] = booking_code
                    self.db['latest_booking_time'] = time.time()
            else:
                booking_code = input("WHAT is the current booking code for today?\n")
                self.booking_code = booking_code
                self.db['latest_booking'] = booking_code
                self.db['latest_booking_time'] = time.time()

            self.how_many_games_to_play = int(input("How many game do you want to play today?\n"))
            # self.stake = input("Enter bet stake?\n")
            
            self.browser.get(self._url_)

            if self.autoBet == 1:
                self.login()

            while self.globalLoop:
                try:
                    balance = WebDriverWait(self.browser, 20, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "hl_w_cLogin_lblSaldo"))).text
                    acc_bal = int(balance.split(".")[0].replace(",", ""))
                    if acc_bal < int(self.minimumStake):
                        print("You have Exhausted your account balance --> ", acc_bal)
                        break
                except Exception as exc:
                    pass
                rand_game = self.randomly_generate_code()
                self.book(rand_game)

        elif choice == 2:
            self.autobet()
        elif choice == 3:
            self.setMaximumStake()
        elif choice == 4:
            self.watch_type()
        elif choice == 5:
            self.view_all_games()
        elif choice == 6:
            self.clear_all_games()
        elif choice == 7:
            self.view_all_games_to_watch()     
        elif choice == 8:
            self.add_market_to_watch()
        elif choice == 9:
            self.clear_all_games_to_watch()
        elif choice == 10:
            self.strict_matching()
        elif choice == 11:
            self.max_odds()
        elif choice == 12:
            self.setBooking()    
        elif choice == 13:
            self.setUsername(True)    
        elif choice == 14:
            self.setPassword(True)            
        
        elif choice == 15:
            self.setMinimumStake()

        elif choice == 16:
            self.setMinimumGames()
            
        elif choice == 17:
            self.setTotalOdds()
        elif choice == 18:
            self.setMinimumOdds()        

    def setMaximumStake(self):
        maximumStake = input("Set your maximum autobetting bot stake\n")
        self.maximumStake = maximumStake
        self.db['maximumStake'] = maximumStake
        self.initiate()

    def setMinimumStake(self):
        minimumStake = input("Set your minimum autobetting bot stake\n")
        self.minimumStake = minimumStake
        self.db['minimumStake'] = minimumStake
        self.initiate()
    
    def setMinimumGames(self):
        minimumGames = int(input("Set your minimum autobetting bot Games to play\n"))
        self.minimumGames = minimumGames
        self.db['minimumGames'] = minimumGames
        self.initiate()

    def setTotalOdds(self):
        TotalOdds = float(input("Set the maximum total odds the bot can play\n"))
        self.TotalOdds = TotalOdds
        self.db['TotalOdds'] = TotalOdds
        self.initiate()

    
    def setMinimumOdds(self):
        MinimumOdds = float(input("Set the minimum total odds the bot can play\n"))
        self.MinimumOdds = MinimumOdds
        self.db['MinimumOdds'] = MinimumOdds
        self.initiate()
        
    def setBooking(self):
        booking_code = input("WHAT is the current booking code for today?\n")
        self.booking_code = booking_code
        self.db['latest_booking'] = booking_code
        self.db['latest_booking_time'] = time.time()
        self.initiate()

    def book(self, rand_game):        
        try:
            if not self.cancelPopUp:
                popup = WebDriverWait(self.browser, 50, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "novasdk-inbox-app-widget__close")))
                if popup:
                    popup[0].click()

        except Exception as exc:
            print(exc)
            pass
        try:
            if self.autoBet == 1:
                _load_input = WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID,"hl_w_PC_cCoupon_txtPrenotatore")))
                _load_input.send_keys(Keys.CONTROL + 'a')
                _load_input.send_keys(rand_game)
                
                _load_btn = WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID,"hl_w_PC_cCoupon_lnkLoadPrenotazione")))
                _load_btn.click()
                self.cancelPopUp = True
            else:
                _load_input = WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID,"h_w_PC_cCoupon_txtPrenotatore")))
                _load_input.send_keys(Keys.CONTROL + 'a')
                _load_input.send_keys(rand_game)
                
                _load_btn = WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID,"h_w_PC_cCoupon_lnkLoadPrenotazione")))
                _load_btn.click()
                self.cancelPopUp = True
        except Exception as exc:
            pass

        _gameB = []
        try: 
            _gameB = WebDriverWait(self.browser, 7, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_all_elements_located((By.XPATH, "//div[@class='CItems']/div")))#self.browser.find_elements_by_xpath("//div[@class='CItems']/div")
            # print(_gameB, len(_gameB))
        except Exception as exc:
            pass
            # print(exc)
        if rand_game not in self.games_already_played:
            if len(_gameB) > self.minimumGames:
                analysis_result = self.analyse_games(rand_game)
                time.sleep(4)
                if analysis_result:
                    if self.autoBet == 1:              
                        try:
                            _Stake = WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID,"hl_w_PC_cCoupon_txtImporto")))
                            if _Stake:
                                stake = _Stake.get_attribute('value').replace(",", "")
                                if int(stake) >= int(self.maximumStake):
                                    stake = self.maximumStake
                            else:
                                stake = self.minimumStake
                            
                            print("bot is playing this game with this stake --> ", stake)
                            
                            _Stake.send_keys(Keys.CONTROL, 'a')
                            _Stake.clear()
                            _Stake.send_keys(stake)

                            betButton = WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "hl_w_PC_cCoupon_lnkAvanti")))
                            if betButton:
                                # print(betButton, betButton.text, betButton.get_attribute("href"))
                                betButton.click()
                                confirmBetButton = WebDriverWait(self.browser, 20, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "hl_w_PC_cCoupon_lnkConferma")))
                                # print(confirmBetButton)
                                # ac_w_cLogin_lblSaldo
                                if confirmBetButton:
                                    confirmBetButton.click()
                                    self.gamePlayCount += 1
                                    print(f"You have Successfully played {self.gamePlayCount} games out of {self.how_many_games_to_play}")
                                    self.games_already_played.append(rand_game)
                                    # Cache gamess
                                    self.cache_games() 
                                    if self.gamePlayCount >= self.how_many_games_to_play:
                                        self.globalLoop = False
                                        print(f"the bot has finished playing {self.how_many_games_to_play} games")
                                else:
                                    print("bet not played")

                        except Exception as exc:
                            pass    
                    else:
                        # Append Random Booking
                        li = self.db["save_games"]
                        li.append(rand_game)
                        self.db["save_games"] = li
                        
                        # Increment game count
                        self.gamePlayCount += 1
                        
                        print(self.gamePlayCount)
                        
                        print(self.db.get("save_games"))
                        print(f"{rand_game} -- Analysis and meets threshold -- Game Saved")
                        print(f"{self.gamePlayCount} game played out of {self.how_many_games_to_play}")
                        
                        if self.gamePlayCount >= self.how_many_games_to_play:
                            self.globalLoop = False
                            print(f"You have Successfully added {self.gamePlayCount} to your bookings")
                else:
                    print("Analysis failed the booking cos it does not meet requirement")

            else:
                print(f"games is less than {self.minimumGames}, can't be played")
        else:
            print(f"{rand_game} is already played!")
        
        self.temp_game_cache = []
        # chill_time = 1
        # print(f"CHILLING FOR {chill_time} secs")
        try:
            cancelButton = WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "h_w_PC_cCoupon_lnkCancella")))
            if cancelButton:
                cancelButton.click()
                # print("cancelled button clicked!!!")
        except Exception as exc:
            pass
            # print("Cancell butt no")
    
        # time.sleep(chill_time)
    
    def cache_games(self):
        for title, market in self.temp_game_cache:
            self.perm_game_cache_market.append([title, market])
            

    def setUsername(self, reset):
        if not self.db.get("username") or reset:
            name = input("what's ur bet9ja username\n")
            self.db["username"] = name
        else:
            self.username = self.db.get("username")

        if reset:
            self.initiate()
    
    def setPassword(self, reset):
        if not self.db.get("password") or reset:
            name = input("what's ur bet9ja password\n")
            self.db["password"] = name
        else:
            self.password = self.db.get("password")
    
        if reset:
            self.initiate()
            

    def login(self):
        self.setUsername(False) 
        self.setPassword(False) 
        username = WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "h_w_cLogin_ctrlLogin_Username")))
        password =  WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "h_w_cLogin_ctrlLogin_Password")))
        username.send_keys(self.username)
        password.send_keys(self.password)
        button =  WebDriverWait(self.browser, 5, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "h_w_cLogin_ctrlLogin_lnkBtnLogin")))
        button.click()
        
    def view_all_games(self):
        if self.db.get("save_games"):
            games = self.db.get("save_games")
            if self.watchType == 1:
                print("These are the market to watch out exclude from betting when analysing")
            else:
                print("These are the market to watch out for when analysing")
            
            for i in games:
                print(f"{i} is available for play")
            
            if not games:
                print("---EMPTY--- NO GAME TO PLAY, RUN BOT")    
        else:
            print("---EMPTY--- NO GAME TO PLAY, RUN BOT")
        time.sleep(4)
        # self.initiate()

    def clear_all_games(self):
        self.db["save_games"] = []
        print("Bookings are cleared successfully")
        time.sleep(4)
        self.initiate()
    
    def view_all_games_to_watch(self):
        if self.db.get("games_to_watch"):
            games = self.db.get("games_to_watch")
            for i in games:
                print(f"Bot will watch out for this - {i} market")
            
            if not games:
                print("---EMPTY--- NO MARKET TO WATCH, ADD MARKET")
        else:
            print("---EMPTY--- NO MARKET TO WATCH, ADD MARKET")
        time.sleep(4)
        self.initiate()

    def clear_all_games_to_watch(self):
        self.db["games_to_watch"] = []
        print("Market are cleared successfully")
        time.sleep(4)
        self.initiate()

    def add_market_to_watch(self):
        loop = True
        if self.db.get("games_to_watch") != None:
            if not self.db.get("watch_type"):
                self.watch_type()
            else:
                self.watchType = self.db.get("watch_type")

            while loop:
                if self.watchType == 1:
                    market = input("Enter market you want exclude from betting eg. Over(1.5), 1, 1X\n")
                else:
                    market = input("Enter market you want watch eg. Over(1.5), 1, 1X\n")

                li = self.db["games_to_watch"]
                li.append(market)
                self.db["games_to_watch"] = li
                print(self.db["games_to_watch"])
                print("Market saved successfully!!!")
                choice = self.ask_for_input("Do you want to add more \n1. Yes \n2.No\n", 2)
                if choice == 2:
                    loop = False
                    time.sleep(4)
                    self.initiate()
        else:
            self.db["games_to_watch"] = []
            self.add_market_to_watch()

    def strict_matching(self):
        result = self.ask_for_input("Do want to enable strict matching\n1. Yes \n2. No\n", 2)
        self.db["strict_matching"] = result
        print("You have set your strict match successfully")
        time.sleep(4)
        self.initiate()

    # def games_matching(self):
    #     result = self.ask_for_input("Do want to enable strict matching\n1. Yes \n2. No\n", 2)
    #     self.db["strict_matching"] = result
    #     print("You have set your strict match successfully")
    #     time.sleep(4)
    #     self.initiate()

    def autobet(self):
        result = self.ask_for_input("Do you want to activate autobetting?\n1. Yes \n2. No\n", 2)
        self.db["autobet"] = result
        print("You choice have been saved")
        time.sleep(4)
        self.initiate()
    
    def watch_type(self):
        result = self.ask_for_input("Do you want to play all games except those that have the selected markets?\n1. Yes \n2. No\n", 2)
        self.db["watch_type"] = result
        print("You choice have been saved")
        time.sleep(4)
        self.initiate()

    def clear_all_games(self):
        self.db["save_games"] = []
        time.sleep(4)
        self.initiate()

    def max_odds(self):
        odds = float(input("Enter your maximum odds you want the game to pick, e.g 2.1, Set something outrageous if you don't need this feature\n"))
        self.db["max_odds"] = odds
        print(f"Your max odds as been successfully set to {odds}")
        time.sleep(4)
        self.initiate()
        
    def randomly_generate_code(self):
        all_possible_char = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] 
        how_many_replace = random.randint(1, 3)
        new_booking = []
        for i in self.booking_code:
            new_booking.append(i)

        for i in range(how_many_replace):
            # starts from three to account for staticness
            replace_index = random.randrange(4, len(new_booking))
            char_index = random.randrange(1, len(all_possible_char))
            new_booking[replace_index] = all_possible_char[char_index]
        
        new_booking = "".join(new_booking)

        return new_booking


    def analyse_games(self, rand_game):
        try:
            if self.autobet == 1:
                total_odds = WebDriverWait(self.browser, 10, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "hl_w_PC_cCoupon_lblQuotaTotale"))).text
            else:
                total_odds = WebDriverWait(self.browser, 10, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "h_w_PC_cCoupon_lblQuotaTotale"))).text
        
        except Exception as exc:
            total_odds = 0

        if total_odds:
            total_odds = total_odds.split(".")[1].replace(",", "")

        if float(total_odds) > self.TotalOdds:
            print(f"the odds is Too much, playing another, The total odds is {total_odds} and the maximum the bot can play is {self.TotalOdds}")
        elif float(total_odds) < self.MinimumOdds:
            print(f"the odds is Too Small, playing another, The total odds is {total_odds} and the minimum the bot can play is {self.MinimumOdds}")
        else:    
            try:
                _game = WebDriverWait(self.browser, 10, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"CItems")))
                all_game = WebDriverWait(_game, 10, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME,"div")))
            except Exception as exc:
                all_game = []
                return False

            print("analysing..")
            for i, game in enumerate(all_game):
                try:
                    game_type = self.browser.find_elements_by_class_name("CqSegno")[i].text
                    gameType = self.browser.find_elements_by_class_name("CSegno")[i].get_attribute("title")
                    odds = float(self.browser.find_elements_by_class_name("valQuota_1")[i].text)
                    title = self.browser.find_elements_by_class_name("CSubEv")[i].find_elements_by_tag_name("span")[0].text
                    # print(title, game_type, "analyse", odds, gameType, self.maxOdds)
                    isPresent = False

                    for myTitle, market in self.perm_game_cache_market:
                        if myTitle == title and market == gameType:
                            print(f'{title} --> {gameType} has already been played so this game won\'t be played')
                            return False    

                    # if title in self.game_cache_title and gameType in self.game_cache_market:
                    #     titleIndex = self.game_cache_title.index(title)
                    #     marketIndex = self.game_cache_market.index(gameType)
                    #     if titleIndex == marketIndex:
                    
                    self.temp_game_cache.append([title, gameType])
                    
                    if self.watchType == 1:
                        if self.strict == 1:
                            # print(gameType, "is this in", self.gamesMarket)
                            if gameType not in self.gamesMarket:
                                isPresent = True 
                        else:
                            # print(gameType, self.gamesMarket)
                            for each_market in self.gamesMarket:
                                # print(each_market, "in", gameType)
                                if each_market not in gameType:
                                    # print("yes", gameType, each_market)
                                    isPresent = True
                                    break
                    else:
                        if self.strict == 1:
                            # print(gameType, "is this in", self.gamesMarket)
                            if gameType in self.gamesMarket:
                                isPresent = True 
                        else:
                            # print(gameType, self.gamesMarket)
                            for each_market in self.gamesMarket:
                                # print(each_market, "in", gameType)
                                if each_market in gameType:
                                    # print("yes", gameType, each_market)
                                    isPresent = True
                                    break
                    
                    # If gameType is not in the selected market return nothing
                    if not isPresent:            
                        return False

                    if "Z." in title:
                        print("Zoom Game spotted, discarding game...")
                        return False

                    elif "Srl" in title or "SRL" in title:
                        print("SRL Game spotted, discarding game...")
                        return False


                    if odds > float(self.maxOdds):
                        print(f"The game can't be played because the of bigger odds constraint which is set to {self.maxOdds}")
                        return False
                except Exception as exc:
                    # print(exc)
                    break
                
            
            time.sleep(1)
            return True

    def ask_for_input(self, question, max_choice):
        choice = ""
        while choice == "":
            num_input = input(question)
            if num_input.isdecimal():
                choice = int(num_input)
                if choice <= max_choice:
                    return choice
                
                print('++++++++++++++++++++\nyour choice is out of bound\n++++++++++++++++++++')
                choice = ""
            print('++++++++++++++++++++\ninvalid choice\n++++++++++++++++++++')

Booking()