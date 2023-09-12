### Carga de históricos en LOTBA


### Notas

- Ataca la BBDD en local, activando el tunel

#### Bugs y feature request
- Anyadir una tabla de log de los procesos de carga, que guarde cuando, cuanto ha tardado y si fallo
- Tengo que repensar la logica de comportamiento.

### Dvp Log
- RUD_D 202205 - 6 ficheros. 1 fichero repetido 5 veces
    Campos que faltan:
        - Mes ????
        - FVDocumental
- RUD_D 202206 - 16 ficheros. 2 fichero repetido 2 veces
- RUD_D 202205 - 47 ficheros. 2 fichero repetido 2 veces
##### 29mar23
###### RUD_D
- AJL0005_AJL0005_SCI_RU_RUD_D_20220704_ALI13375.xml	3.316	10.340 	ERROR RUD_D.insertJugadoresRud(): Column 'FechaNacimiento' cannot be null
- AJL0005_AJL0005_SCI_RU_RUD_D_20220705_ALI14253.xml	802	2.274 	ERROR RUD_D.insertJugadoresRud(): Column 'FechaNacimiento' cannot be null
  - jugador 24048 defectuoso
- Duplicados controlados pero no sale el error en la pagina.
  - 202207 Ya carga todo. Cuenta bien
  - 202209 Carga todo. Cuenta bien en 2'4"
  - 202210 Carga todo. Cuenta bien en 2'1"
  - 202211 Carga todo, cuenta bien: 16.235	66.137 en 3'19"
  - 202212 Carga todo, cuenta bien:  8718 Jugadores 51056 en 2'11"
- Procedo a cargar todos los meses para ver que no hay fallo.
  - 202301 7034 Jugadores 52014 en 2'2"
  - 202302 10067 Jugadores 55065 en 2'15"
  - 202303 12266 Jugadores 45202 en 2'7"
  - 202205 589 Jugadores 1836 en 16"
  - 202206 4604 Jugadores 13823 en 59"
  - 202207 11968 Jugadores 44433 en 3'8"
  - 202208 4262 Jugadores 24966 en 1'14"
  - 202210 8775 Jugadores 48035 en 2'
  - 202209 8904 Jugadores 41611 en 2'6"
  - 202211 16235 Jugadores 66137 en 2'56"
  - 202212 8718 Jugadores 51056 en 2'10"
  - 202301 7034 Jugadores 52014 en 2'5"
  - Con esto completo la carga de todos los XML (no repetidos) de RUD_D
###### RUD_M
- Depurar la carga
  - 220206 Falla por duplicados y ademas es supercostoso de cargar (uno solo de los ficheros tarda 1'4" en cargarse)
  - Implemento el control de duplicados para la carga del mes y testeo sin insertar (son 14 ficheros, le puede llevar 15 minutos)
  - 220206 Carga bien, cuenta mal 139998 Jugadores in RUD_M XML for 202206: 0:12:57
  - 220210 68.119	156.168 en 8'9"
##### 30mar23
###### RUD_M
  - 220212 12 xml 60.000    134.618 en 23'16"
  - 202301 12 xml 60.000	134.630 en 14'35"
  - 202208 21 xml 0 0 19'32"
    - Lo reintento
  - 202208 21 xml 56.027	127.530 en 18'58"
  - 202209 21 xml 62.177	141.932 en 18'32"
  - 202211  8 xml 77.014	175.579 en 8'33"
  - 202302  7 xml 70.000	156.290 en 7'24"
  - 202207 52 xml 53.914	121.230 en 46'18"
  - Con esto completo la carga de todos los XML (no repetidos) de RUD_M
###### RUT_D
  - Sigo con la implementacion basica