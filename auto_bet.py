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
        self._url_ = 'https://web.bet9ja.com/Sport/Odds?EventID=949665,1435391'#'https://web.bet9ja.com/Sport/GroupsExt.aspx?IDSport=590&Antepost=0'
        self.browser = None
        self.all_available_games = []
        self.start()
        self.stake = 0
        
    def start(self):
        # self.browser = webdriver.Chrome()
        self.initiate()
        options = webdriver.ChromeOptions() 
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        self.browser = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')
        self.browser.maximize_window()
        self.browser.get(self._url_)
        self.book()

    def initiate(self):
        pass
        # db = shelve.open("db")
        # if not db.get("latest_booking"):
        #     booking_time = db.get("latest_booking_time")
        #     if not booking_time:
        #         booking_time = 0
        #     print(time.time(), booking_time + 86400 )
        #     if time.time() >  booking_time + 86400:
        #         booking_code = input("WHAT is the current boking code for today?\n")
        #         self.booking_code = booking_code
        #         db['latest_booking'] = booking_code
        #         db['latest_booking_time'] = time.time()
        # else:
        #     booking_code = input("WHAT is the current boking code for today?\n")
        #     self.booking_code = booking_code
        #     db['latest_booking'] = booking_code
        #     db['latest_booking_time'] = time.time()

        # how_many_games_to_play = int(input("How many game do you want to play today?\n"))
        # self.stake = input("Enter bet stake?\n")
        # # 3GF39LK
        # for i in range(how_many_games_to_play):
        #     rand_game = self.randomly_generate_code()
        #     self.book(rand_game)

    def book(self):
        # try:
        # MAX_EVENT = 2
        # all_check_box = WebDriverWait(self.browser, 50, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,"input[type=checkbox]")))[:MAX_EVENT]
        # for check_box in all_check_box:
        #     try:
        #         check_box.click()
        #     except Exception as exc:
        #         print("Unclickable")

        # View_btn = self.browser.find_element_by_link_text("View")
        # View_btn.click()

        # try:
        #     all_games = WebDriverWait(self.browser, 50, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"Event ng-binding")))
        #     for game in all_games:
        #         print(game.text)
        
        # except Exception as exc:
        #     print(f"Error Wait ERROR {exc}")
        
        # date = self.browser.find_element_by_class_name("sepData ng-binding")
        # title = self.browser.find_element_by_class_name("Event ng-binding")
        # # stats = self.browser.find_element_by_class_name("stats innprojekt")
        # print(date.text, title.text)
                
        # self.browser.implicitly_wait(5)
        # games = self.browser.find_elements_by_class_name("item ng-scope")
        # print(games)

        script = """
        games = document.getElementsByClassName('item ng-scope')
        for(let i = 0; i < games.length; i++){
            date = games[i].getElementsByClassName("sepData ng-binding")[0]
            title = games[i].getElementsByClassName("Event ng-binding")[0]
            console.log(date.innerText, title.innerText)
            // odd  r1 c1 g1 
            let one = games[i].getElementsByClassName("odd  r1 c1 g1 ")[0]
            let [oddType1, odds1] = one.getElementsByTagName('div')
            console.log(oddType1.innerText, odds1.innerText)
            
            let draw = games[i].getElementsByClassName("odd  r1 c2 g1 ")[0]
            let [oddTypex, oddsx] = draw.getElementsByTagName('div')
            console.log(oddTypex.innerText, oddsx.innerText)
            
            let two = games[i].getElementsByClassName("odd  r1 c3 g1 ")[0]
            let [oddType2, odds2] = two.getElementsByTagName('div')
            console.log(oddType2.innerText, odds2.innerText)

            
            let onex = games[i].getElementsByClassName("odd  r1 c4 g1 ")[0]
            let [oddType1x, odds1x] = onex.getElementsByTagName('div')
            console.log(oddType1x.innerText, odds1x.innerText)

            
            let onetwo = games[i].getElementsByClassName("odd  r1 c5 g1 ")[0]
            let [oddType12, odds12] = onetwo.getElementsByTagName('div')
            console.log(oddType12.innerText, odds12.innerText)

            
            let twox = games[i].getElementsByClassName("odd  r1 c6 g1 ")[0]
            let [oddType2x, odds2x] = twox.getElementsByTagName('div')
            console.log(oddType2x.innerText, odds2x.innerText)

            
            let over2 = games[i].getElementsByClassName("odd  r1 c7 g1 ")[0]
            let [oddTypeov2, oddsov2] = over2.getElementsByTagName('div')
            console.log(oddTypeov2.innerText, oddsov2.innerText)

            
            let under2 = games[i].getElementsByClassName("odd  r1 c8 g1 ")[0]
            let [oddTypeun2, oddsun2] = under2.getElementsByTagName('div')
            console.log(oddTypeun2.innerText, oddsun2.innerText)

            // stats = games[i].getElementsByClassName("stats innprojekt")[0].click()
            
            onetwo.click()
            
        }
        // alert(arguments[0])   

        //let booking = document.getElementById('bookHead')
        //let booking_code = null
        //do{
//            booking_code = booking.getElementsByClassName('number')[0].innerText
  //          console.log(divBody.getElementsByClassName('number')[0].innerText)
    //    }
      //  while(!booking_code)

    
        let waitForElements = (id_name, method_name) =>{
        let getElements = setInterval(
            () =>{
                let element = document.getElementById(id_name)
                console.log(element)
                if(element){
                    method_name(element)
                    clearInterval(getElements)
                    return element
                }
            }, 
            2000
            )
        }


        let play_booking = (stake_elem) =>{
            try{
                document.getElementById('s_w_PC_cCoupon_txtImporto').value = arguments[0]
                document.getElementById('s_w_PC_cCoupon_lnkAvanti').click()
                //setTimeout(()=>{
            
                    // booking_code = document.getElementById("bookHead").getElementsByClassName('number')[0].innerText
                    // console.log(booking_code, booking)
                  //  alert("ran")        
                // }, 5000)
            }
            catch(e){
                console.log(e)
            }
        }

        let get_booking = (booking) => {
            booking_code = booking.contentWindow.document.getElementsByClassName('number')[0].innerText
            console.log(booking_code, booking)
            return booking_code 
        }

        waitForElements('s_w_PC_cCoupon_txtImporto', play_booking)
        return waitForElements('iframePrenotatoreSco', get_booking)


        // booking_code = null
        
        // return booking_code
        // return games
        """
        games = self.browser.execute_script(script, "100")
        print(games, "t")

        # self.browser.find_element_by_id('s_w_PC_cCoupon_txtImporto').send_keys("100")
        # self.browser.find_element_by_id('s_w_PC_cCoupon_lnkAvanti').click()
            

        # script2 = """
        #     alert(arguments[0])            
        #     document.getElementById('s_w_PC_cCoupon_txtImporto').value = arguments[0]
        #     document.getElementById('s_w_PC_cCoupon_lnkAvanti').click()
            

        #     let booking = document.getElementById('bookHead')
        #     let booking_code = null
        #     do{
        #         booking_code = divBody.getElementsByClassName('number')[0].innerText
        #         console.log(divBody.getElementsByClassName('number')[0].innerText)
        #     }
        #     while(!divBody)
        #     return booking_code
        # """

        # booking_code = self.browser.execute_script(script2, "100")
        # print(booking_code)
        # divBody
        # for game in games:
        #     date = game.find_element_by_class_name("sepData ng-binding")
        #     title = game.find_element_by_class_name("Event ng-binding")
        #     print(date, title)
        #     # stats = game.find_element_by_class_name("stats innprojekt")
        #     # print("sleeping for three secs")
        #     time.sleep(3)
            
        # #     stats.click()
        # #     stats = game.find_element_by_class_name("stats innprojekt")
        print("peace")
        time.sleep(3600)
        # s_w_PC_cCoupon_txtImporto
        # s_w_PC_cCoupon_lnkAvanti
        # while not games:
        #     # print(games)
        #     # games = self.browser.find_elements_by_class_name("item ng-scope")
        
        #     for game in games:
        #         date = game.find_element_by_class_name("sepData ng-binding")
        #         title = game.find_element_by_class_name("Event ng-binding")
        #         stats = game.find_element_by_class_name("stats innprojekt")
        #         print(date.text, title.text)
        #         print("sleeping for three secs")
        #         time.sleep(3)
                
        #         stats.click()
        #         stats = game.find_element_by_class_name("stats innprojekt")
            
        #     time.sleep(3)
        # else:      
        #     for game in games:
        #         date = game.find_element_by_class_name("sepData ng-binding")
        #         title = game.find_element_by_class_name("Event ng-binding")
        #         stats = game.find_element_by_class_name("stats innprojekt")
        #         print(date.text, title.text)
        #         print("sleeping for three secs")
        #         time.sleep(3)
                
        #         stats.click()
        #         stats = game.find_element_by_class_name("stats innprojekt")
            
        #     time.sleep(3)
            
    #         _load_input.send_keys(Keys.CONTROL + 'a')
    #         _load_input.send_keys(rand_game)
            
    #         _load_btn = WebDriverWait(self.browser, 50, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID,"h_w_PC_cCoupon_lnkLoadPrenotazione")))
    #         _load_btn.click()
            
    #         info = WebDriverWait(self.browser, 50, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID,"h_w_PC_cCoupon_mexPrenotazione")))
    #         print(info.text[:29])
    #         if info.text[:29] == f"Booking number {rand_game} found.":
    #             print("BOOKING FOUND\n")
    #             # self.all_available_games.append(rand_game)
    #             # print(self.all_available_games)
    #             self.analyse_games()
    #             try:
    #                 _Stake = WebDriverWait(self.browser, 50, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID,"h_w_PC_cCoupon_txtImporto")))
    #                 _Stake.send_keys(Keys.CONTROL + 'a')
    #                 _Stake.send_keys(self.stake)
    #             except:
    #                 print("BOOKING NOT FOUND")
    #         else:
    #             print("BOOKING NOT FOUND\n")
            
    #         chill_time = 3
    #         print(f"CHILLING FOR {chill_time} secs")
    #         time.sleep(chill_time)
    #     except Exception as exc:
    #         print(str(exc), "NETWORK ISSUES")
    
    # def randomly_generate_code(self):
    #     all_possible_char = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] 
    #     how_many_replace = random.randint(1, 4)
    #     new_booking = []
    #     for i in self.booking_code:
    #         new_booking.append(i)

    #     for i in range(how_many_replace):
    #         # starts from three to account for staticness
    #         replace_index = random.randrange(3, len(new_booking))
    #         char_index = random.randrange(1, len(all_possible_char))
    #         new_booking[replace_index] = all_possible_char[char_index]
        
    #     new_booking = "".join(new_booking)

        # return new_booking


    def analyse_games(self):
        _game = WebDriverWait(self.browser, 50, ignored_exceptions=self.ignored_exceptions).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"CItems")))
        all_game = _game.find_elements_by_tag_name("div")
        for game in all_game:
            game_type = game.find_element_by_class_name("CqSegno").text
            odds = game.find_element_by_class_name("valQuota_1").text
            print(game_type, odds)
        


Booking()
# 3FXJ79T