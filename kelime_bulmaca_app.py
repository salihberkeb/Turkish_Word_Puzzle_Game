import random
import time
import threading
from kelime_bulmaca_menu import Ui_MainWindowMenu
from kelime_bulmaca_oyunForm import Ui_MainWindowGame
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QTimer
import sys
import vlc


instance = vlc.Instance()
player = instance.media_player_new()
# Çalmak istediğiniz medya dosyasının yolu
media = instance.media_new("music/Super Mario Bros. Soundtrack.mp3")
player.set_media(media)
player.play()

class KelimeBulmaca(QtWidgets.QMainWindow):
    def __init__(self,wrong_count,correct_count,wrong_questions):
        super(KelimeBulmaca,self).__init__()
        self.ui_menu=Ui_MainWindowMenu()
        self.wrong_count=wrong_count
        self.wrong_count=correct_count
        self.wrong_questions=wrong_questions
        self.ui_menu.setupUi(self)
        self.ui_menu.btn_startgame.clicked.connect(self.open_second_page)
        self.ui_menu.btn_cikis.clicked.connect(self.close_func)
        self.ui_menu.btn_oynu_verileri.clicked.connect(self.oyun_verileri)
        self.game_page=None

    def update_wrong_count(self, new_count_wrong,new_count_correct,wrong_questions):
        self.wrong_count = new_count_wrong
        self.correct_count=new_count_correct
        self.wrong_questions=wrong_questions

    def open_second_page(self):
        self.hide()
        if self.game_page is None:
            self.game_page=GamePage()
        self.game_page.show()

    def oyun_verileri(self):
        # print(self.wrong_questions)
        try:
            self.ui_menu.lbl_correct_count.setText(f"  {self.correct_count}")
            self.ui_menu.lbl_wrong_count_2.setText(f"  {self.wrong_count}")
        except AttributeError:
            self.ui_menu.lbl_correct_count.setText("_")
            self.ui_menu.lbl_wrong_count_2.setText(f"_")


    def close_func(self):
        quitmessage=QMessageBox.question(self,"Çıkış","Çıkmak istedğine emin misiniz ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if quitmessage==QMessageBox.Yes:
            quit()


class GamePage(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui_game=Ui_MainWindowGame()
        self.ui_game.setupUi(self)
        correct_count=0
        wrong_count=0
        self.correct_count=0
        self.wronq_count=0
        self.oyunucalistir()

    def oyunucalistir(self):
        count=0
        bas_harfer=[]
        wrong_questions=[]
        process=threading.Thread(target=self.timer,args=(10,))
        process.daemon=True
        process.start()
        self.process=process
        self.startgame(count,self.correct_count,self.wronq_count,wrong_questions,bas_harfer)

    def startgame(self,count,correct_count,wrong_count,wrong_questions,bas_harfler):
        self.timer_end()
        file=self.openFile(count)
        self.file=file
        sorular_cevaplar,sorular,cevaplar=self.getwords(self.file)

        random_choice=random.randint(0,len(sorular)-1)
        self.choice=random_choice
        self.ui_game.lbl_soru.setText(sorular[random_choice])
        self.ui_game.txt_cevap.setFocus()
        QCoreApplication.processEvents()
        self.ui_game.btn_cikis.clicked.connect(self.stop_and_switcth_to_page1)
        self.ui_game.txt_cevap.returnPressed.connect(lambda : self.check_answer(self.choice,sorular_cevaplar,cevaplar,count,correct_count,wrong_count,wrong_questions,bas_harfler))

    def stop_and_switcth_to_page1(self):
        self.hide()
        try:
            page1.ui_menu.btn_startgame.clicked.disconnect()
        except TypeError:
            pass 
        if self.correct_count==None:
            self.correct_count=0
        if self.wronq_count== None:
            self.wronq_count=0
        try:
            page1.update_wrong_count(self.wronq_count,self.correct_count,self.wrong_questions)
        except AttributeError:
            self.wrong_questions=[]
        page1.show()


    def check_answer(self, choice,sorular_cevaplar ,cevaplar,count,correct_count,wrong_count,wrong_questions,bas_harfler):

        buyuk_alfabe=["A", "B", "C", "D", "E", "F", "G", "H", "I", "İ", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "Y", "Z"]
        user_answer = self.ui_game.txt_cevap.text()
        self.ui_game.txt_cevap.clear()


        if user_answer.lower() == cevaplar[choice]:

            self.ui_game.lbl_dogru_yada_yanlis.setText("DOĞRU")
            count+=1
            correct_count+=1
            self.correct_count=correct_count

        elif user_answer.lower() == "":
            self.ui_game.lbl_dogru_yada_yanlis.setText("PAS")
            wrong_questions.append(sorular_cevaplar[choice])
            if count<24:
                bas_harfler.append(buyuk_alfabe[count])

            count+=1        
        else :
            self.ui_game.lbl_dogru_yada_yanlis.setText("YANLIŞ")
            wrong_count+=1
            self.wronq_count=wrong_count
            count+=1

        if correct_count==len(buyuk_alfabe):#Bütün Sorular bittikten sonra başlar.(Fonksiyon yapabilirdim gerek duymadım)

            self.ui_game.lbl_durum_bilgilendirmesi.setText("Bütün Sorular Doğru")
            self.correct_count=correct_count

            return self.stop_and_switcth_to_page1()

        elif wrong_count+correct_count==len(buyuk_alfabe):#Bütün Sorular yanlış ise

            self.ui_game.lbl_durum_bilgilendirmesi.setText("Bütün Sorular Bitti")
            self.wronq_count=wrong_count
            self.stop_btn_game()
            return self.stop_and_switcth_to_page1()    
        
        elif count==(len(buyuk_alfabe)):
            print("wrong fonksiyonu çalıştı\n")
            return self.start_wrongquestion(wrong_questions,correct_count,wrong_count,0,bas_harfler)



        self.wrong_questions=wrong_questions
        self.on_return_pressed(user_answer)
        self.startgame(count,correct_count,wrong_count,wrong_questions,bas_harfler)

    def start_wrongquestion(self,wrong_questions,correct_count,wrong_count,count,bas_harfler):
        yanlis_sorular=[]        
        self.timer_end()


        if count==len(wrong_questions):
            count=0
        try:
            if count<24:
                self.ui_game.lbl_bas_harf.setText(f"{bas_harfler[count]}")
        except IndexError:
                self.ui_game.lbl_bas_harf.setText(f"-")

        self.ui_game.txt_cevap.returnPressed.disconnect()
        for elemanlar in wrong_questions:
            wrong_questions_new=elemanlar
            yanlis_soru=wrong_questions_new[0].strip()
            yanlis_sorular.append(yanlis_soru)

        if count!=len(yanlis_sorular):
            self.ui_game.lbl_soru.setText(yanlis_sorular[count])
            

        self.ui_game.txt_cevap.returnPressed.connect(lambda : self.wrongQuestions(wrong_questions,correct_count,wrong_count,count,bas_harfler))        

    def wrongQuestions(self,wrong_questions,correct_count,wrong_count,count,bas_harfler): #Eğer kullanıcı ilk etapta yanlış soru işaretlediyse çalışır.

        yanlis_sorular=[]
        yanlis_sorularin_cevaplar=[]
        wrong_questions_new=[]

        for elemanlar in wrong_questions:
            wrong_questions_new=elemanlar
            yanlis_soru=wrong_questions_new[0].strip()
            yanlis_cevap=wrong_questions_new[1].strip().lower()
            yanlis_sorular.append(yanlis_soru)
            yanlis_sorularin_cevaplar.append(yanlis_cevap)

        user_answer=self.ui_game.txt_cevap.text()
        if user_answer==yanlis_sorularin_cevaplar[count]: #Cevap doğruysa çalışır.
            self.ui_game.lbl_dogru_yada_yanlis.setText("DOĞRU")
            correct_count+=1
            self.correct_count=correct_count
            wrong_questions.pop(count)
            bas_harfler.pop(count)

        elif user_answer=="":
            self.ui_game.lbl_dogru_yada_yanlis.setText("PAS")
            count+=1
        else: #Yanlış yaptıysa çalışır.
            wrong_questions.pop(count)
            bas_harfler.pop(count)
            self.ui_game.lbl_dogru_yada_yanlis.setText("YANLIŞ")
            wrong_count+=1
            self.wronq_count=wrong_count


        if correct_count==24: #Bütün soruların doğru bilinmesi halinde çalışır.

            self.ui_game.lbl_durum_bilgilendirmesi.setText("Bütün Sorular Doğru")

            self.stop_and_switcth_to_page1()
        
        if wrong_questions==[]:
            self.ui_game.lbl_durum_bilgilendirmesi.setText("Bütün Sorular Bitti")
            self.stop_and_switcth_to_page1()
            self.stop_btn_game()

        self.ui_game.txt_cevap.clear()
        self.wrong_questions=wrong_questions
        self.start_wrongquestion(wrong_questions,correct_count,wrong_count,count,bas_harfler)


    def openFile(self,count):
        alfabe=["a", "b", "c", "d", "e", "f", "g", "h", "ı", "i", "j","k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "v", "y", "z"]
        gecici=str(alfabe[count])
        try:
            file=open("questions/"+alfabe[count]+".txt","r",encoding="utf-8")
            
            buyuk_harf=gecici.upper()
            self.ui_game.lbl_bas_harf.setText(f"{buyuk_harf}")
        except IndexError:
            print("dosya bulunamadı")

        return file
    
    def getwords(self,file):
        sorular=[]
        cevaplar=[]
        sorular_cevaplar_listesi=[]
        readingfile=file.readlines()
        for elemanlar in readingfile:
            
            soru_cevap=elemanlar.strip().split("-")
            sorular_cevaplar_listesi.append(soru_cevap)
            soru=soru_cevap[0].strip()
            cevap=soru_cevap[1].strip().lower()
            sorular.append(soru)
            cevaplar.append(cevap)
        return sorular_cevaplar_listesi,sorular,cevaplar
    
    def stop_btn_game(self):
        page1.ui_menu.btn_startgame.clicked.disconnect()
    def sleeper(self,param):
        self.timer_pyqt5=QTimer()
        self.timer_pyqt5.timeout.connect(param)
        self.timer_pyqt5.start(4000)

    def on_return_pressed(self,user_input):# Burada kullanıcı girişiyle yapılması gereken işlemleri gerçekleştirin
        self.ui_game.txt_cevap.returnPressed.disconnect()
        print("Kullanıcı girişi:",user_input)  

    def close_func(self):
        quitmessage=QMessageBox.question(self,"Çıkış","Çıkmak istedğine emin misiniz ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if quitmessage==QMessageBox.Yes:
            quit()

    def timer(self,timing):
        start_time=int(time.time())#saniye cinsinden       #gün=24*3600 saniye          saat=3600 saniye          dakika=60 saniye
        while True:

            saniye=int(time.time()) - start_time # saat=int(saniye // 3600)
            dakika=int(saniye//60) # saniye=int(saniye % 60)
            ekrana_yazılacak_saniye=timing-saniye
            time.sleep(1)
            self.ui_game.lbl_durum_bilgilendirmesi.setText(f"{ekrana_yazılacak_saniye}")
            if timing==saniye:
                self.ui_game.lbl_durum_bilgilendirmesi.setText("SÜRE BİTTİ-Enter'a Basınız")
                break

        return saniye

    def timer_end(self):
        if self.ui_game.lbl_durum_bilgilendirmesi.text()=="SÜRE BİTTİ-Enter'a Basınız":
            self.stop_and_switcth_to_page1()

app=QtWidgets.QApplication(sys.argv)
page1=KelimeBulmaca(0,0,[])
page2=GamePage()
page1.show()
sys.exit(app.exec_())