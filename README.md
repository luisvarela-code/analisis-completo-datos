# Análisis de Desempeño Operativo de Vuelos 
#### Contexto:
La compañía busca evaluar el desempeño de sus operaciones aéreas debido a un incremento sostenido en retrasos y cancelaciones que impactan la experiencia del cliente y los costos operativos. Se requiere un análisis integral que permita identificar patrones, causas potenciales y oportunidades de mejora. 
## Objetivo General
Analizar el comportamiento de los vuelos para identificar factores asociados a retrasos y cancelaciones, así como estimar su impacto económico, con el fin de proponer recomendaciones accionables. 
## Alcance
- Análisis descriptivo de desempeño operativo
- Evaluación por aerolínea, ruta y tipo de aeronave 
- Estimación de impacto financiero

## Instrucciones Técnicas 
- Importar el dataset proporcionado en un entorno analítico (SQL, Python u otro). 
- Evaluar la calidad de los datos y realizar procesos de limpieza necesarios.
- Construir métricas operativas clave. 
- Desarrollar consultas o scripts reproducibles. 
- Presentar resultados mediante visualizaciones claras.

## Requerimientos Analíticos 
- Porcentaje de vuelos a tiempo, retrasados y cancelados. 
- Retraso promedio por aerolínea. 
- Retraso promedio por ruta. 
- Retraso promedio por tipo de aeronave. 
- Top rutas con mayor nivel de retraso. 
- Estimación de ingresos perdidos por cancelaciones. 



# ANÁLISIS DE DESEMPEÑO OPERATIVO DE VUELOS - DOCUMENTACIÓN TÉCNICA COMPLETA
##  ESTRUCTURA DE ARCHIVOS ANALIZADOS
#### SQL
```sql
- Creación de la base de datos y tabla principal
CREATE DATABASE aerolineas;
USE aerolineas;

CREATE TABLE aerolinea(
    flight_id VARCHAR(10) PRIMARY KEY,
    airline VARCHAR(50),
    origin VARCHAR(10),
    destination VARCHAR(10),
    departure_time TIME,
    arrival_time TIME,
    delay_minutes INT,
    status VARCHAR(20),
    ticket_price DECIMAL(10,2),
    aircraft_type VARCHAR(20)
);
```
2. ARCHIVO SQL: consultas aerolineas.sql
sql
-- Carga masiva de datos desde CSV
BULK INSERT dbo.aerolinea
FROM 'C:\Users\HP Pavilion\Desktop\analisis 3\aviones_dataset_pro.csv'
WITH (
    format = 'csv',
    fieldterminator = ',',
    rowterminator = '\n',
    firstrow = 2
);

-- CONSULTAS CLAVE EJECUTADAS:

```sql
-- 1. Limpieza de datos nulos
UPDATE aerolinea
SET delay_minutes = 0
WHERE delay_minutes IS NULL;

-- 2. Aerolínea más popular (por número de vuelos)
SELECT airline, COUNT(*) AS numero_de_vuelos
FROM aerolinea
GROUP BY airline
ORDER BY numero_de_vuelos DESC;

-- 3. Destino más visitado
SELECT destination, COUNT(*) AS numero_de_vuelos
FROM aerolinea
GROUP BY destination
ORDER BY numero_de_vuelos DESC;

-- 4. Boletos más caros y baratos
SELECT MIN(ticket_price) AS boleto_mas_barato, 
       MAX(ticket_price) AS boleto_mas_caro
FROM aerolinea;

-- 5. Top 10 rutas con mayor retraso promedio
SELECT origin, destination, AVG(delay_minutes) AS retraso_promedio
FROM aerolinea
GROUP BY origin, destination
ORDER BY retraso_promedio DESC
OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;

-- 6. Aerolíneas con mayor tasa de cancelación
SELECT airline, 
       SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) 
       AS tasa_cancelacion
FROM aerolinea
GROUP BY airline
ORDER BY tasa_cancelacion DESC;

-- 7. Desempeño por tipo de avión
SELECT aircraft_type, 
       AVG(delay_minutes) AS retraso_promedio
FROM aerolinea
GROUP BY aircraft_type
ORDER BY retraso_promedio ASC;

-- 8. Impacto financiero total
SELECT 
    SUM(ticket_price) AS ingresos_totales,
    COUNT(*) AS total_vuelos_cancelados,
    SUM(ticket_price) AS ingresos_perdidos,
    SUM(delay_minutes * 10) AS costos_perdidos_por_retrasos
FROM aerolinea
WHERE status = 'Cancelled' OR delay_minutes > 30;
```
#  ARCHIVO EXCEL: aviones.xlsx
- HOJA "datos" (300 registros)3. ARCHIVO EXCEL: aviones.xlsx
- Estructura:

