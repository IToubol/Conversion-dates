import streamlit as st
from calendarcomputing import Chana, Taarikh, convertCH, convertHC

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
with c2: st.image('Soleil & Lune.jpeg')
with c3: st.write("")

months = {
    "ינואר":1, "פברואר":2, "מרץ":3, "אפריל":4,
    "מאי":5, "יוני":6, "יולי":7, "אוגוסט":8,
    "ספטמבר":9, "אוקטובר":10, "נובמבר":11, "דצמבר":12
}

left, middle, right = st.columns((6,2,6))

with left:
    st.write("<center><h5><font color=#D06070>מעברי ללועזי</font></h5><center/>", unsafe_allow_html=True)

    hodashim = {
        "ניסן":1, "אייר":2, "סיון":3, "תמוז":4,
        "אב":5, "אלול":6, "תשרי":7, "חשוון":8,
        "כסלו":9, "טבת":10, "שבט":11,
    }

    chana = st.text_input("שנה עברית")
    if chana:
        chana = chana.strip()
        if chana.isdigit():
            chana = int(chana)
            shana = Chana(chana)
            hodashim[f"אדר{'-א' if shana.isbissextile else ''}"]=12
            if shana.isbissextile:
                hodashim['אדר-ב']=13

            col2, col1 = st.columns(2)

            hodesh = col1.selectbox("חודש עברי", options=hodashim, index=None, placeholder="בחר חודש", key='hodesh')

            if hodesh:
                hodesh = hodashim[hodesh]
                # print(hodesh)
                # hodesh

                hodesh = ((hodesh-6)%(12+shana.isbissextile)) or 12+shana.isbissextile
                # hodesh

            yamim = {
                "א":1, "ב":2, "ג":3, "ד":4, "ה":5, "ו":6,
                "ז":7, "ח":8, "ט":9, "י":10, "יא":11, "יב":12,
                "יג":13, "יד":14, "טו":15, "טז":16, "יז":17, "יח":18,
                "יט":19, "כ":20, "כא":21, "כב":22, "כג":23, "כד":24,
                "כה":25, "כו":26, "כז":27, "כח":28, "כט":29
            }
            if hodesh in {
                1, 5,
                7-shana.isbissextile,
                9-shana.isbissextile,
                11-shana.isbissextile,
                13-shana.isbissextile
            } or (hodesh == 2 and shana.ecart == 2) or (hodesh == 3 and shana.ecart > 0):
                yamim["ל"]=30

            yom = col2.selectbox("יום", options=yamim if hodesh else (None,), index=None, placeholder="בחר יום")

            if yom:
                yom = yamim[yom]
                taarikh = Taarikh(yom, hodesh, chana)
                date = convertHC(taarikh).split()

            if st.button("המרה", use_container_width=True, key = "hebrew_to_civil"):
                if hodesh and yom:
                    st.write(f"<h4><center><font color='#E08070'>{date[0]} :  {date[1]} \ {date[2]} \ {date[3]}<font/></center></h4>", unsafe_allow_html=True)
                    st.text(f"{date[1]}.{months[date[2]]}.{date[3]}")
                else:
                    st.text(f"השנה העברית {chana}\nרוכבת על שתי השנים\n{chana-3761}|{chana-3760} הלועזיות")
        else:
            st.warning("ציון שנה במספר דיגיטלי בלבד")

middle.write("")

with right:

    days = {
        '1':'א',  '2':'ב',  '3':'ג',  '4':'ד',  '5':'ה',  '6':'ו',
        '7':'ז',  '8':'ח',  '9':'ט',  '10':'י',  '11':'יא',  '12':'יב',
        '13':'יג',  '14':'יד',  '15':'טו',  '16':'טז',  '17':'יז',  '18':'יח',
        '19':'יט', '20':'כ',  '21':'כא',  '22':'כב',  '23':'כג',  '24':'כד',
        '25':'כה',  '26':'כו',  '27':'כז',  '28':'כח',  '29':'כט',  '30':'ל'
    }

    st.write("<center><h5><font color='#579F83'>מלועזי לעברי</font></h5><center/>", unsafe_allow_html=True)

    year = st.text_input("שנה לועזית")

    if year:

        year = year.strip()

        if year.isdigit():

            year = int(year)

            col2, col1  = st.columns(2)

            month = col2.selectbox("חודש לועזי", options=months, index=None, placeholder="בחר חודש")

            days_options = (None,)
            if month:
                month = months[month]
                last_day = 30 + (month in {1,3,5,7,8,10,12})
                if month == 2:
                    last_day -= 1 + (year % 4 or (year % 100 == 0 and year % 400))
                days_options = range(1, last_day+1)
            day = col1.selectbox("תאריך", options=days_options, index=None, placeholder="בחר יום")

            if month and day:
                date = convertCH((day, month, year))
                # print("éléments de date:", date.year, date.month, date.day)
                convert_date = date.__str__().split()
                # print("convert date:", convert_date)
                convert_date[1] = days[convert_date[1]]

            if st.button("המרה", use_container_width=True, key = "civil_to_hebrew"):
                if month and day:
                    isbissextile = Chana(date.year).isbissextile
                    digital_month = (date.month-6-isbissextile) % (12+isbissextile)
                    digital_month = digital_month or 12+isbissextile
                    st.write(f"<h4><center><font color='#57DFA3'>{convert_date[0]} :  {convert_date[1]} \ {convert_date[2]} \ {convert_date[3]}<font/></center></h4>", unsafe_allow_html=True)
                    st.text(f"{date.day}.{digital_month}.{date.year}")
                else:
                    st.text(f"השנה הלועזית {year}\nרוכבת על שתי השנים\n{year+3760}|{year+3761} העבריות")
        else:
            st.warning("ציון השנה במספר דיגיטלי בלבד")