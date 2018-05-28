from __future__ import absolute_import, unicode_literals
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time


@shared_task
def Crear_FPBajo(text_data):
        text_data_json = json.loads(text_data)
        #La B es Back, variable
        Valor_B_NombreFiltro = text_data_json['Clave_F_NombreFiltro']
        Valor_B_Ap_db = text_data_json['Clave_F_Ap_db']
        Valor_B_As_db = text_data_json['Clave_F_As_db']
        Valor_B_Fp_Hz = text_data_json['Clave_F_Fp_Hz']
        Valor_B_Fs_Hz = text_data_json['Clave_F_Fs_Hz']
        Valor_B_Rg_Ohm = text_data_json['Clave_F_Rg_Ohm']
        Valor_B_Rl_Ohm = text_data_json['Clave_F_Rl_Ohm']
        channel_layer = get_channel_layer()
        time.sleep(5)
        async_to_sync(channel_layer.group_send)(
            'grupo',
            {
                'type': 'CrearFiltroAsincrono',
                'Clave_B_Estado': "Creando Filtro", 
                'Clave_B_Nombre_Filtro': Valor_B_NombreFiltro,
                'Clave_B_Ap_db': Valor_B_Ap_db, 
                'Clave_B_As_db': Valor_B_As_db,
                'Clave_B_Fp_Hz': Valor_B_Fp_Hz,
                'Clave_B_Fs_Hz': Valor_B_Fs_Hz,
                'Clave_B_Rg_Ohm': Valor_B_Rg_Ohm,
                'Clave_B_Rl_Ohm': Valor_B_Rl_Ohm,
             },
        )