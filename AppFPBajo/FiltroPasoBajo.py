import os
import matplotlib
import matplotlib.pyplot as plt
import math
from .models import Filtro_Butterworth


class FiltroPasoBajo:
    """
    id: Identificiador del filtro en la base de datos
    nombre_Filtro: Nombre del filtro en la base de datos
    Ap_db: Atenuacion en la banda de paso, medida en Decibelios (db) 
    As_db: Atenuacion en la banda eliminada (stop), medida en Decibelios (db) 
    Fp_Hz: Frecuencia de paso, medida en Herzios (Hz)
    Fs_Hz: Frecuencia de stop, medida en Herzios (Hz)
    Rg_Ohm: Resistencia generador, medida en ohmios (Ohm)
    Rl_Ohm: Resistencia de carga (load), medida en ohmios (Ohm)
    """   

    #Metodo constructor y le paso la instancia del filtro de la base de datos
    def __init__(self,Filtro):
        self.Filtro = Filtro

    #Me creo esta funcion para que sea escalable el filtro por si hay que cambiar el orden del filtro
    def Valores_Filtro(self):
        InstanciaFiltro = self.Filtro
        id_Filtro = self.Filtro.id
        n_Filtro = self.Filtro.nameFilter
        tipo_Filtro = self.Filtro.tipoFiltro
        Ap_db = self.Filtro.Ap_db
        As_db = self.Filtro.As_db
        Fp_Hz = self.Filtro.Fp_Hz
        Fs_Hz = self.Filtro.Fs_Hz
        Rg_Ohm = self.Filtro.Rg_Ohm
        Rl_Ohm = self.Filtro.Rl_Ohm
        return (InstanciaFiltro,id_Filtro,n_Filtro,tipo_Filtro,Ap_db,As_db,Fp_Hz,Fs_Hz,Rg_Ohm,Rl_Ohm)
        
    #Normalizo la frencuencia para sacar la omega
    def Frecuencia_Normalizada(self,Fp_Hz,Fs_Hz):
        Wp = (2*math.pi*Fp_Hz)
        Ws = (2*math.pi*Fs_Hz)
        try:
            OMEGAp= Wp/Wp
        except ZeroDivisionError:
            OMEGAp=0
        try:
            OMEGAs= Ws/Wp
        except ZeroDivisionError:
            OMEGAs = 0
        return(OMEGAp,OMEGAs)  
    
    #Escalo las frecuencias para poner las etiquetas en cada plantilla
    def Escalar_Frecuencia(self,Fp_Hz,Fs_Hz):
        #Hz
        if (Fs_Hz<=999):
            escala_mayor_frecuencia = 100
            etiqueta = "Herzios [Hz]"
            print("Trabajando en Herzios [Hz]")
            return (Fp_Hz,Fs_Hz,etiqueta,escala_mayor_frecuencia)
        
        #Khz
        elif (Fs_Hz>999 and Fs_Hz<=999999): #divido entre 1000 y me queda 999*10^3 Hz
            escala_mayor_frecuencia = 100
            s_Fp_KHz =  Fp_Hz/1000
            s_Fs_KHz =  Fs_Hz/1000
            etiqueta = "KiloHerzios [KHz]"
            print("Trabajando en KiloHerzios [KHz]")
            return (s_Fp_KHz,s_Fs_KHz,etiqueta,escala_mayor_frecuencia)
        
        #Mhz
        elif (Fs_Hz>999999 and Fs_Hz<=999999999): #divido entre 1000000 y me queda 999*10^6 Hz
            escala_mayor_frecuencia = 100
            s_Fp_MHz =  Fp_Hz/1000000
            s_Fs_MHz =  Fs_Hz/1000000
            etiqueta = "MegaHerzios [MHz]"
            print("Trabajando en MegaHerzios [MHz]")
            return(s_Fp_MHz,s_Fs_MHz,etiqueta,escala_mayor_frecuencia)
            
        #Ghz
        elif (Fs_Hz>999999999 and Fs_Hz<=999999999999): #divido entre 1000000000 y me queda 999*10^9 Hz
            escala_mayor_frecuencia = 100
            s_Fp_GHz =  Fp_Hz/1000000000
            s_Fs_GHz =  Fs_Hz/1000000000
            print("Trabajando en KiloHerzios [GHz]")
            etiqueta = "GigaHerzios [GHz]"  
            return(s_Fp_GHz,s_Fs_GHz,etiqueta,escala_mayor_frecuencia)    
        
        #Thz
        elif (Fs_Hz>999999999999 and Fs_Hz<=999999999999999): #divido entre 1000000000000 y me queda 999*10^12 Hz
            escala_mayor_frecuencia = 100
            s_Fp_THz =  Fp_Hz/1000000000000
            s_Fs_THz =  Fs_Hz/1000000000000
            etiqueta = "TeraHerzios [THz]"  
            print("Trabajando en TeraHerzios [THz]")
            return(s_Fp_THz,s_Fs_THz,etiqueta,escala_mayor_frecuencia)  
        
        #PHz
        elif (Fs_Hz>999999999999999 and Fs_Hz<=999999999999999999): #divido entre 1000000000000000 y me queda 999*10^15 Hz
            escala_mayor_frecuencia = 100
            s_Fp_PHz =  Fp_Hz/1000000000000000
            s_Fs_PHz =  Fs_Hz/1000000000000000
            etiqueta = "PetaHerzios [PHz]"  
            print("Trabajando en PetaHerzios [PHz]")
            return(s_Fp_PHz,s_Fs_PHz,etiqueta,escala_mayor_frecuencia) 
        
        #Fuera de rango
        else:
            etiqueta = "Fuera de rango" 
            
    #Escalo las frecuencias para poner las etiquetas en cada plantilla      
    def Escalar_db(self,Ap_db,As_db):
        Etiqueta_DB = "Decibelios [db]"
        escala_mayor_db = 10
        return(Ap_db,As_db,Etiqueta_DB,escala_mayor_db)           
      
    #En lugar de pasarselo como parametro a la funcion uso las variables del constructor
    def Dibujar_Plantilla_Filtro(self,InstanciaFiltro,Filtro_id,Ap,As,Fp,Fs,OMEGAp,OMEGAs,Etiqueta_F,Etiqueta_Db,Escala_Mayor_Frecuencia,Escala_Mayor_DB):
            #Creo la figura
            Figura = plt.figure()
                
            """Modulo de la funcion de transferencia de un filtro paso bajo"""
            Modulo_Funcion_Transferencia_Filtro = Figura.add_subplot(5,1,1) # con esto digo que pinten la figura en dicha posicion, divido el cuadro en 5 filas y 1 columna y selecciono la posicion 1
            BandaDePaso = matplotlib.patches.Rectangle((0,0),Fp - 0,-Ap-0, color='red')
            BandaDeTransicion = matplotlib.patches.Rectangle((Fp,0),Fs - Fp,-(As-0), color='red')
            BandaDeStop = matplotlib.patches.Rectangle((Fs,0),Fs+Escala_Mayor_Frecuencia-Fs,-(As-0), hatch='\\',fill=False)
            Modulo_Funcion_Transferencia_Filtro.add_patch(BandaDePaso)
            Modulo_Funcion_Transferencia_Filtro.add_patch(BandaDeTransicion)
            Modulo_Funcion_Transferencia_Filtro.add_patch(BandaDeStop)
            Modulo_Funcion_Transferencia_Filtro.set_xlim([0,Fs+Escala_Mayor_Frecuencia])
            Modulo_Funcion_Transferencia_Filtro.set_ylim([-(As + Escala_Mayor_DB),0])
            plt.annotate('Fp', xy=(0, 0), xytext=(Fp,0) )
            plt.annotate('Fs', xy=(0, 0), xytext=(Fs,0) )
            plt.annotate('Ap', xy=(0, 0), xytext=(0, -Ap) )
            plt.annotate('As', xy=(0, 0), xytext=(0, -As) )
            plt.xlabel(Etiqueta_F)
            plt.ylabel(Etiqueta_Db)
            plt.title('Modulo de la funcion de transferencia de un filtro paso bajo')
            plt.grid(True)
            
                      
            """Plantilla de atenuacion del filtro"""
            Plantilla_Filtro = Figura.add_subplot(5,1,3) # con esto digo que pinten la figura en dicha posicion, divido el cuadro en 5 filas y 1 columna y selecciono la posicion 3
            BandaDePaso = matplotlib.patches.Rectangle((0,0),Fp - 0,Ap-0, color='red')
            BandaDePasoAtenuacion = matplotlib.patches.Rectangle((0,Ap),(Fp-0),(As+Ap), color='gray')
            BandaDeTransicion = matplotlib.patches.Rectangle((Fp,0),Fs - Fp,(As-0), color='red')
            BandaDeStop = matplotlib.patches.Rectangle((Fs,0),Fs+Escala_Mayor_Frecuencia-Fs,(As - 0), color='gray')
            Plantilla_Filtro.add_patch(BandaDePaso)
            Plantilla_Filtro.add_patch(BandaDePasoAtenuacion)
            Plantilla_Filtro.add_patch(BandaDeTransicion)
            Plantilla_Filtro.add_patch(BandaDeStop)
            plt.xlim([0,Fs+Escala_Mayor_Frecuencia])
            plt.ylim([0,(As + Escala_Mayor_DB)])
            plt.annotate('Fp', xy=(0, 0), xytext=(Fp,0) )
            plt.annotate('Fs', xy=(0, 0), xytext=(Fs,0) )
            plt.annotate('Ap', xy=(0, 0), xytext=(0, Ap) )
            plt.annotate('As', xy=(0, 0), xytext=(0, As) )
            plt.xlabel(Etiqueta_F)
            plt.ylabel(Etiqueta_Db)
            plt.title('Plantilla de atenuacion del filtro')
            plt.grid(True)
            
            
            """Plantilla de atenuacion normalizada del filtro"""
            Plantilla_Filtro = Figura.add_subplot(5,1,5) # con esto digo que pinten la figura en dicha posicion, divido el cuadro en 5 filas y 1 columna y selecciono la posicion 3
            BandaDePaso = matplotlib.patches.Rectangle((0,0),OMEGAp - 0,Ap-0, color='red') #Wp es (2*np.pi*Fp)
            BandaDePasoAtenuacion = matplotlib.patches.Rectangle((0,Ap),(OMEGAp-0),(As+Ap), color='gray')
            BandaDeTransicion = matplotlib.patches.Rectangle((OMEGAp,0),(OMEGAs - OMEGAp),(As-0), color='red')
            BandaDeStop = matplotlib.patches.Rectangle((OMEGAs,0),OMEGAs+Escala_Mayor_Frecuencia-OMEGAs,(As - 0), color='gray')
            Plantilla_Filtro.add_patch(BandaDePaso)
            Plantilla_Filtro.add_patch(BandaDePasoAtenuacion)
            Plantilla_Filtro.add_patch(BandaDeTransicion)
            Plantilla_Filtro.add_patch(BandaDeStop)
            try:
                plt.xlim([0,OMEGAs+((2*math.pi*Escala_Mayor_Frecuencia)/(2*math.pi*Fp))])
                plt.ylim([0,(As + Escala_Mayor_DB)])
                plt.annotate('OMEGAp', xy=(0, 0), xytext=(OMEGAp,0) )
                plt.annotate('OMEGAs', xy=(0, 0), xytext=(OMEGAs,0) )
                plt.annotate('Ap', xy=(0, 0), xytext=(0, Ap) )
                plt.annotate('As', xy=(0, 0), xytext=(0, As) )
                plt.xlabel("OMEGAp [Wp/Wp] y OMEGAs [Ws/Wp] siendo W=2*pi*f")
                plt.ylabel(Etiqueta_Db)
                plt.title('Plantilla de atenuacion normalizada del filtro')
                plt.grid(True)
            except ZeroDivisionError:
                pass
            
            """esto debe guardar la imagen en la base de datos si se ejecuta bien celery
            figure = io.BytesIO()
            plt.savefig(figure, format="png")
            content_file = ImageFile(figure)
            InstanciaFiltro.nameFilter = "FiltroGuardado"
            InstanciaFiltro.imagePlantilla.save('imagen.png', content_file)
            InstanciaFiltro.save()
            """
            """mientras hago una chapucilla que es coger el path donde se guardan las imagenes predefinido en models y concatenar a ese path el nombre del fitro y el id"""
            #pathImagen es la URL donde guardare la imagen
            pathImagen = (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\media\FPBajo')
            #name_id_Filtro es el nombre del filtro y el la primary key del filtro para aniadirlo a la url
            #Pongo la doble \\ porque tengo que escapar la barra \
            name_id_Filtro = ('\\'+InstanciaFiltro.nameFilter+'_'+str(InstanciaFiltro.id)+'.png')
            #Guardo el la imagen del filtro en el pc
            Figura.savefig(pathImagen+name_id_Filtro)
            #Leo del pc la imagen del filtro para guardarla en la BBDD
            InstanciaFiltro.imagePlantilla = (pathImagen+name_id_Filtro)
            
    def Calcular_Orden_Filtro_Butterworth(self,As_db,Ap_db,OMEGAs):
        try:
            deltaCuadrado = float(  ( math.pow(10,(As_db/10)) ) -1 )
            epsilonCuadrado = float( ( math.pow(10,(Ap_db/10)) ) -1 )
            raizDeltaEpsilon = float( math.sqrt(deltaCuadrado/epsilonCuadrado) )
            logaritmoRaizDeltaEpsilon = float( math.log(raizDeltaEpsilon,10) )
            OrdenFiltro = float( (logaritmoRaizDeltaEpsilon/(math.log(OMEGAs,10))) )
            return ( math.ceil(OrdenFiltro) , epsilonCuadrado )
        except:
            return ( 0 , 0 )
        
    def Calcular_Orden_Filtro_Chebyshev(self,As_db,Ap_db,OMEGAs):
        try:
            deltaCuadrado = float(  ( math.pow(10,(As_db/10)) ) -1 )
            epsilonCuadrado = float( ( math.pow(10,(Ap_db/10)) ) -1 )
            raizDeltaEpsilon = float( math.sqrt(deltaCuadrado/epsilonCuadrado) )
            OrdenFiltro = float ( ( math.acosh(raizDeltaEpsilon) / math.acosh(OMEGAs) ) )
            return ( math.ceil(OrdenFiltro) , epsilonCuadrado )
        except:
            return ( 0 )  
        
    def Calcular_Frecuencia_Corte_Butterworth(self,OrdenFiltro,epsilonCuadrado):
        try:
            Omegamenos3db = float ( ( 1/( math.pow(epsilonCuadrado,(1/(2*OrdenFiltro))) ) ) )
            return ( Omegamenos3db )
        except:
            return ( 0 )      
        
    def Prototipo_Filtro_Butterworth(self,OrdenFiltro):
        Lista_G_Filtro = []
        try:
            #Extraigo la instancia del filtro de la base de datos que le paso a la clase crear FiltroPasoBajo
            FiltroButterworth = Filtro_Butterworth.objects.get(ordenFiltro=OrdenFiltro)
            #Necesito el +1 porque si orden es 4 va del 1 al 4 , coge uno y excluye 4
            for x in range(1, int(OrdenFiltro)+1):
                # Necesito obtener FiltroButterworth.g_x siendo x lo que recorro
                prefijo = "FiltroButterworth"
                sufijo = ".g_"+str(x)
                PRE_SUF = '{0}{1}'.format(prefijo, sufijo)  # FiltroButterworth.g_1 , ...
                Lista_G_Filtro.append(eval(PRE_SUF))
            return (Lista_G_Filtro)
        except:
            return ( 0 )

    def Crear_Filtro_Paso_Bajo(self):
        FPB=FiltroPasoBajo(self.Filtro)
        (InstanciaFiltro,id_Filtro,n_Filtro,tipo_Filtro,Ap_db,As_db,Fp_Hz,Fs_Hz,Rg_Ohm,Rl_Ohm) = FPB.Valores_Filtro()
        (OMEGAp,OMEGAs)=FPB.Frecuencia_Normalizada(Fp_Hz,Fs_Hz)
        (Fp,Fs,Etiqueta_F,escala_max_F) = FPB.Escalar_Frecuencia(Fp_Hz,Fs_Hz)
        (Ap,As,Etiqueta_DB,escala_max_DB) = FPB.Escalar_db(Ap_db,As_db)
             
        
        if (tipo_Filtro == "Butterworth") :
            # 1 Dibujar la plantilla y plantilla normalizada del filtro
            FPB.Dibujar_Plantilla_Filtro(InstanciaFiltro,id_Filtro,Ap,As,Fp,Fs,OMEGAp,OMEGAs,Etiqueta_F,Etiqueta_DB,escala_max_F,escala_max_DB)
            # 2 Calcular el orden del filtro
            (OrdenFiltro,epsilonCuadrado) = FPB.Calcular_Orden_Filtro_Butterworth(As_db,Ap_db,OMEGAs)
            # SOLO BUTTERWORTH - Calcular la frencuencia de corte
            Omegamenos3db = FPB.Calcular_Frecuencia_Corte_Butterworth(OrdenFiltro, epsilonCuadrado)
            # 3 Creo prototipo del filtro
            FPB.Prototipo_Filtro_Butterworth(OrdenFiltro)

        elif (tipo_Filtro == "Chebyshev") :
            # 1 Dibujar la plantilla y plantilla normalizada del filtro
            FPB.Dibujar_Plantilla_Filtro(InstanciaFiltro,id_Filtro,Ap,As,Fp,Fs,OMEGAp,OMEGAs,Etiqueta_F,Etiqueta_DB,escala_max_F,escala_max_DB)
            # 2 Calcular el orden del filtro
            (OrdenFiltro,epsilonCuadrado) = FPB.Calcular_Orden_Filtro_Chebyshev(As_db,Ap_db,OMEGAs)
