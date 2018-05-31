from __future__ import absolute_import, unicode_literals
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from .models import ModeloFPBajo
from .FiltroPasoBajo import FiltroPasoBajo


@shared_task
def Crear_FPBajo(Filtro_id,text_data):
        #Extraigo el filtro de la base de datos
        Filtro = ModeloFPBajo.objects.get(pk=Filtro_id)
        #Llamo a la clase que crea el filtro paso bajo
        FPB=FiltroPasoBajo(Filtro.id,Filtro.nameFilter,Filtro.tipoFiltro,Filtro.Ap_db,Filtro.As_db,Filtro.Fp_Hz,Filtro.Fs_Hz,Filtro.Rg_Ohm,Filtro.Rl_Ohm)
        FPB.Crear_Filtro_Paso_Bajo()
        
        
        #Actualizo el estado a completado:
        Filtro.estado = "Completado"
        Filtro.save()
        #La B es Back, variable
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'grupo',
            {
                    'type': 'CrearFiltroAsincrono', 
                    'Clave_B_Estado': "Completado",
                    'Clave_B_Filtro_id' : Filtro.id,
                    'Clave_B_Nombre_Filtro': Filtro.nameFilter,
                    'Clave_B_TipoFiltro': Filtro.tipoFiltro,
                    'Clave_B_Ap_db': Filtro.Ap_db, 
                    'Clave_B_As_db': Filtro.As_db,
                    'Clave_B_Fp_Hz': Filtro.Fp_Hz,
                    'Clave_B_Fs_Hz': Filtro.Fs_Hz,
                    'Clave_B_Rg_Ohm': Filtro.Rg_Ohm,
                    'Clave_B_Rl_Ohm': Filtro.Rl_Ohm
             },
        )