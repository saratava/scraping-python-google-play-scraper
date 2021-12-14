import pandas as pd
import numpy as np
from google_play_scraper import Sort, reviews_all
from pandas_profiling import ProfileReport as pr
import os


# App Scraping Alexa - google play
br_reviews = reviews_all(
    'com.amazon.dee.app',
    lang='pt',  # defaults to 'en'
    sleep_milliseconds=0,  # defaults to 0 
    country='br',  # defaults to 'us'
    sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
)

# Geração de DataFrame do atributo Review do App Alexa
df_reviews = pd.DataFrame(np.array(br_reviews), columns=['review'])

df_completa = df_reviews.join(pd.DataFrame(df_reviews.pop('review').tolist()))

df_final = df_completa.drop(columns=['reviewId','userName','userImage', 'repliedAt'])

# Filtragem de acordo com o score (estrelas) atribuida
filtro_positiva = df_final['score'] >= 4
df_positiva = df_final[filtro_positiva]

filtro_neutra = df_final['score'] == 3
df_neutra = df_final[filtro_neutra]

filtro_negativa = df_final['score'] < 3
df_negativa = df_final[filtro_negativa]

path = os.getcwd()

# Report Positivas
profile_positivo = pr(df_positiva, title='Report Geral Reviews Alexa - Avaliações Positivas', html={'style':{'full_width':True}})

profile_positivo.to_notebook_iframe()

profile_positivo.to_file(output_file=f"{path}/Reports-html/Report_Positivas.html")

# Report Neutras
profile_neutra = pr(df_neutra, title='Report Geral Reviews Alexa - Avaliações Neutras', html={'style':{'full_width':True}})

profile_neutra.to_notebook_iframe()

profile_neutra.to_file(output_file=f"{path}/Reports-html/Report_Neutras.html")

# Report Negativas
profile_negativa = pr(df_negativa, title='Report Geral Reviews Alexa - Avaliações Negativas', html={'style':{'full_width':True}})

profile_negativa.to_notebook_iframe()

profile_negativa.to_file(output_file=f"{path}/Reports-html/Report_Negativas.html")

df_positiva.to_csv(f"{path}/sheets/df_positiva.csv", index=False)               
df_neutra.to_csv(f"{path}/sheets/df_neutra.csv", index=False)                   
df_negativa.to_csv(f"{path}/sheets/df_negativa.csv", index=False) 

from banco.request_database import database
database()

def etc():
    path = os.getcwd()
    dir = os.listdir(f'{path}/sheets')
    for file in dir:
        if file == "df_negativa.csv":
            os.remove(file)
            
##########################  Package Tools ########################## 
# Gerar planilha completa pela primeira vez:                       #
# df_final.to_excel("scraping_com_python-limpa.xlsx", index=False) #
#                                                                  #
# Gerar planilhas de acordo com score:                             #
# df_positiva.to_csv("df_positiva.csv", index=False)               #
# df_neutra.to_csv("df_neutra.csv", index=False)                   #
# df_negativa.to_csv("df_negativa.csv", index=False)               #
#                                                                  #
####################################################################