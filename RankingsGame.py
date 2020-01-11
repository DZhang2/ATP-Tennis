from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import requests

page = requests.get("https://www.atptour.com/en/rankings/singles")
soup = BeautifulSoup(page.content, 'html.parser')

age = soup.find_all(class_ = 'age-cell')
rank = soup.find_all(class_ = 'rank-cell')
ptcell = soup.find_all(class_ = 'points-cell')  #narrow down to only pt cells
playercell = soup.find_all(class_ = 'player-cell') #narrow down to player cells
tourncell = soup.find_all(class_ = 'tourn-cell') #narrow down to tourn cells

player_list = []
points_list = []
age_list = []
rank_list = []
tourn_list = []
leverage_list = []      #leverage = points/tourn
n = 50     #n=number of players displayed in data (up to 100)
for i in range(n):      #appends first n values to each list
    age_list.append(age[i].get_text())
    rank_list.append(rank[i].get_text())
    points_list.append(ptcell[i].find('a').get_text())
    player_list.append(playercell[i].find('a').get_text())
    tourn_list.append(int(tourncell[i].find('a').get_text()))

#reformatting to remove escape chars and ,
escapes = ['\n', '\r', '\t']
for i in range(n):
    age_list[i] = int(age_list[i].translate(str.maketrans('','', ''.join(escapes))))
    rank_list[i] = rank_list[i].translate(str.maketrans('','', ''.join(escapes)))
    points_list[i] = int(points_list[i].translate(str.maketrans('','',''.join(','))))
    leverage_list.append(points_list[i]/tourn_list[i])

COUNT = 0
pointsTotal = 0
got = []    #list of already guessed players
def check_player(player):
    res = 'not a player'    
    global COUNT
    global pointsTotal
    double = False
    for i in range(n):
        if player == player_list[i]:
            res = player + " (" + rank_list[i] + ")" + " " + str(points_list[i])
            for g in got:
                if player == g:      
                    double = True
                    res = 'repeat'
            if double == False:
                got.append(player)
                COUNT = COUNT + 1
                pointsTotal = pointsTotal + points_list[i]
            break
    text = QLabel(res)
    VB.addWidget(text)
    res2 = str(COUNT) + " players , " + str(pointsTotal) + " points"
    countLabel.setText(res2)
            
#gui
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("ATP Rankings")
label = QLabel("Top " + str(n) + " Players")
label.setAlignment(Qt.AlignCenter)
VB = QVBoxLayout()
HB = QHBoxLayout()
formLayout = QFormLayout()
line1 = QLineEdit()
formLayout.addRow("Player:", line1)
check = QPushButton("Check")
countLabel = QLabel("")
check.clicked.connect(lambda: check_player(line1.text()))

VB.addWidget(label)
HB.addLayout(formLayout)
HB.addWidget(check)
HB.addWidget(countLabel)
VB.addLayout(HB)

window.setLayout(VB)
window.show()
sys.exit(app.exec())