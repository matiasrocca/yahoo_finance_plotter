import unittest
from yahoo_finance_plotter import *


# Para testear cada una de las funciones del ejercicio 5, definimos un set de valores que nos parecía adecuado
# para los rendimientos y un set de valores para las fechas de esos rendimientos. 
# Una vez que definíamos esto, hicimos una versión del test usando assertEqual y assertNotEqual que nos debería dar OK.
# Luego otra versión del test usando los mismos métodos que nos debería dar FAIL. 
# Repetimos este proceso para cada una de las funciones del ejercicio 5. 
class Test(unittest.TestCase):

  def test_dias_positivos_consecutivos_v1(self):
    rendimientos = [2,0.1,-0.5,1.3,0.85,0.2,0.44,-0.01,-0.005,3]
    fechas = ["2021-01-05", "2021-01-06", "2021-01-07", "2021-01-08", "2021-01-09", "2021-01-10", "2021-01-11", "2021-01-12", "2021-01-13", "2021-01-14"]

    self.assertEqual(dias_consecutivos_positivos(rendimientos, fechas), ["2021-01-08","2021-01-12"])
    self.assertNotEqual(dias_consecutivos_positivos(rendimientos, fechas), ["2021-01-10","2021-01-14"])

  def test_dias_positivos_consecutivos_v2(self):
    rendimientos = [0.5,0.3,0.1,-0.3,-0.4,0.1,2,-1,1,-0.2]
    fechas = ["2021-01-05", "2021-01-06", "2021-01-07", "2021-01-08", "2021-01-09", "2021-01-10", "2021-01-11", "2021-01-12", "2021-01-13", "2021-01-14"]

    self.assertEqual(dias_consecutivos_positivos(rendimientos, fechas), ["2021-01-08","2021-01-12"])
    self.assertNotEqual(dias_consecutivos_positivos(rendimientos, fechas), ["2021-01-05","2021-01-08"])


  def test_dias_negativos_consecutivos_v1(self):
    rendimientos = [2,0.1,-0.5,1.3,0.85,0.2,0.44,-0.01,-0.005,3]
    fechas = ["2021-01-05", "2021-01-06", "2021-01-07", "2021-01-08", "2021-01-09", "2021-01-10", "2021-01-11", "2021-01-12", "2021-01-13", "2021-01-14"]

    self.assertEqual(dias_consecutivos_negativos(rendimientos, fechas), ["2021-01-12","2021-01-14"])
    self.assertNotEqual(dias_consecutivos_negativos(rendimientos, fechas), ["2021-01-10","2021-01-14"])

  def test_dias_negativos_consecutivos_v2(self):
    rendimientos = [0.5,0.3,0.1,-0.3,-0.4,0.1,2,-1,1,-0.2]
    fechas = ["2021-01-05", "2021-01-06", "2021-01-07", "2021-01-08", "2021-01-09", "2021-01-10", "2021-01-11", "2021-01-12", "2021-01-13", "2021-01-14"]

    self.assertEqual(dias_consecutivos_negativos(rendimientos, fechas), ["2021-01-10","2021-01-14"])
    self.assertNotEqual(dias_consecutivos_negativos(rendimientos, fechas), ["2021-01-12","2021-01-14"])

  def test_maximo_rendimiento_obtenible_v1(self):
    lows = [209,300,343,347,405,390,395,433,480,491]
    highs = [255,330,366,368,425,420,425,473,505,518]
    fechas = ["2021-01-05", "2021-01-06", "2021-01-07", "2021-01-08", "2021-01-09", "2021-01-10", "2021-01-11", "2021-01-12", "2021-01-13", "2021-01-14"]

    self.assertEqual(maximo_rendimiento_obtenible_unittest(lows, highs, fechas), ["2021-01-05","2021-01-14"])
    self.assertNotEqual(maximo_rendimiento_obtenible_unittest(lows, highs, fechas), ["2021-01-07","2021-01-11"])

  def test_maximo_rendimiento_obtenible_v2(self):
    lows = [209,300,343,347,405,390,395,433,480,491]
    highs = [255,330,366,368,425,420,425,473,505,518]
    fechas = ["2021-01-05", "2021-01-06", "2021-01-07", "2021-01-08", "2021-01-09", "2021-01-10", "2021-01-11", "2021-01-12", "2021-01-13", "2021-01-14"]

    self.assertEqual(maximo_rendimiento_obtenible_unittest(lows, highs, fechas), ["2021-01-07","2021-01-11"])
    self.assertNotEqual(maximo_rendimiento_obtenible_unittest(lows, highs, fechas), ["2021-01-05","2021-01-14"])

  def test_minimo_rendimiento_obtenible_v1(self):
    lows = [209,300,343,347,405,390,395,433,480,491]
    highs = [255,330,366,368,425,420,425,473,505,518]
    fechas = ["2021-01-05", "2021-01-06", "2021-01-07", "2021-01-08", "2021-01-09", "2021-01-10", "2021-01-11", "2021-01-12", "2021-01-13", "2021-01-14"]

    self.assertEqual(minimo_rendimiento_obtenible_unittest(lows, highs, fechas), ["2021-01-09","2021-01-10"])
    self.assertNotEqual(minimo_rendimiento_obtenible_unittest(lows, highs, fechas), ["2021-01-09","2021-01-15"])

  def test_minimo_rendimiento_obtenible_v2(self):
    lows = [209,300,343,347,405,390,395,433,480,491]
    highs = [255,330,366,368,425,420,425,473,505,518]
    fechas = ["2021-01-05", "2021-01-06", "2021-01-07", "2021-01-08", "2021-01-09", "2021-01-10", "2021-01-11", "2021-01-12", "2021-01-13", "2021-01-14"]

    self.assertEqual(minimo_rendimiento_obtenible_unittest(lows, highs, fechas), ["2021-01-09","2021-01-15"])
    self.assertNotEqual(minimo_rendimiento_obtenible_unittest(lows, highs, fechas), ["2021-01-09","2021-01-10"])



