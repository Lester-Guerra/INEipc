# from sqline import sqlINE
from typing import List, Tuple

from funcionesjo import mes_anio_by_abreviacion, mes_by_ordinal


class Descriptor:
    def __init__(self, anio: int, mes: int, var_mensual: int) -> None:
        self.mes = mes
        self.anio = anio
        self.region = dict(zip(range(1,9), ('I','II','III','VI','V','VI','VII','VIII')))
        self.__notaReg = '''\\footnote{Guatemala se encuentra organizada en 8
                            regiones; La región I o Metropolitana está conformada
                            por el departamento de Guatemala, la región II o Norte
                            por Alta Verapaz y Baja Verapaz, la región III o Nororiental
                            por Chiquimula, El Progreso, Izabal y Zacapa, la región
                            IV o Suroriental por Jutiapa, Jalapa y Santa Rosa,
                            la región V o Central por Chimaltenango, Sacatepéquez
                            y Escuintla, la región VI o Suroccidental por Quetzaltenango,
                            Retalhuleu, San Marcos, Suchitepéquez, Sololá y Totonicapán,
                            la región VII o Noroccidental por Huehuetenango y
                            Quiché y la región VIII por Petén.}'''
        # signo de la variación mensual
        self.signo_var_mensual = True if var_mensual >= 0 else False

    def retocar_plantilla(self, plantilla: str) -> str:
        plantilla = plantilla.replace("\n", " ")
        plantilla = plantilla.split()
        plantilla = " ".join(plantilla)
        return plantilla

    def variacion(self, dato: float, dato_antes: float) -> float:
        """
        Calcula la variación porcentual entre dos valores numéricos.

        Args:
        dato (float): Valor actual.
        dato_antes (float): Valor anterior.

        Returns:
        float: Variación porcentual entre los dos valores.
        """
        return ((dato - dato_antes) / dato_antes) * 100

    def indice_precio_alimentos(self, datos: List[Tuple[str]], precision: int=2) -> str:
        """
        Genera un texto con la información del índice de precios de los alimentos.

        Parameters
        ----------
            datos (List[Tuple[str, float]]): Lista de tuplas que contiene información de fecha y precio.

        Returns
        ----------
            str: Texto con la información del índice de precios de los alimentos.
        """
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        fecha_2 = mes_anio_by_abreviacion(datos[0][0], mmaa=True)
        fecha_3 = mes_anio_by_abreviacion(datos[-2][0], mmaa=True)
        indice = datos[-1][1]
        variacion_1 = self.variacion(datos[-1][1], datos[0][1])
        variacion_2 = self.variacion(datos[-1][1], datos[-2][1])
        nota_1 = '''\\footnote{El índice de precios de los alimentos de la FAO es una medida
                    de la variación mensual de los precios internacionales de
                    una canasta de productos alimenticios. Consiste en el promedio
                    de los índices de precios de cinco grupos de productos básicos,
                    ponderado con las cuotas medias de exportación de cada uno
                    de los grupos para 2002-2004.}'''
        nota_2 = '''\\footnote{Organización de las Naciones Unidas para la
                    Alimentación y la Agricultura.}'''
        plantilla = f"""El índice de precios de los alimentos{nota_1} de la FAO{nota_2} registró en
                    {fecha_1} un índice de {indice:,.{precision}f}, lo que representa una
                    variación de {variacion_1:,.{precision}f}% respecto a {fecha_2} y de
                    {variacion_2:,.2f}% respecto a {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    def petroleo(self, datos: List[Tuple[str, float]], precision: int=2) -> str:
        """
        Función que recibe una lista de tuplas con datos del precio del petróleo y
        devuelve una cadena de texto formateada con la información correspondiente.

        Parameters
        ----------
            datos: Lista de tuplas con los datos del precio del petróleo. Cada
            tupla contiene una cadena con la abreviatura del mes y el año
            correspondiente (por ejemplo, "Ene 2022") y un valor float con
            el precio del petróleo en dólares por barril.
        
        Returns
        ----------
            Cadena de texto con la información del precio del petróleo formateada.
        """
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        fecha_3 = mes_anio_by_abreviacion(datos[-2][0])
        PRECIO = datos[-1][1]
        diferencia_1 = datos[-1][1] - datos[0][1]
        variacion_1 = self.variacion(datos[-1][1], datos[0][1])
        if diferencia_1 > 0:
            signo_1 = ""
        else:
            diferencia_1 = diferencia_1 * -1
            signo_1 = "-"
        diferencia_2 = datos[-1][1] - datos[-2][1]
        variacion_2 = self.variacion(datos[-1][1], datos[-2][1])
        if diferencia_2 > 0:
            signo_2 = ""
        else:
            diferencia_2 = diferencia_2 * -1
            signo_2 = "-"
        nota = """\\footnote{Se refiere al crudo West Texas Intermediate (WTI)
                    producido en Texas y el sur de Oklahoma}"""
        plantilla = f"""El precio internacional del petróleo{nota} registró en {fecha_1}
                    un precio medio de US${PRECIO:,.{precision}f} por barril, lo que representa
                    una variación de {variacion_1:,.{precision}f}% ({signo_1}US${diferencia_1:,.{precision}f})
                    respecto a {fecha_2} y de {variacion_2:,.{precision}f}% ({signo_2}US${diferencia_2:,.{precision}f})
                    respecto a {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    def cambio_del_quetzal(self, datos: List[Tuple[str, float]], precision: int=2) -> str:
        """
        Retorna un string con información sobre el tipo de cambio del quetzal
        guatemalteco respecto al dólar estadounidense.

        Parameters
        ----------
        datos : list of tuple of str and float
            Una lista de tuplas con información sobre el tipo de cambio. Cada tupla
            contiene una cadena con la abreviación del mes y el año (por ejemplo, "Ene 2022")
            y un valor float con el tipo de cambio en quetzales por dólar estadounidense.

        Returns
        -------
        str
            Un string con información sobre el tipo de cambio.
        """
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        fecha_3 = mes_anio_by_abreviacion(datos[-2][0])
        PRECIO = datos[-1][1]
        variacion_1 = self.variacion(datos[-1][1], datos[0][1])
        variacion_2 = self.variacion(datos[-1][1], datos[-2][1])
        nota = """\\footnote{El tipo de cambio de referencia lo calcula el Banco
                    de Guatemala con la información que las instituciones que
                    constituyen el Mercado Institucional de Divisas le proporcionan,
                    relativa al monto de divisas compradas y al monto de divisas
                    vendidas y sus respectivas equivalencias en moneda nacional.}"""
        plantilla = f"""El tipo de cambio de referencia{nota} del quetzal respecto al dólar
                    de los Estados Unidos de América, registró en {fecha_1} un tipo de cambio
                    promedio de Q{PRECIO:,.{precision}f} por US$1.00, lo que representa una variación
                    de {variacion_1:,.{precision}f}% respecto a {fecha_2} y de {variacion_2:,.{precision}f}%
                    respecto a {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    def tasa_de_interes(self, datos: List[Tuple[str, float]], precision: int=2) -> str:
        """
        Retorna un string con información sobre la tasa de interés activa en
        moneda nacional.

        Parameters
        ----------
        datos : list of tuple of str and float
            Una lista de tuplas con información sobre la tasa de interés activa.
            Cada tupla contiene una cadena con la abreviación del mes y el año
            (por ejemplo, "Ene 2022") y un valor float con la tasa de interés
            activa en porcentaje.

        Returns
        -------
        str
            Un string con información sobre la tasa de interés activa.
        """
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        fecha_3 = mes_anio_by_abreviacion(datos[-2][0])
        tasa = datos[-1][1]
        diferencia_1 = datos[-1][1] - datos[0][1]
        diferencia_2 = datos[-1][1] - datos[-2][1]
        if diferencia_1 < 0:
            cambio_1 = "una disminución"
            diferencia_1 *= -1
        elif diferencia_1 > 0:
            cambio_1 = "un aumento"
        else:
            cambio_1 = "un cambio"
        if diferencia_2 < 0:
            cambio_2 = "una disminución"
            diferencia_2 *= -1
        elif diferencia_2 > 0:
            cambio_2 = "un aumento"
        else:
            cambio_2 = "un cambio"
        nota = """\\footnote{Es el porcentaje que las instituciones bancarias,
                    de acuerdo con las condiciones de mercado y las disposiciones
                    del banco central, cobran por los diferentes tipos de servicios
                    de crédito a los usuarios de los mismos.}"""
        plantilla = f"""El promedio ponderado preliminar de la tasa de interés activa{nota}
                    en moneda nacional se ubicó en {fecha_1} en {tasa:,.{precision}f}%,
                    representa {cambio_1} de {diferencia_1:,.{precision}f} puntos porcentuales
                    respecto a {fecha_2} y {cambio_2} de {diferencia_2:,.{precision}f} puntos
                    porcentuales respecto a {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    # IPC USA
    """
    ejemplo de datos
    ('2021-Ago', 5.205331689652515)
    ('2021-Sep', 5.389907375379521)
    ...
    ('2022-May', 8.516412942713858)
    ('2022-Jun', 8.995220608588127)
    """
    def ipc_usa(self, datos: list[tuple[str]], precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        indice_1 = datos[-1][1]
        indice_2 = datos[0][1]
        diferencia = datos[-1][1] - datos[0][1]
        if diferencia < 0:
            cambio = "se desaceleró"
            diferencia *= -1
        elif diferencia > 0:
            cambio = "se aceleró"
        else:
            cambio = "cambio"
        nota = """\\footnote{Para mayor información sobre el indice de precios
                    al consumidor de los Estados Unidos, visite
                    \\url{http://www.bls.gov/cpi}.}"""
        plantilla = f"""El Índice de Precios al Consumidor en los Estados Unidos de
                    América{nota} registró una variación interanual al mes de {fecha_1} de
                    {indice_1:,.{precision}f}%. En {fecha_2} la variación interanual se ubicó en
                    {indice_2:,.{precision}f}%, por lo que este indicador {cambio} {diferencia:,.{precision}f}
                    puntos porcentuales en el último año."""
        return self.retocar_plantilla(plantilla)

    # IPC MEX
    """
    ejemplo de datos
    ('2021-Ago', 5.205331689652515)
    ('2021-Sep', 5.389907375379521)
    ...
    ('2022-May', 8.516412942713858)
    ('2022-Jun', 8.995220608588127)
    """
    def ipc_mex(self, datos: list[tuple[str]], precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        indice_1 = datos[-1][1]
        indice_2 = datos[0][1]
        diferencia = datos[-1][1] - datos[0][1]
        if diferencia < 0:
            cambio = "se desaceleró"
            diferencia *= -1
        elif diferencia > 0:
            cambio = "se aceleró"
        else:
            cambio = "cambio"
        nota = """\\footnote{Para mayor información sobre el índice de precios
                    al consumidor en México, visite \\url{http://www.inegi.org.mx}.}"""
        plantilla = f"""El Índice de Precios al Consumidor en México{nota} se registró una
                    variación interanual al mes de {fecha_1} de {indice_1:,.{precision}f}%. En
                    {fecha_2} la variación interanual se ubicó en {indice_2:,.{precision}f}%,
                    por lo que este indicador {cambio} {diferencia:,.{precision}f} puntos
                    porcentuales en el último año."""
        return self.retocar_plantilla(plantilla)

    def inflacion(self, datos, mes, anio, precision: int=2) -> str:
        inflacion_mes = [(i[2], i[0]) for i in datos[1::]]
        inflacion_mes.sort()
        INFLACION_MIN = inflacion_mes[0]
        INFLACION_MAX = inflacion_mes[-1]
        plantilla = f"""Para el mes de {mes} {anio}, en Centro América, República
                    Dominicana y México, {INFLACION_MAX[1]} presentó
                    la mayor tasa de inflación interanual de {INFLACION_MAX[0]:,.{precision}f}%,
                    mientras que {INFLACION_MIN[1]} registró la tasa más
                    baja con un nivel de {INFLACION_MIN[0]:,.{precision}f}%."""
        return self.retocar_plantilla(plantilla)

    def serie_historica_ipc(self, datos, QGba: bool=False, QReg: bool=False, precision: int=2) -> str:
        if QGba:
            gba = f'índice del gasto basico {datos[0].lower()}'
            datos = datos[1]
        elif QReg:
            gba = 'número índice'
        else:
            gba = 'Índice de Precios al Consumidor'
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        fecha_2 = mes_anio_by_abreviacion(datos[0][0], mmaa=True)
        if datos[-1][0].split('-')[0] == datos[0][0].split('-')[0]:
            Qmismo_anio = False
        else:
            Qmismo_anio = True
        if Qmismo_anio:
            plantilla_aux = f'{fecha_2}'
        else:
            plantilla_aux = 'el mismo mes del año anterior'

        indice_1 = datos[-1][1]
        indice_2 = datos[0][1]
        diferencia = indice_1 - indice_2
        if diferencia > 0:
            cambio = "mayor"
            diferencia *= -1
        elif diferencia < 0:
            cambio = "menor"
        else:
            cambio = "igual"
        plantilla = f"""El {gba} a {fecha_1} se ubicó en
                    {indice_1:,.{precision}f}, {cambio} a lo observado en {plantilla_aux}
                    ({indice_2:,.{precision}f})."""
        return self.retocar_plantilla(plantilla)

    # tipo = intermensual, interanual, acumulada
    def serie_historica_inflacion(self, datos, tipo: str, nivel: str='a nivel nacional', Qmensual: bool=True, precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        fecha_2 = mes_anio_by_abreviacion(datos[0][0], mmaa=True)
        indice_1 = datos[-1][1] # mes actual
        indice_2 = datos[-2][1] # mes anterior
        indice_3 = datos[0][1]
        diferencia_1 = indice_1 - indice_2
        diferencia_2 = indice_1 - indice_3
        if diferencia_1 > 0:
            cambio_1 = "una aceleración"
        elif diferencia_1 < 0:
            cambio_1 = "una desaceleración"
            diferencia_1 *= -1
        else:
            cambio_1 = "un cambio"
        if diferencia_2 > 0:
            cambio_2 = "una aceleración"
        elif diferencia_2 < 0:
            cambio_2 = "una desaceleración"
            diferencia_2 *= -1
        else:
            cambio_2 = "un cambio"
        if tipo == "interanual":
            plantilla = f"""La variación {tipo} del índice {nivel} en {fecha_1},
                        se ubicó en {indice_1:,.{precision}f}%. Esta variación representa {cambio_1}
                        en el nivel de aumento de los precios de {diferencia_1:,.{precision}f} puntos porcentuales
                        respecto al mes anterior ({indice_2:,.{precision}f}%), y con respecto a la
                        variación alcanzada en {fecha_2} ({indice_3:,.{precision}f}%) {cambio_2} de
                        {diferencia_2:,.{precision}f} puntos."""
        elif tipo == "acumulada":
            fecha_2 = mes_anio_by_abreviacion(datos[-2][0], mmaa=True)
            indice_3 = datos[-2][1]
            plantilla = f"""La variación {tipo} del índice {nivel} en {fecha_1},
                        se ubicó en {indice_1:,.{precision}f}%. La de {fecha_2} se
                        presentó en {indice_3:,.{precision}f}%."""
        else:
            plantilla = f"""La variación {tipo} del índice {nivel} en {fecha_1},
                        se ubicó en {indice_1:,.{precision}f}%. Esta variación representa {cambio_1}
                        en el ritmo de crecimiento de los precios de {diferencia_1:,.{precision}f} puntos porcentuales
                        respecto al mes anterior ({indice_2:,.{precision}f}%), y la de {fecha_2} se
                        presentó en {indice_3:,.{precision}f}%."""
        return self.retocar_plantilla(plantilla)

    def incidencias(self, datos, fecha: str, Qpositivas: bool=True) -> str:
        datos = sorted(datos, reverse=Qpositivas)[0:5]
        if Qpositivas:
            indices = [d[0] for d in datos]
            tipo = 'variaciones'
        else:
            indices = [d[0]*-1 for d in datos]
            tipo = 'variaciones negativas'
        nombres = [d[1].lower() for d in datos]
        plantilla = """Los gastos básicos que registraron mayor alza porcentual mensual
                    en {} fueron: {}, {}, {}, {} y {} todo incluido al exterior con
                    {} de {:,.2f}%, {:,.2f}%, {:,.2f}%, {:,.2f}% y {:,.2f}%,
                    respectivamente.""".format(fecha, *nombres, tipo, *indices)
        return self.retocar_plantilla(plantilla)

    def poder_adquisitivo(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        indice_1 = datos[-1][1]
        perdida = 1 - indice_1
        plantilla = f"""El quetzal ha perdido {perdida:,.2f} centavos en poder adquisitivo
                    respecto a diciembre de 2010, esto es, un quetzal de diciembre 2010 es
                    equivalente a {indice_1:,.2f} centavos de {fecha_1}."""
        return self.retocar_plantilla(plantilla)

    def serie_fuentes(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], mmaa=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], mmaa=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""La cantidad de fuentes consultadas en {fecha_1} es de {indice_1:,}.
                    La mayor cantidad de fuentes consultadas fue en el mes de {fecha_2}
                    con una cantidad de {indice_2:,} y la menor se encuentra en el mes
                    de {fecha_3} con una cantidad de {indice_3:,}."""
        return self.retocar_plantilla(plantilla)

    def serie_precios(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], mmaa=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], mmaa=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""La cantidad de precios diligenciados en {fecha_1} es de {indice_1:,}.
                    La mayor cantidad de precios diligenciados fue en el mes de {fecha_2}
                    con una cantidad de {indice_2:,} y la menor se encuentra en el mes
                    de {fecha_3} con una cantidad de {indice_3:,}."""
        return self.retocar_plantilla(plantilla)

    def imputacion_precios(self, datos, precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], mmaa=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], mmaa=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""El porcentaje de precios imputados en {fecha_1} es de {indice_1:.{precision}f}%.
                    El mayor porcentaje de imputaciones fue en el mes de {fecha_2}
                    con una cantidad de {indice_2:.{precision}f}% y el menor se encuentra en el mes
                    de {fecha_3} con una cantidad de {indice_3:.{precision}f}%."""
        return self.retocar_plantilla(plantilla)

    def incidencia_divisiones(self, datos) -> str:
        datos = sorted(datos, reverse=True)
        maximo1 = datos[0]
        maximo2 = datos[1]
        minimo = datos[-1]
        if self.signo_var_mensual:
            plantilla = f"""De las doce divisiones de gasto que integran
                        el IPC, la de {maximo1[1].lower()} ({round(maximo1[0], 2):,.2f}%) y
                        {maximo2[1].lower()} ({round(maximo2[0], 2):,.2f}%), registraron la mayor
                        incidencia mensual positiva. Por su parte, {minimo[1].lower()} es la división
                        de gasto con menor incidencia mensual negativa ({round(minimo[0], 2):,.2f}%)."""
        else:
            plantilla = f"""De las doce divisiones de gasto que integran
                        el IPC, la de {minimo[1].lower()} es la división
                        de gasto con menor incidencia mensual negativa ({round(minimo[0], 2):,.2f}%). 
                        Por su parte, {maximo1[1].lower()} ({round(maximo1[0], 2):,.2f}%) y
                        {maximo2[1].lower()} ({round(maximo2[0], 2):,.2f}%), registraron la mayor
                        incidencia mensual positiva."""
        return self.retocar_plantilla(plantilla)

    def cobertura_fuentes(self, datos) -> str:
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        region = dict(zip(range(1,9), ('I','II','III','VI','V','VI','VII','VIII')))
        plantilla = f"""En el mes de {mes} {self.anio} la región{self.__notaReg} {region[maximo[0]]}
                    fue donde más fuentes fueron consultadas con un total de
                    {maximo[1]:,} y la región {region[minimo[0]]} fue donde menos fuentes
                    fueron consultadas con un total de {minimo[1]:,}."""
        return self.retocar_plantilla(plantilla)

    def desagregacion_fuentes(self, datos, mes_ordinal, precision: int=2) -> str:
        mes = mes_by_ordinal(mes_ordinal, abreviado=False).lower()
        maximo = datos[0][1]
        fuente_max = datos[0][0].lower()
        minimo = datos[1][1]
        fuente_min = datos[1][0].lower()
        plantilla = f"""En el mes de {mes} el tipo de fuente más consultado fue
                    {fuente_max} ({maximo:,.{precision}f}%), y el segundo más consultado fue
                    {fuente_min} ({minimo:,.{precision}f}%)."""
        return self.retocar_plantilla(plantilla)

    def cobertura_precios(self, datos):
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        plantilla = f"""En el mes de {mes} {self.anio} la región{self.__notaReg} {self.region[maximo[0]]}
                    fue donde más precios fueron diligenciados con un total de
                    {maximo[1]:,} y la región {self.region[minimo[0]]} fue donde menos precios
                    fueron diligenciados con un total de {minimo[1]:,}."""
        return self.retocar_plantilla(plantilla)

    def ipc_regiones(self, datos, precision: int=2):
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        plantilla = f"""En el mes de {mes} del año {self.anio}, la región{self.__notaReg} {self.region[maximo[0]]}
                    presentó el mayor índice de precios al consumidor, el cual fue
                    de {maximo[1]:,.{precision}f}, mientras que la región {self.region[minimo[0]]}
                    presentó el índice más bajo, de {minimo[1]:,.{precision}f}"""
        return self.retocar_plantilla(plantilla)

    def inflacion_interanual_regiones(self, datos, precision: int=2):
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        plantilla = f"""En el mes de {mes} del año {self.anio}, la región{self.__notaReg}
                    {self.region[maximo[0]]} presentó la mayor variación interanual,
                    la cual fue de {maximo[1]:,.{precision}f}, mientras que la región
                    {self.region[minimo[0]]} presentó la menor variación interanual,
                    de {minimo[1]:,.{precision}f}"""
        return self.retocar_plantilla(plantilla)

    def incidencias_gba(self, datos, Qpositiva: bool = True):
        if Qpositiva:
            signo = 'positiva'
        else:
            signo = 'negativa'
        textos = []
        for d in datos:
            gba = d[0]
            indice = d[1]
            tx = f"{gba} ({indice:,.2f}%)"
            textos.append(tx)
        plantilla = """Los cinco principales gastos básicos que
                    registran la mayor incidencia {} mensual
                    se encuentran: {}, {}, {}, {} y {}.""".format(signo, *textos)
        return self.retocar_plantilla(plantilla)

    def serie_historica(self, tipo: str) -> str:
        """
        Genera el texto de la serie histórica de IPC, inflación interanual o
        variación mensual.
        Parámetros
        ----------
        tipo: str
            Tipo de serie. Puede ser 'ipc', 'anual' o 'mensual'.
            
        Retorna
        -------
        str
            Texto de la serie histórica.
            
        Excepciones
        -----------
        ValueError
            Si el tipo de serie no es reconocido.  
        """
        if tipo == 'ipc':
            titulo = 'del Índice de precios al consumidor'
        elif tipo == 'anual':
            titulo = 'ritmo inflacionario'
        elif tipo == 'mensual':
            titulo = 'de la variación mensual'
        else:
            raise ValueError('Tipo de serie no reconocido')
        plantilla = """En la siguiente gráfica se presenta la serie histórica
                    {} desde el inicio de la base (diciembre de 2010).""".format(titulo)
        return self.retocar_plantilla(plantilla)

    def tabla_serie_historica(self) -> str:
        """
        Genera el texto de la tabla de la serie histórica de IPC, inflación
        interanual o variación mensual.
        Retorna
        -------
        str
            Texto de la tabla de la serie histórica.
        """
        plantilla = """En la siguiente tabla se presenta la serie histórica
                    del ritmo inflacionario, variación mensual e Índice de precios
                    al consumidor desde el inicio de la base (diciembre de 2010)."""
        return self.retocar_plantilla(plantilla)
    
    def serie_historica_mensual_inflacion(self, datos, tipo: str, nivel: str='a nivel nacional', precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        fecha_2 = mes_anio_by_abreviacion(datos[-2][0], mmaa=True)
        indice_1 = datos[-1][1] # mes actual
        indice_2 = datos[-2][1] # mes anterior
        
        plantilla = f"""La variación {tipo} del índice {nivel} en {fecha_1},
                    se ubicó en {indice_1:,.{precision}f}%. La de {fecha_2} se
                    presentó en {indice_2:,.{precision}f}%."""

        return self.retocar_plantilla(plantilla)