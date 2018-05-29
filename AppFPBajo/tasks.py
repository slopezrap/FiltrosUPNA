from __future__ import absolute_import, unicode_literals
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from .models import ModeloFPBajo


@shared_task
def Crear_FPBajo(Filtro_id,text_data):
        time.sleep(5)
        Filtro = ModeloFPBajo.objects.get(pk=Filtro_id)
        #Actualizo el estado a completado:
        Filtro.estado = "Completado"
        Filtro.save()
        print(Filtro.id)
        #La B es Back, variable
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'grupo',
            {
                    'type': 'CrearFiltroAsincrono',
                    'Clave_B_Estado': "Completado",
                    'Clave_B_Filtro_id' : Filtro.id,
                    'Clave_B_Nombre_Filtro': Filtro.nameFilter,
                    'Clave_B_Ap_db': Filtro.Ap_db, 
                    'Clave_B_As_db': Filtro.As_db,
                    'Clave_B_Fp_Hz': Filtro.Fp_Hz,
                    'Clave_B_Fs_Hz': Filtro.Fs_Hz,
                    'Clave_B_Rg_Ohm': Filtro.Rg_Ohm,
                    'Clave_B_Rl_Ohm': Filtro.Rl_Ohm
             },
        )