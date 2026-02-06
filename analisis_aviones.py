import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# leer datos del archivo
datos=pd.read_csv(r'C:\Users\HP Pavilion\Desktop\analisis_de_datos\ejercicio 3 analisis\aviones\aviones_dataset_pro.csv', sep=',')

# limpiar datos del dataframe
datos=datos.dropna(subset=['flight_id', 'airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'delay_minutes', 'status', 'ticket_price','aircraft_type'])

# limpieza profunda de los datos nulos y repetidos 
datos = datos.drop_duplicates()  
datos = datos.dropna(subset=['flight_id', 'airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'delay_minutes', 'status', 'ticket_price','aircraft_type'])
# ver las primeras 30 filas
print(datos.head(30));



# visualizaciones
# grafica de barras por aerolinea
plt.figure(figsize=(12, 6))
aerolineas=datos.groupby('airline')['airline'].count()
aerolineas.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Aerolineas con más vuelos', fontsize=16, fontweight='bold')
plt.xlabel('Aerolinea', fontsize=12)
plt.ylabel('Cantidad de Vuelos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# grafica de barras por origen
plt.figure(figsize=(12, 6))
origen=datos.groupby('origin')['origin'].count()
origen.plot(kind='bar', color='salmon', edgecolor='black')
plt.title('Origen con más vuelos', fontsize=16, fontweight='bold')
plt.xlabel('Origen', fontsize=12)
plt.ylabel('Cantidad de Vuelos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# grafica de barras por destino
plt.figure(figsize=(12, 6))
destino=datos.groupby('destination')['destination'].count()
destino.plot(kind='bar', color='gold', edgecolor='black')
plt.title('Destino con más vuelos', fontsize=16, fontweight='bold')
plt.xlabel('Destino', fontsize=12)
plt.ylabel('Cantidad de Vuelos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# grafica de barras por aerolinea y origen
plt.figure(figsize=(12, 6))
aerolinea_origen=datos.groupby(['airline', 'origin'])['origin'].count()
aerolinea_origen.plot(kind='bar', color='seagreen', edgecolor='black')
plt.title('Aerolineas con más vuelos por origen', fontsize=16, fontweight='bold')
plt.xlabel('Aerolinea', fontsize=12)
plt.ylabel('Cantidad de Vuelos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# grafica de barras por aerolinea y destino
plt.figure(figsize=(12, 6))
aerolinea_destino=datos.groupby(['airline', 'destination'])['destination'].count()
aerolinea_destino.plot(kind='bar', color='seagreen', edgecolor='black')
plt.title('Aerolineas con más vuelos por destino', fontsize=16, fontweight='bold')
plt.xlabel('Aerolinea', fontsize=12)
plt.ylabel('Cantidad de Vuelos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# grafica de pastel por estatus de vuelos
plt.figure(figsize=(14, 8))
status_counts = datos['status'].value_counts()

# Crear gráfico de pastel
plt.pie(status_counts.values, labels=status_counts.index,
        autopct='%1.1f%%', startangle=90,
        colors=plt.cm.Paired.colors,
        explode=[0.05] * len(status_counts))

plt.title('Distribución de Estatus de Vuelos', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()
# histograma de los retrasos en minutos
plt.figure(figsize=(12, 6))
retrasos = datos['delay_minutes'].value_counts()
sns.histplot(datos['delay_minutes'], bins=30, color='purple', kde=True)
plt.title('Histograma de Retrasos en Minutos', fontsize=16, fontweight='bold')
plt.xlabel('Retrasos en Minutos', fontsize=12)
plt.ylabel('Cantidad de Vuelos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

#historigrama de los vuelos mas concurrentes con porcentajes
plt.figure(figsize=(14, 8))

# Crear subplots para múltiples visualizaciones
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Concurrencia por aerolínea
datos['airline'].value_counts(normalize=True).head(10).plot(
    kind='bar', ax=axes[0, 0], color='skyblue', edgecolor='black'
)
axes[0, 0].set_title('Top 10 Aerolíneas más Concurridas', fontweight='bold')
axes[0, 0].set_xlabel('')
axes[0, 0].set_ylabel('Porcentaje (%)')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Concurrencia por origen
datos['origin'].value_counts(normalize=True).plot(
    kind='bar', ax=axes[0, 1], color='salmon', edgecolor='black'
)
axes[0, 1].set_title('Concurrencia por Aeropuerto de Origen', fontweight='bold')
axes[0, 1].set_xlabel('')
axes[0, 1].set_ylabel('Porcentaje (%)')
axes[0, 1].tick_params(axis='x', rotation=45)

# 3. Concurrencia por estado
datos['status'].value_counts(normalize=True).plot(
    kind='bar', ax=axes[1, 0], color='lightgreen', edgecolor='black'
)
axes[1, 0].set_title('Concurrencia por Estado de Vuelo', fontweight='bold')
axes[1, 0].set_xlabel('')
axes[1, 0].set_ylabel('Porcentaje (%)')
axes[1, 0].tick_params(axis='x', rotation=45)

# 4. Concurrencia por tipo de avión
datos['aircraft_type'].value_counts(normalize=True).plot(
    kind='bar', ax=axes[1, 1], color='gold', edgecolor='black'
)
axes[1, 1].set_title('Concurrencia por Tipo de Aeronave', fontweight='bold')
axes[1, 1].set_xlabel('')
axes[1, 1].set_ylabel('Porcentaje (%)')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# historigrama de los los boletos mas vendidos con porcentaje
plt.figure(figsize=(12, 6))
datos['ticket_price'].value_counts(normalize=True).head(10).plot( kind='bar', color='seagreen', edgecolor='black')
plt.title('Top 10 Boletos más Vendidos', fontweight='bold')
plt.xlabel('Boletos', fontsize=12)
plt.ylabel('Porcentaje (%)', fontsize=12)
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# grafica de barras apiladas de los aviones con mas vuelos 
plt.figure(figsize=(12, 6))
aviones_por_aerolinea = datos.groupby('airline')['flight_id'].count()
aviones_por_aerolinea.plot(kind='barh', color='skyblue', edgecolor='black')
plt.title('Top 10 Aerolíneas con más vuelos', fontweight='bold')
plt.xlabel('Cantidad de Vuelos', fontsize=12)
plt.ylabel('Aerolínea', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# grafica de barras apiladas de los aviones con mas vuelos por origen y destinno
plt.figure(figsize=(12, 6))
aviones_por_origen = datos.groupby(['origin', 'destination'])['flight_id'].count()
aviones_por_origen.plot(kind='barh', color='salmon', edgecolor='black')
plt.title('Top 10 Aeropuertos con más vuelos', fontweight='bold')
plt.xlabel('Cantidad de Vuelos', fontsize=12)
plt.ylabel('Aeropuerto', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# grafica de lineas de Retraso promedio por ruta.
plt.figure(figsize=(12, 6))

rutas = datos.groupby('flight_id')['delay_minutes'].mean()

# Tomar solo las 10 rutas con mayor retraso
rutas = rutas.sort_values(ascending=False).head(20)

plt.plot(rutas.index, rutas.values, marker='o')
plt.title('Top 20 rutas con mayor retraso promedio')
plt.xlabel('Ruta')
plt.ylabel('Retraso promedio (minutos)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# grafica de lineas del incremento de costo de los boletos
plt.figure(figsize=(12, 6))
plt.plot(datos['ticket_price'], label='Costo del boleto')
plt.title('Incremento del costo de los boletos')
plt.xlabel('Número de vuelo')
plt.ylabel('Costo del boleto')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# grafica de barras de promedio de retraso por aeronave
plt.figure(figsize=(12, 6))
promedio_retraso_aeronave = datos.groupby('aircraft_type')['delay_minutes'].mean()
promedio_retraso_aeronave.plot(kind='bar', color='gold', edgecolor='black')
plt.title('Promedio de Retraso por Aeronave', fontweight='bold')
plt.xlabel('Aeronave', fontsize=12)
plt.ylabel('Retraso Promedio (minutos)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# totall de los vuelos faltantes y promedio de retraso
total_vuelos_faltantes = datos[datos['status'] == 'missing'].shape[0]
promedio_retraso = datos['delay_minutes'].mean()
print(f'Total de vuelos faltantes: {total_vuelos_faltantes}')
print(f'Promedio de retraso: {promedio_retraso} minutos')

# Aerolinea con el boleto mas caro y el precio
aerolinea_con_boleto_mas_caro = datos[datos['ticket_price'] == datos['ticket_price'].max()]['airline'].value_counts().index[0]
precio_boleto_mas_caro = datos[datos['airline'] == aerolinea_con_boleto_mas_caro]['ticket_price'].max()
print(f'Aerolinea con el boleto mas caro: {aerolinea_con_boleto_mas_caro}')
print(f'Precio del boleto mas caro: {precio_boleto_mas_caro}')

# Destino con el vuelo mas largo y el tiempo de vuelo
destino_con_vuelo_mas_longo = datos[datos['flight_id'] == datos['flight_id'].max()]['destination'].value_counts().index[0]
vuelo_mas_longo = datos[datos['destination'] == destino_con_vuelo_mas_longo]['flight_id'].max()
print(f'Destino con el vuelo mas largo: {destino_con_vuelo_mas_longo}')
print(f'Vuelo mas largo: {vuelo_mas_longo}')

# Origen con el vuelo mas corto y el tiempo de vuelo
origen_con_vuelo_mas_corto = datos[datos['flight_id'] == datos['flight_id'].min()]['origin'].value_counts().index[0]
vuelo_mas_corto = datos[datos['origin'] == origen_con_vuelo_mas_corto]['flight_id'].min()
print(f'Origen con el vuelo mas corto: {origen_con_vuelo_mas_corto}')
print(f'Vuelo mas corto: {vuelo_mas_corto}')

vuelos_cancelados_por_aerolinea = datos[datos['status'].str.lower().str.contains('Cancelled')].groupby('airline')['flight_id'].count()

print("Vuelos cancelados por aerolínea:")
print(vuelos_cancelados_por_aerolinea)
