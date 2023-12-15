from __future__ import annotations
import streamlit as st


class Ytaron():

    def __init__(self, jour:int=1, heures:int=12, halakim:int=793)->None:
        self.jour = jour
        self.heures = heures
        self.halakim = halakim

    def __repr__(self)->str:
        return f"Ytaron{(self.jour, self.heures, self.halakim)}"

    def __add__(self, ytaron:tuple|Ytaron)->Ytaron:

        if isinstance(ytaron,tuple):
            halakim = self.halakim + ytaron[2]
            heures = self.heures + ytaron[1] + halakim // 1080
            jours =  self.jour + ytaron[0] + heures // 24
            return Ytaron(jours%7, heures%24, halakim%1080)

        elif isinstance(ytaron,Ytaron):
            halakim = ytaron.halakim + self.halakim
            heures = ytaron.heures + self.heures + halakim // 1080
            jours = ytaron.jour + self.jour + heures // 24
            return Ytaron(jours%7, heures%24, halakim%1080)

    def __mul__(self, nombre:int)->Ytaron:

        halakim = self.halakim * nombre
        heures = self.heures*nombre + halakim//1080
        return Ytaron((self.jour*nombre + heures//24) % 7, heures % 24, halakim % 1080)


cumulYtaronAnnees = ((0,0,0),(4,8,876),(1,17,672),(0,15,181),(4,23,1057),
                     (2,8,853),(1,6,362),(5,15,158),(4,12,747),(1,21,543),
                     (6,6,339),(5,3,928),(2,12,724),(6,21,520),(5,19,29),
                     (3,3,905),(0,12,701),(6,10,210),(3,19,6))


class Chana():

    def __init__(self, chana:int)->None:

        rang = chana % 19 or 19

        # self.bissextile:
        self.bissextile = rang in {3,6,8,11,14,17,19}

        # self.molad:
        cycles = chana // 19 + (rang < 19) -1
        molad = Ytaron(2,16,595)*(cycles) + cumulYtaronAnnees[rang-1] + (2,5,204)
        self.molad = (molad.jour, molad.heures, molad.halakim)

        # self.ecart:
        roch, heures, halakim = self.molad
        if heures > 17 or \
        (not self.bissextile and roch == 3 and heures*1080 + halakim > 9923) or \
        (rang in {1,4,7,9,12,15,18} and roch == 2 and heures*1080 + halakim > 16788):
            roch += 1
        roch += roch in {1,4,6}
        next = Ytaron(self.molad[0], heures, halakim) + ((4,8,876),(5,21,589))[self.bissextile]
        sof, heures, halakim = next.jour, next.heures, next.halakim
        if heures > 17 or \
        (rang in {1,3,4,6,8,9,11,12,14,15,17,19} and sof == 3 and heures*1080 + halakim > 9923) or \
        (self.bissextile and sof == 2 and heures*1080 + halakim > 16788):
            sof += 1
        sof += sof in {1,4,6}
        self.ecart = (sof - roch - 3 - self.bissextile*2) % 7


# SEMAINE = ('Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi')
SEMAINE = ('ראשון','שני','שלישי','רביעי','חמישי','שישי','שבת')


class Taarikh():

    def __init__(self, jour:int, hodashim:int, annee:int)->None:
        self.jour = jour
        self.hodashim = hodashim
        self.annee = annee

    def jourDeLaSemaine(self)->str:
        jours = taarikh_yamim(self)
        return SEMAINE[jours % 7]

    def __add__(self, nombre:int)->Taarikh:
        return yamim_taarikh(taarikh_yamim(self) + nombre)

    def __sub__(self, jours):
        if isinstance(jours, int):
            return yamim_taarikh(taarikh_yamim(self) - jours)
        if isinstance(jours, tuple) or isinstance(jours, Taarikh):
            return taarikh_yamim(self) - taarikh_yamim(jours)

    def __repr__(self)->str:
        chana = Chana(self.annee)
        adar = ('אדר','אדר א')[chana.bissextile]
        # adar = ('Adar','Adar_A')[chana.bissextile]

        moisHebraiques = ['תשרי','חשוון','כסלו','טבת','שבט',adar,'ניסן','אייר','סיון','תמוז','אב','אלול']
        if chana.bissextile: moisHebraiques.insert(6,'אדר ב')
        # moisHebraiques = ['Tishri','Heshvan','Kislev','Tevet','Chevat',adar,'Nissan','Iyar','Sivan','Tamouz','Av','Eloul']
        # if chana.bissextile: moisHebraiques.insert(6,'Adar_B')

        return f"{self.jourDeLaSemaine()}   {self.jour}   {moisHebraiques[self.hodashim-1]}   {self.annee}"

    def __eq__(self, other:object)->bool:
        if isinstance(other, tuple):
            jour, hodashim, annee = other
        elif isinstance(other, Taarikh):
            jour, hodashim, annee = other.jour, other.hodashim, other.annee
        else:
            return NotImplemented
        return self.jour==jour and self.hodashim==hodashim and self.annee==annee

    def __lt__(self, other:object)->bool:
        if isinstance(other, tuple):
            jour, hodashim, annee = other
        elif isinstance(other, Taarikh):
            jour, hodashim, annee = other.jour, other.hodashim, other.annee
        if self.annee != annee:
            return self.annee < annee
        if self.hodashim != hodashim:
            return self.hodashim < hodashim
        return self.jour < jour

    def __gt__(self, other:object)->bool:
        return other < self


def taarikh_yamim(taarikh:object)->int:

    if isinstance(taarikh,Taarikh):
        jours,hodashim,annee = taarikh.jour, taarikh.hodashim, taarikh.annee
    elif isinstance(taarikh,tuple):
        jours,hodashim,annee = taarikh
    chana = Chana(annee)
    heshvan = chana.ecart == 2
    kislev = chana.ecart > 0
    hk = heshvan + kislev
    hkb = hk + chana.bissextile

    cumuls = (0, 30, 59+heshvan, 88+hk, 117+hk, 147+hk, 176+hkb, 206+hk, 235+hkb, 265+hk, 294+hkb, 324+hk, 353+hkb)
    jours += cumuls[hodashim-1]

    while annee > 1:
        annee -= 1
        chana = Chana(annee)
        jours += 353 + chana.ecart + chana.bissextile*2*3*5

    return jours


def yamim_taarikh(jours:int)->Taarikh:

    if jours > 0:
        annee = 1
        chana = Chana(annee)
        longueur = 353 + chana.ecart + chana.bissextile*2*3*5

        while jours >= longueur:
            jours -= longueur
            annee += 1
            chana = Chana(annee)
            longueur = 353 + chana.ecart + chana.bissextile*2*3*5

        if not jours:
            annee -= 1
            bissextile = annee % 19 in {0,3,6,8,11,14,17}
            return Taarikh(29, 12+bissextile, annee)

        B = chana.bissextile

        cumuls = (30, 29+(chana.ecart==2), 29+(chana.ecart>0), 29, 30, 29+B, 30-B, 29+B, 30-B, 29+B, 30-B, 29+B, 29)

        hodashim = 0
        while jours > cumuls[hodashim]:
            jours -= cumuls[hodashim]
            hodashim += 1

        return Taarikh(jours, hodashim+1, annee)


def jours_date(jours:int)->tuple:
    "Convertit un nombre de jours en une date civile."

    if not isinstance(jours,int):
        return NotImplemented

    jour = SEMAINE[jours%7]

    quadrisiecles = jours//146097

    jours %= 146097
    siecles = jours//36524

    jours %= 36524
    if siecles == 4:
        siecles == 3
        jours == 36524
    quadriennats = jours//1461

    jours %= 1461
    ans = jours//365

    jours %= 365
    if ans == 4:
        ans = 3
        jours = 365

    if not jours:
        return jour, 31, 12, quadrisiecles*400 + siecles*100 + quadriennats*4 + ans

    ans += 1

    cumuls = (31, 28+(0 if ans % 4 or (quadriennats == 24 and siecles % 4) else 1), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    hodashim = 0
    while jours > cumuls[hodashim]:
        jours -= cumuls[hodashim]
        hodashim += 1

    return jour, jours, hodashim+1, quadrisiecles*400 + siecles*100 + quadriennats*4 + ans


def date_jours(date:tuple)->int:
    """
    Convertit une date civile en un nombre de jours
    (depuis le 01/01/0001 du calendrier civil Géorgien).
    """
    jours,hodashim,annee = date

    annees = annee - 1
    jours += (annees // 400) * 146097

    annees %= 400
    jours += (annees // 100) * 36524

    annees %= 100
    jours += (annees // 4) * 1461

    annees %= 4
    jours += annees*365

    d = 0 if annee % 4 else 1
    cumuls = (0, 31, d+59, d+90, d+120, d+151, d+181, d+212, d+243, d+273, d+304, d+334)

    return jours + cumuls[hodashim-1]


def convertHC(date:object)->str:

    jour, jours, hodashim, annee = jours_date(taarikh_yamim(date)-1373428)
    # hodashim = ('Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Décembre')[hodashim-1]
    hodashim = ('ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר')[hodashim-1]
    return f"{jour} {jours} {hodashim} {annee}"


def convertCH(date:tuple)->Taarikh:
    return yamim_taarikh(date_jours(date) + 1373428)






st.write("""
         <center>
                <h1>
                    <font color='#29a2ba'>
                    ממיר תאריכים
                    </font>
                </h1>
            </center>
         """, unsafe_allow_html=True)


c1, c2, c3 = st.columns(3)
with c1: st.write("")
# with c2: st.image('Molad.jpeg')
# with c2: st.image('Symbolique.jpeg')
with c2: st.image('Soleil & Lune.jpeg')
with c3: st.write("")

st.write("</br>", unsafe_allow_html=True)

left, _, right = st.columns((20,1,20))

with right:
    st.write("<center><h5><font color=#D06070>מעברי ללועזי</font></h5><center/>", unsafe_allow_html=True)

    col1, col2, col3  = st.columns(3)

    chana = col1.text_input("שנה עברית")
    if chana.isdigit():
        chana = int(chana)
        shana = Chana(chana)
        hodashim = {
                    "ניסן":1, "אייר":2, "סיון":3, "תמוז":4,
                    "אב":6, "אלול":6, "תשרי":7, "חשוון":8,
                    "כסלו":9, "טבת":10, "שבט":11,
                    f"אדר{' א' if shana.bissextile else ''}":12,
        }
        if shana.bissextile:
            hodashim['אדר ב']=13

        hodesh = col2.selectbox("חודש עברי", options=hodashim, index=None, placeholder="בחר חודש")

        if hodesh:
            hodesh = hodashim[hodesh]

            yamim = {
                "א":1, "ב":2, "ג":3, "ד":4, "ה":5, "ו":6,
                "ז":7, "ח":8, "ט":9, "י":10, "יא":11, "יב":12,
                "יג":13, "יד":14, "טו":15, "טז":16, "יז":17, "יח":18,
                "יט":19, "כ":20, "כא":21, "כב":22, "כג":23, "כד":24,
                "כה":25, "כו":26, "כז":27, "כח":28, "כט":29
            }
            if hodesh in {1,3,5,7,11,13} or (hodesh == 8 and shana.ecart > 0) or (hodesh == 9 and shana.ecart == 2):
                yamim["ל"]=30

            yom = col3.selectbox("יום", options=yamim, index=None, placeholder="בחר יום")

            if yom:
                yom = yamim[yom]
                taarikh = Taarikh(yom, (hodesh-6)%(12+shana.bissextile), chana)
                date = convertHC(taarikh)
                st.write(f"<h4><center><font color='#E08070'>יום {date}<font/></center></h4>", unsafe_allow_html=True)


with left:
    st.write("<center><h5><font color='#579F83'>מלועזי לעברי</font></h5><center/>", unsafe_allow_html=True)

    col1, col2, col3  = st.columns(3)

    year = col3.text_input("שנה לועזית")
    if year.isdigit():
        year = int(year)
        # bissextile = (year % 4==0 and year % 100 != 0) or (year % 400 == 0)
        months = {
            "ינואר":1, "פברואר":2, "מרץ":3, "אפריל":4,
            "מאי":5, "יוני":6, "יולי":7, "אוגוסט":8,
            "ספטמבר":9, "אוקטובר":10, "נובמבר":11, "דצמבר":12
        }
        month = col2.selectbox("חודש לועזי", options=months, index=None, placeholder="בחר חודש")
        if month:
            month = months[month]
            last_day = 30 + (month in {1,3,5,7,8,10,12})
            if month == 2 and (year % 4 or (year % 100 == 0 and year % 400)):
                last_day -= 2
            day = col1.selectbox("תאריך", options=range(1, last_day+1), index=None, placeholder="בחר יום")
            if day:
                date = (day, month, year)
                date = convertCH(date).__str__().split()
                jours = {'1':'א',  '2':'ב',  '3':'ג',  '4':'ד',  '5':'ה',  '6':'ו',
             '7':'ז',  '8':'ח',  '9':'ט',  '10':'י',  '11':'יא',  '12':'יב',
             '13':'יג',  '14':'יד',  '15':'טו',  '16':'טז',  '17':'יז',  '18':'יח',
             '19':'יט', '20':'כ',  '21':'כא',  '22':'כב',  '23':'כג',  '24':'כד',
             '25':'כה',  '26':'כו',  '27':'כז',  '28':'כח',  '29':'כט',  '30':'ל'}


                date[1] = jours[date[1]]

                st.write(f"<h4><center><font color='#57DFA3'>יום {' '.join(date)}<font/></center></h4>", unsafe_allow_html=True)
