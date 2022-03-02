# importamos las Librerías que vamos a usar
import pandas as pd
from matplotlib import pyplot as plt

# especifico que muestre todo sin resrticción
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('Display.width', None)

# llamo a mis datos y creo mi diccionario
content_data = 'activity.csv'
df = pd.read_csv(content_data)
ddias = {'Dias': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
         'id_dias': [0, 1, 2, 3, 4, 5, 6]
        }
#reviso los Encabezados
# print(list(df))

# elimino encabezados que no serán utilizados
df = df.drop(['Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark', 'Country'], axis=1)
# print(list(df))

# transformo la data de tiempo a la conocida
df['Start Time'] = pd.to_datetime(df['Start Time'], utc=True)
df = df.set_index('Start Time')
df.index = df.index.tz_convert('America/Santiago')
df = df.reset_index()

# Transformamos la Duración a una Medida reconocible con to_timedelta
df['Duration'] = pd.to_timedelta(df['Duration'])

# Armo una Columna de Semana y hora
df['WeekDay'] = df['Start Time'].dt.weekday
df['Hora'] = df['Start Time'].dt.hour

#reviso los primeros Datos
# print(df.head(5))

# Creo un Data ser en Base al Diccionario
df_dias = pd.DataFrame(ddias)
# print(list(df_dias))

# Usando el método UNIR Dejo que el Id_Dias sea el index o clave y lo relaciono con el Día de la semana
df = df.join(df_dias.set_index('id_dias'), on = 'WeekDay')
# print(df.head(5))

# Limpio lo que no me interesa, dejo sólo el Perfil CASA y Niego lo que sea Trailer
df = df[df['Profile Name'].str.contains('Casa', regex=False) & ~df['Title'].str.contains('Trailer')]
df = df[(df['Duration'] > '0 days 00:01:00')]
# print(df.head(5))

# Analizando al Data
tiempo = df['Duration'].sum()
horatop = df["Hora"].value_counts().idxmax()
diatop = df["Dias"].value_counts().idxmax()
topset = df['Title'].value_counts().head(5)

#Sacamos los mensajes
print(f'\nTiempo que Ha gastado en Netflix: {tiempo}')
print('El día que más Netflix ve es {}'.format(diatop))
print(f'El Horario en el que consume más Netflix es a las {horatop} horas\n')
print(f'Estas son las 5 Películas Más vistas:\n{topset}')

# preparamos info apra plot
# la ponemos en una nueva data argupada y dejamos el index en orden
netflixplot = df['WeekDay'].value_counts().sort_index()

# ploteamos
''' netflixplot.plot(kind='XXX')
'bar’ or ‘barh’ for bar plots
 ‘hist’ for histogram
 ‘box’ for boxplot
 'area’ for area plots
 ‘kde’ or ‘density’ for density plots (Scioy module)
 ‘scatter’ for scatter plots (DF ONLY)
 ‘hexbin’ for hexagonal bin plots (DF ONLY)
 ‘pie’ for pie plots 
'''
plt.plot(netflixplot)
plt.legend(['Visualizaciones'])
plt.xlabel('Días de la Semana')
plt.ylabel('Nº Visualizaciones')
plt.show()
