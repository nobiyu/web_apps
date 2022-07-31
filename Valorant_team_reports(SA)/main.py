import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
import base64
import lxml
# import pip

# pip.main(['install', 'lxml'])

sns.set_palette('coolwarm')



st.title('Valorant Team Stats for SA Teams')

st.markdown("""
\- by Ayush Bist
\nThis app performs webscraping of stats of team matches and creates a simple comparision report against opponent team(s).
* **Python libraries:** base64, pandas, streamlit, numpy, seaborn
* **Data source:** [liquipedia.net](https://liquipedia.net/).
""")

st.sidebar.header('Input Details here')
teams_dict = {
    'Enigma Gaming(EG)': 'Enigma_Gaming',
    'Exceeli Esports': 'Exceeli_Esports',
    'Global Esports(GE)': 'Global_Esports',
    'Orangutan(OG)': 'Orangutan',
    'Reckoning Esports(RGE)':'Reckoning_Esports',
    'Revenant Esports(RNT)':'Revenant_Esports',
    'True Rippers Esports(TR)':'True_Rippers_Esports',
    'Velocity Gaming(VLT)':'Velocity_Gaming'
 }

team = st.sidebar.selectbox('Select Team: ', teams_dict.keys())

@st.cache
def load_data(team):
    url = "https://liquipedia.net/valorant/" + str(team) + "/Matches"
    html = pd.read_html(url, header=0)
    raw = html[0]
    raw['Score'] = raw['Score'].str.replace("-", ":")
    raw['Score'] = raw['Score'].str.replace("\xa0", "")
    raw = raw.drop(['Tournament', 'VOD'], axis=1)

    new = raw['Score'].str.split(":", n = 1, expand=True)
    new[0] = new[0].replace(['FF', 'W'], '0').apply(int)
    new[1] = new[1].replace([' FF', ' W'], '0').apply(int)
    new['diff'] = new[0] - new[1]
    new['winner'] = np.where(new['diff'] > 0, 'Won', 'Lost')
    rnds_w = new[0]
    rnds_l = new[1]
    df = pd.concat([raw, new['winner']], axis=1)
    return df

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="teamstats.csv">Download CSV File</a>'
    return href


df = load_data(teams_dict[team])

sorted_unique_team = sorted(df['vs. Team'].unique())

opponents = st.sidebar.multiselect('Against:', sorted_unique_team, [])
df_opponent = df[df['vs. Team'].isin(opponents)]

st.write("""
***
Full Dataset:
""")
df
st.markdown(filedownload(df), unsafe_allow_html=True)


if st.button('Show All time stats'):
    st.write(f"""
    ***Total Matches/Series Played:*** {str(len(df))} \n
    ***Won by {team}:*** {str((df['winner']=='Won').sum())}\n
    ***Win rate:*** {np.around((df['winner']=='Won').sum()/len(df) * 100, 2)} %
    """)

    g = sns.catplot(data=df, y='winner', kind='count', order=['Won', 'Lost'], aspect=3/1.5)
    g.set(xlabel='Matches/Series',
        ylabel='Result')
    st.pyplot(g)


st.write("""
***
Against selected teams
""")
df_opponent
st.markdown(filedownload(df_opponent), unsafe_allow_html=True)

if st.button('Show stats against selected teams'):

    st.write(team + ' has faced (' + ', '.join(opponents) + ') ' +  str(len(df_opponent)) + ' times out of which ' + team + ' has won ' + str((df_opponent['winner']=='Won').sum()))

    st.write(f"""
    ***Total Matches/Series Played:*** {str(len(df_opponent))} \n
    ***Won by {team}:*** {str((df_opponent['winner']=='Won').sum())}\n
    ***Win rate:*** {(df_opponent['winner']=='Won').sum()/len(df_opponent) * 100} %
    """)

    h = sns.catplot(data=df_opponent, y='winner', kind='count', order=['Won', 'Lost'], aspect=3/1.5)
    h.set(xlabel='Matches/Series',
        ylabel='Result')
    st.pyplot(h)

fro = df['Date'].max()
to = df['Date'].min()
st.write(f"""
***
Note: Data used is recorded from {fro} to {to}""")
