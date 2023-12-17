from __future__ import annotations

class Ytaron():

    def __init__(self, jour:int=1, heures:int=12, halakim:int=793)->None:
        self.day = jour
        self.heures = heures
        self.halakim = halakim

    def __repr__(self)->str:
        return f"Ytaron{(self.day, self.heures, self.halakim)}"

    def __add__(self, ytaron:tuple|Ytaron)->Ytaron:

        if isinstance(ytaron,tuple):
            halakim = self.halakim + ytaron[2]
            heures = self.heures + ytaron[1] + halakim // 1080
            jours =  self.day + ytaron[0] + heures // 24
            return Ytaron(jours%7, heures%24, halakim%1080)

        elif isinstance(ytaron,Ytaron):
            halakim = ytaron.halakim + self.halakim
            heures = ytaron.heures + self.heures + halakim // 1080
            jours = ytaron.day + self.day + heures // 24
            return Ytaron(jours%7, heures%24, halakim%1080)

    def __mul__(self, nombre:int)->Ytaron:

        halakim = self.halakim * nombre
        heures = self.heures*nombre + halakim//1080
        return Ytaron((self.day*nombre + heures//24) % 7, heures % 24, halakim % 1080)


MAHZOR_CUMULS = (
    (0,0,0),(4,8,876),(1,17,672),(0,15,181),(4,23,1057),
    (2,8,853),(1,6,362),(5,15,158),(4,12,747),(1,21,543),
    (6,6,339),(5,3,928),(2,12,724),(6,21,520),(5,19,29),
    (3,3,905),(0,12,701),(6,10,210),(3,19,6)
)

HODASHIM_EZRAHIIM = ('ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר')


# WEEK_DAYS = ('Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi')
WEEK_DAYS = ('ראשון','שני','שלישי','רביעי','חמישי','שישי','שבת')

class Chana():

    def __init__(self, chana:int)->None:

        rang = chana % 19 or 19

        # self.isbissextile:
        self.isbissextile = rang in {3,6,8,11,14,17,19}

        # self.molad:
        cycles = chana // 19 + (rang < 19) -1
        molad = Ytaron(2,16,595)*(cycles) + MAHZOR_CUMULS[rang-1] + (2,5,204)
        self.molad = (molad.day, molad.heures, molad.halakim)

        # self.ecart:
        roch, heures, halakim = self.molad
        if heures > 17 or \
        (not self.isbissextile and roch == 3 and heures*1080 + halakim > 9923) or \
        (rang in {1,4,7,9,12,15,18} and roch == 2 and heures*1080 + halakim > 16788):
            roch += 1
        roch += roch in {1,4,6}
        next = Ytaron(self.molad[0], heures, halakim) + ((4,8,876),(5,21,589))[self.isbissextile]
        sof, heures, halakim = next.day, next.heures, next.halakim
        if heures > 17 or \
        (rang in {1,3,4,6,8,9,11,12,14,15,17,19} and sof == 3 and heures*1080 + halakim > 9923) or \
        (self.isbissextile and sof == 2 and heures*1080 + halakim > 16788):
            sof += 1
        sof += sof in {1,4,6}
        self.ecart = (sof - roch - 3 - self.isbissextile*2) % 7


class Taarikh():

    def __init__(self, day:int, month:int, year:int)->None:
        annee = Chana(year)
        if ((year < 0) or (day < 1) or (day > 30)) or \
           (month > 12 + annee.isbissextile) or \
           (month == 4 and day > 29) or \
           (month - annee.isbissextile in {6,8,10,12} and day > 29) or \
           (month == 2 and annee.ecart < 2 and day > 29) or \
           (month == 3 and annee.ecart == 0 and day > 29):
            raise ValueError(f"Invalide date: {day}/{month}/{year}")
        self.year = year
        self.day = day
        self.month = month

    def weekday(self)->str:
        jours = taarikh_yamim(self)
        return WEEK_DAYS[jours % 7]

    def __add__(self, nombre:int)->Taarikh:
        return yamim_taarikh(taarikh_yamim(self) + nombre)

    def __sub__(self, jours):
        if isinstance(jours, int):
            return yamim_taarikh(taarikh_yamim(self) - jours)
        if isinstance(jours, tuple) or isinstance(jours, Taarikh):
            return taarikh_yamim(self) - taarikh_yamim(jours)

    def __repr__(self)->str:
        chana = Chana(self.year)
        adar = ('אדר','אדר-א')[chana.isbissextile]
        # adar = ('Adar','Adar_A')[chana.isbissextile]

        moisAnnee = ['תשרי','חשוון','כסלו','טבת','שבט',adar,'ניסן','אייר','סיון','תמוז','אב','אלול']
        if chana.isbissextile: moisAnnee.insert(6,'אדר-ב')
        # moisAnnee = ['Tishri','Heshvan','Kislev','Tevet','Chevat',adar,'Nissan','Iyar','Sivan','Tamouz','Av','Eloul']
        # if chana.isbissextile: moisAnnee.insert(6,'Adar_B')

        return f"{self.weekday()} {self.day} {moisAnnee[self.month-1]} {self.year}"

    def __eq__(self, other:object)->bool:
        if isinstance(other, tuple):
            jour, month, year = other
        elif isinstance(other, Taarikh):
            jour, month, year = other.day, other.month, other.year
        else:
            return NotImplemented
        return self.day==jour and self.month==month and self.year==year

    def __lt__(self, other:object)->bool:
        if isinstance(other, tuple):
            jour, month, year = other
        elif isinstance(other, Taarikh):
            jour, month, year = other.day, other.month, other.year
        if self.year != year:
            return self.year < year
        if self.month != month:
            return self.month < month
        return self.day < jour

    def __gt__(self, other:object)->bool:
        return other < self



def taarikh_yamim(taarikh:object)->int:

    if isinstance(taarikh,tuple):
        taarikh = Taarikh(*taarikh)

    jours, hodashim, annee = taarikh.day, taarikh.month, taarikh.year

    chana = Chana(annee)
    heshvan = chana.ecart == 2
    kislev = chana.ecart > 0
    hk = heshvan + kislev
    hkb = hk + chana.isbissextile

    cumuls = (0, 30, 59+heshvan, 88+hk, 117+hk, 147+hk, 176+hkb, 206+hk, 235+hkb, 265+hk, 294+hkb, 324+hk, 353+hkb)
    jours += cumuls[hodashim-1]

    while annee > 1:
        annee -= 1
        chana = Chana(annee)
        jours += 353 + chana.ecart + chana.isbissextile*2*3*5

    return jours



def yamim_taarikh(jours:int)->Taarikh:

    if jours > 0:
        annee = 1
        chana = Chana(annee)
        longueur = 353 + chana.ecart + chana.isbissextile * 30

        while jours >= longueur:
            jours -= longueur
            annee += 1
            chana = Chana(annee)
            longueur = 353 + chana.ecart + chana.isbissextile * 30

        if not jours:
            annee -= 1
            bissextile = annee % 19 in {0,3,6,8,11,14,17}
            return Taarikh(29, 12+bissextile, annee)

        B = chana.isbissextile

        months_lenghts = (
            30, 29+(chana.ecart==2), 29+(chana.ecart>0), 29,
            30, 29+B, 30-B, 29+B, 30-B, 29+B, 30-B, 29+B, 29
        )
        hodashim = 0
        while jours > months_lenghts[hodashim]:
            jours -= months_lenghts[hodashim]
            hodashim += 1

        return Taarikh(jours, hodashim+1, annee)



def jours_date(jours:int)->tuple:

    "Convertit un nombre de jours en une date civile."

    if not isinstance(jours,int):
        return NotImplemented

    jour = WEEK_DAYS[jours%7]

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

    cumuls = (
        31, 28+(0 if ans % 4 or (quadriennats == 24 and siecles % 4) else 1),
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
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
    days, months, years = date
    years -= 1

    days += (years // 400) * 146097
    years %= 400

    days += (years // 100) * 36524
    years %= 100

    days += (years // 4) * 1461
    years %= 4

    days += years * 365
    year = years + 1

    d = 0 if year % 4 else 1
    cumuls = (0, 31, d+59, d+90, d+120, d+151, d+181, d+212, d+243, d+273, d+304, d+334)

    return days + cumuls[months-1]


def convertHC(date:object)->str:

    jour, jours, hodashim, annee = jours_date(taarikh_yamim(date)-1373428)
    hodashim = HODASHIM_EZRAHIIM[hodashim-1]
    return f"{jour} {jours} {hodashim} {annee}"


def convertCH(date:tuple)->Taarikh:

    return yamim_taarikh(date_jours(date) + 1373428)


# print()
# print("4 Janvier 2022 → hebrew:", convertCH((4,1,2022)))
# print("2 Chevat 5782 → civil:", convertHC((2,5,5782)))
# print()
# print("4 Fevrier 2022 → hebrew:", convertCH((4,2,2022)))
# print("3 adar1 5782 → civil:", convertHC((3,6,5782)))
# print()
# print("4 Mars 2022 → hebrew:", convertCH((4,3,2022)))
# print("1 adar2 5782 → civil:", convertHC((1,7,5782)))
# print()
# print("4 Avril 2022 → hebrew:", convertCH((4,4,2022)))
# print("3 nissan 5782 → civil:", convertHC((3,8,5782)))
# print("4 Février 2022 → hebrew:", convertCH((4,2,2022)))
# print("3 adar1 5782 → civil:", convertHC((3,6,5782)))