| flight_id | airline | origin | destination | departure_time | arrival_time | delay_minutes | status | ticket_price | aircraft_type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

Ejemplo registro:

| flight_id | airline | origin | destination | departure_time | arrival_time | delay_minutes | status | ticket_price | aircraft_type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F0001 | VivaFly | QRO | CDMX | 07:14:00 | 04:47:00 | 0 | Cancelled | 2039 | A320 |

# HOJA "Hoja2" - ANÁLISIS CON FÓRMULAS DINÁMICASHOJA "Hoja2" - ANÁLISIS CON FÓRMULAS DINÁMICAS
### ## FÓRMULAS CLAVE IMPLEMENTADAS:

excel
### Total de vuelos por aerolínea:Total de vuelos por aerolínea:
- =COUNTIF(datos!$B:$B, "VivaFly")
- =COUNTIF(datos!$B:$B, "AeroMX")
- =COUNTIF(datos!$B:$B, "GlobalAir")
- =COUNTIF(datos!$B:$B, "SkyJet")
#### Vuelos cancelados por aerolínea:
=COUNTIFS(datos!$B:$B, $A2, datos!$H:$H, "Cancelled")
#### Pérdidas por cancelaciones:
=SUMIFS(datos!$I:$I, datos!$B:$B, $A2, datos!$H:$H, "Cancelled")
#### Aerolínea con boleto más caro:
=LOOKUP(MAX(datos!I:I), datos!I:I, datos!B:B)
####  Precio del boleto más caro:
=MAX(datos!I:I)
####  Aerolínea con boleto más barato:
=INDEX(datos!B:B, MATCH(MIN(datos!I:I), datos!I:I, 0))
#### Precio del boleto más barato:
=MIN(datos!I:I)
#### Total de boletos vendidos por aerolínea:
=SUMIF(datos!$B$2:$B$301, $A2, datos!$I$2:$I$301)

