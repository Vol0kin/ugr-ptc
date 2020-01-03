# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from capturar import establecer_conexion, obtener_camara_handler, procesar_ciclo, stop_simulacion_conexion
from agrupar import procesar_clusters_muestra
from caracteristicas import calcular_caracteristicas 
from sklearn.externals import joblib