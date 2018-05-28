import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import Crear_FPBajo

class Consumidor(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(
            'grupo',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'grupo',
            self.channel_name
         )
        
    # Recibes mensaje del websocket del frontend al backend (Receive message from WebSocket)
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        #La B es Back, variable
        Valor_B_NombreFiltro = text_data_json['Clave_F_NombreFiltro']
        Valor_B_Ap_db = text_data_json['Clave_F_Ap_db']
        Valor_B_As_db = text_data_json['Clave_F_As_db']
        Valor_B_Fp_Hz = text_data_json['Clave_F_Fp_Hz']
        Valor_B_Fs_Hz = text_data_json['Clave_F_Fs_Hz']
        Valor_B_Rg_Ohm = text_data_json['Clave_F_Rg_Ohm']
        Valor_B_Rl_Ohm = text_data_json['Clave_F_Rl_Ohm']
        Valor_Accion = text_data_json['Clave_Accion']
        #Si se cumple una condicion llamo a la tarea asincrona (celery), que la tarea asincrona luego envia el resultado al grupo, sino mando el mensaje directamente al grupo
        if str(Valor_Accion) == "Crear_FPBajo":
            #Llamo a celery
            CFPBajoCelery = Crear_FPBajo.delay(text_data)

            print(CFPBajoCelery.id)
            await self.channel_layer.group_send(
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
                }
            )
             
        #Manda directamente el mensaje al grupo  (Send message to room group)
        else:          
            await self.channel_layer.group_send(
                'grupo',
                {
                    'type': 'CrearFiltroAsincrono',
                    'Clave_B_Estado': "Error Filtro",
                    'Clave_B_Nombre_Filtro': Valor_B_NombreFiltro,
                    'Clave_B_Ap_db': Valor_B_Ap_db, 
                    'Clave_B_As_db': Valor_B_As_db,
                    'Clave_B_Fp_Hz': Valor_B_Fp_Hz,
                    'Clave_B_Fs_Hz': Valor_B_Fs_Hz,
                    'Clave_B_Rg_Ohm': Valor_B_Rg_Ohm,
                    'Clave_B_Rl_Ohm': Valor_B_Rl_Ohm,
                }
            )
            
    # Recibe los mensajes del grupo, tanto de la tarea asincrona como sino y los envia al front en JSON
    async def CrearFiltroAsincrono(self, event):
        Valor_B_Nombre_Filtro = event['Clave_B_Nombre_Filtro']
        Valor_B_Ap_db = event['Clave_B_Ap_db']
        Valor_B_As_db = event['Clave_B_As_db']
        Valor_B_Fp_Hz = event['Clave_B_Fp_Hz']
        Valor_B_Fs_Hz = event['Clave_B_Fs_Hz']
        Valor_B_Rg_Ohm= event['Clave_B_Rg_Ohm']
        Valor_B_Rl_Ohm = event['Clave_B_Rl_Ohm']
        Valor_B_Estado = event['Clave_B_Estado']

        # Envia mensaje del backend al frontend (Send message to WebSocket)
        await self.send(text_data=json.dumps({
            'type': 'CrearFiltroAsincrono',
            "Clave_B_Estado": Valor_B_Estado,
            'Clave_B_Nombre_Filtro': Valor_B_Nombre_Filtro,
            'Clave_B_Ap_db': Valor_B_Ap_db, 
            'Clave_B_As_db': Valor_B_As_db,
            'Clave_B_Fp_Hz': Valor_B_Fp_Hz,
            'Clave_B_Fs_Hz': Valor_B_Fs_Hz,
            'Clave_B_Rg_Ohm': Valor_B_Rg_Ohm,
            'Clave_B_Rl_Ohm': Valor_B_Rl_Ohm,
        }))