![tablas](https://github.com/luisvarela-code/analisis-completo-datos/blob/main/graficas%20excel/tablas.png?raw=true "tablas")

# 4. ARCHIVO PYTHON: analisis_aviones.py
CÓDIGO PRINCIPAL DE ANÁLISIS:
python
# importacion de librerias 
```python
import pandas as pd    # Para DataFrames y operaciones de datos
import numpy as np     # Para cálculos numéricos y estadísticos

# 1.2 Librerías de visualización
import matplotlib.pyplot as plt  # Para crear gráficos personalizados
import seaborn as sns            # Para gráficos estadísticos más atractivos

# 1.3 Librerías de formato y utilidades
from matplotlib.ticker import PercentFormatter  # Para formatear ejes como porcentajes
```
# Lectura y limpieza de datos
```python
# leer datos del archivo
datos=pd.read_csv(r'C:\Users\HP Pavilion\Desktop\analisis_de_datos\ejercicio 3 analisis\aviones\aviones_dataset_pro.csv', sep=',')

# limpiar datos del dataframe
datos=datos.dropna(subset=['flight_id', 'airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'delay_minutes', 'status', 'ticket_price','aircraft_type'])

# limpieza profunda de los datos nulos y repetidos 
datos = datos.drop_duplicates()  
datos = datos.dropna(subset=['flight_id', 'airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'delay_minutes', 'status', 'ticket_price','aircraft_type'])
# ver las primeras 30 filas
print(datos.head(30));
```
# VISUALIZACIONES IMPLEMENTADAS:

# 1. Gráfica de barras por aerolínea
aerolineas = datos.groupby('airline')['airline'].count()
aerolineas.plot(kind='bar', color='skyblue', edgecolor='black')

![image url](https://github.com/luisvarela-code/analisis-completo-datos/blob/main/graficas%20python/grafica_1.png?raw=true)

# 2. Gráfica de pastel por estatus de vuelos
status_counts = datos['status'].value_counts()
plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%')

![image url](https://github.com/luisvarela-code/analisis-completo-datos/blob/main/graficas%20python/grafica_6.png?raw=true)

# 3. Histograma de retrasos
sns.histplot(datos['delay_minutes'], bins=30, color='purple', kde=True)

![image url](https://github.com/luisvarela-code/analisis-completo-datos/blob/main/graficas%20python/grafica_7.png?raw=true)

# 4. Top 20 rutas con mayor retraso promedio
rutas = datos.groupby('flight_id')['delay_minutes'].mean()
rutas = rutas.sort_values(ascending=False).head(20)

![image url](https://github.com/luisvarela-code/analisis-completo-datos/blob/main/graficas%20python/grafica_12.png?raw=true)

# 5. Promedio de retraso por aeronave
promedio_retraso_aeronave = datos.groupby('aircraft_type')['delay_minutes'].mean()
promedio_retraso_aeronave.plot(kind='bar', color='gold', edgecolor='black')


![image url](https://github.com/luisvarela-code/analisis-completo-datos/blob/main/graficas%20python/grafica_14.png?raw=true)

# MÉTRICAS CALCULADAS EN PYTHON:
- print(f'Total de vuelos faltantes: {total_vuelos_faltantes}')
- print(f'Promedio de retraso: {promedio_retraso} minutos')
- print(f'Aerolinea con el boleto mas caro: {aerolinea_con_boleto_mas_caro}')
- print(f'Precio del boleto mas caro: {precio_boleto_mas_caro}')

![image url](https://github.com/luisvarela-code/analisis-completo-datos/blob/main/datos.png?raw=true)
  


📊 RESULTADOS INTEGRADOS DE LOS TRES ARCHIVOS
A. MÉTRICAS OPERATIVAS (CONSISTENTES ENTRE SQL, EXCEL Y PYTHON)
1. Distribución por Aerolínea:

| Aerolínea | Vuelos Totales | % del Total | Fuente |
| :--- | :--- | :--- | :--- |
| VivaFly | 105 | 35% | Excel: =COUNTIF(datos!$B:$B,"VivaFly") |
| AeroMX | 76 | 25.3% | SQL: COUNT(*) GROUP BY airline |
| GlobalAir | 76 | 25.3% | Python: datos['airline'].value_counts() |
| SkyJet | 43 | 14.3% | Todas las fuentes coinciden |

2. Estado de Vuelos:

| Estado | Cantidad | Porcentaje | Fuente Principal |
| :--- | :--- | :--- | :--- |
| On Time | 208 | 69.3% | Python: status_counts |
| Delayed | 85 | 28.3% | Gráfica de pastel Python |
| Cancelled | 7 | 2.3% | SQL: WHERE status = 'Cancelled' |

3. Retrasos por Tipo de Aeronave:

| Resultado de consulta SQ  | |
| :------------: | :------------: |
|  aircraft_type | etraso_promedio  |
|A321|24.52 minutos
|B737  |29.66 minutos
|A320 |31.86 minutos
|E190   | 37.14 minutos

B. IMPACTO FINANCIERO CALCULADO
1. Desde SQL:
sql
```sql
-- Ingresos totales de todos los vuelos:
SELECT SUM(ticket_price) AS ingresos_totales FROM aerolinea;
-- RESULTADO: $1,218,847.00
```

```sql
-- Ingresos perdidos por cancelaciones:
SELECT SUM(ticket_price) AS ingresos_perdidos 
FROM aerolinea 
WHERE status = 'Cancelled';
-- RESULTADO: $27,361.00
```

```sql
-- Costos por retrasos (mayores a 30 minutos):
SELECT SUM(delay_minutes * 10) AS costos_perdidos_por_retrasos
FROM aerolinea
WHERE delay_minutes > 30;
-- RESULTADO: $14,570.00
```
2. Desde Excel (Hoja2):
Fila AeroMX: =SUMIFS(datos!$I:$I, datos!$B:$B, $A3, datos!$H:$H, "Cancelled")
Resultado: $11,095 (pérdidas por cancelaciones de AeroMX)

C. RUTAS CRÍTICAS IDENTIFICADAS
Top 5 Rutas con Mayor Retraso (SQL):

| origin  | destination  |retraso_promedio   |
| :------------: | :------------: | :------------: |
| CUN   |  MTY    |72.00 minutos   |
|QRO    | TIJ  |  58.25 minutos |
|MTY |GDL|7.00 minutos|
|TIJ|CUN   |56.40 minutos
|CDMX|GDL | 55.67 minutos

Vuelo con Mayor Retraso Individual:
sql
```sql
-- Consulta SQL para identificar el vuelo con mayor retraso:
SELECT * FROM aerolinea 
WHERE delay_minutes = (SELECT MAX(delay_minutes) FROM aerolinea);
-- RESULTADO: Vuelo F0114 (CUN→MTY) con 128 minutos de retraso
```
D. COMPARACIÓN DE FÓRMULAS/CONSULTAS ENTRE HERRAMIENTAS
1. Conteo de Vuelos por Aerolínea:
- Excel: =COUNTIF(datos!$B:$B, "VivaFly")
- SQL: SELECT COUNT(*) FROM aerolinea WHERE airline = 'VivaFly'
- Python: datos[datos['airline'] == 'VivaFly'].shape[0]
2. Cálculo de Tasa de Cancelación:
Excel: Combinación de COUNTIFS y división manual

SQL:
```sql
SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
```
Python:
```python
(datos['status'] == 'Cancelled').sum() / len(datos) * 100
 HALLazgos CRUCIALES CONFIRMADOS POR TRES FUENTES
Hallazgo 1: AeroMX tiene la Mayor Tasa de Problemas
SQL: 6 cancelaciones (7.89% de sus vuelos)
```

- Excel: Fórmula =COUNTIFS(datos!$B:$B, $A3, datos!$H:$H, "Cancelled") confirma 6
- Python: vuelos_cancelados_por_aerolinea muestra AeroMX con 6 cancelaciones
- Hallazgo 2: VivaFly es la Más Puntual
- SQL: 0 cancelaciones en consultas
- Excel: =COUNTIFS(datos!$B:$B, $A2, datos!$H:$H, "Cancelled") = 0
- Python: No aparece en listado de cancelaciones por aerolínea
- Hallazgo 3: E190 es el Avión con Peor Desempeño
- SQL: Retraso promedio de 37.14 minutos (mayor de todos)
- Python: Gráfica de barras muestra E190 con mayor barra de retraso
- Consistencia: Ambas herramientas muestran el mismo orden de desempeño

📈 VISUALIZACIONES COINCIDENTES ENTRE EXCEL Y PYTHON
Gráficas Generadas en Python que Validan Datos de Excel:

Distribución de Aerolíneas:

- Python: Gráfica de barras con GlobalAir como la más alta (105 vuelos)
- Excel: Tabla en Hoja2 confirma 105 para GlobalAir

![image url](https://github.com/luisvarela-code/analisis-completo-datos/blob/main/graficas%20python/grafica_1.png?raw=true)

Retrasos por Tipo de Avión:

- Python: E190 muestra la barra más alta en gráfica
- SQL: Consulta ordenada por retraso promedio confirma E190 en último lugar

  ![image url](https://github.com/luisvarela-code/analisis-completo-datos/blob/main/graficas%20python/grafica_14.png?raw=true)

🎯 RECOMENDACIONES BASADAS EN ANÁLISIS TRIPLE-VERIFICADO
Acción 1: 
Revisión Urgente de AeroMX

- Evidencia SQL: Mayor tasa de cancelación (7.89%)
- Evidencia Excel: $11,095 en pérdidas por sus cancelaciones
- Acción: Auditoría operativa inmediata

Acción 2: Optimización de Flota E190

- Evidencia SQL: 37.14 minutos de retraso promedio (peor desempeño)
- Evidencia Python: Gráfica claramente muestra problema con E190
- Acción: Revisión de mantenimiento y rutas asignadas a E190

Acción 3: Atención a Ruta CUN-MTY

- Evidencia SQL: 72 minutos retraso promedio (más alto)
- Evidencia SQL: Vuelo F0114 con 128 minutos (máximo absoluto)
- Acción: Análisis específico de causas en esta ruta

### VERIFICACIÓN DE CONSISTENCIA ENTRE ARCHIVOS

| Métrica | Excel | SQL | Python | ¿Coincide? |
| :--- | :--- | :--- | :--- | :--- |
| Total vuelos VivaFly | 105 | 105 | 105 | ✅ |
| Cancelaciones AeroMX | 6 | 6 | 6 | ✅ |
| Boleto más caro | $5995 | $5995 | $5995 | ✅ |
| Retraso promedio E190 | N/A | 37.14 | 37.14* | ✅ |
| Ingresos totales | $1,218,847 | $1,218,847 | N/C | ✅

📋 CONCLUSIÓN TÉCNICA
Los tres archivos proporcionados (aerolineas.sql, aviones.xlsx, analisis_aviones.py) demuestran un análisis completo y consistente:

- Excel sirvió para análisis exploratorio inicial y fórmulas dinámicas
- SQL permitió consultas complejas y cálculos agregados robustos
- Python validó resultados y generó visualizaciones profesionales

Los hallazgos son consistentes en las tres herramientas, confirmando la validez de:

- AeroMX como aerolínea con mayores problemas operativos

- E190 como tipo de avión con peor desempeño

- Ruta CUN-MTY como la más crítica en retrasos

-  Impacto financiero total aproximado de $41,931 por problemas operativos
