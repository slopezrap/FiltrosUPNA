from django.conf import settings
import os
import math
import matplotlib
matplotlib.use('Agg') #  Libreria para pintar los circuitos
import matplotlib.pyplot as plt #  Libreria para pintar las plantillas del filtro

#===============================================================================
#  Libreria para la base de datos del filtro
#===============================================================================
from .models import Filtro_Butterworth
from .models import Filtro_Chebyshev
#===============================================================================
# Libreria para pintar los circuitos
#===============================================================================
import SchemDraw as schem
import SchemDraw.elements as e

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
              
    #=========================================================================
    #  1 Dibujar la plantilla y plantilla normalizada del filtro
    #=========================================================================
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
            except:
                pass

            #pathImagen es la URL donde guardare la imagen
            pathImagen = (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+settings.MEDIA_FPB)
            #name_id_Filtro es el nombre del filtro y el la primary key del filtro para aniadirlo a la url
            #Pongo la doble \\ porque tengo que escapar la barra \
            name_id_Filtro = ('\\'+'Plantilla_Filtro_'+InstanciaFiltro.nameFilter+'_'+str(InstanciaFiltro.id)+'.png')
            #Guardo el la imagen del filtro en el pc
            Figura.savefig(pathImagen+name_id_Filtro)
            #Leo del pc la imagen del filtro para guardarla en la BBDD
            InstanciaFiltro.imagePlantilla = (pathImagen+name_id_Filtro)
 
    #=========================================================================
    #  2 Calcular el orden del filtro
    #=========================================================================            
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

    #=========================================================================
    #  SOLO BUTTERWORTH - Calcular la frencuencia de corte
    #=========================================================================           
    def Calcular_Frecuencia_Corte_Butterworth(self,OrdenFiltro,epsilonCuadrado):
        try:
            Omegamenos3db = float ( ( 1/( math.pow(epsilonCuadrado,(1/(2*OrdenFiltro))) ) ) )
            return ( Omegamenos3db )
        except:
            return ( 0 )      
        
    #=========================================================================
    #  3 Creo prototipo del filtro
    #=========================================================================       
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

    def Prototipo_Filtro_Chebyshev(self,OrdenFiltro):
        Lista_G_Filtro = []
        try:
            #Extraigo la instancia del filtro de la base de datos que le paso a la clase crear FiltroPasoBajo
            FiltroChebyshev = Filtro_Chebyshev.objects.get(ordenFiltro=OrdenFiltro)
            #Necesito el +1 porque si orden es 4 va del 1 al 4 , coge uno y excluye 4
            for x in range(1, int(OrdenFiltro)+1):
                # Necesito obtener FiltroChebyshev.g_x siendo x lo que recorro
                prefijo = "FiltroChebyshev"
                sufijo = ".g_"+str(x)
                PRE_SUF = '{0}{1}'.format(prefijo, sufijo)  # FiltroChebyshev.g_1 , ...
                Lista_G_Filtro.append(eval(PRE_SUF))
            return (Lista_G_Filtro)
        except:
            return ( 0 )
        
    #=========================================================================
    #  4 Dibujo los prototipos del filtro
    #========================================================================= 
    def Dibujar_Prototipo_Filtro(self,ListaDeLosGFiltro,InstanciaFiltro):
        try:
            d = schem.Drawing()
            Tierra = d.add(e.GND)
            V = d.add(e.SOURCE_SIN)
            R = d.add(e.RES, d='right') #Resistencia del generador -> Rg
            
            if round( len(ListaDeLosGFiltro) / 2 ) == 0:
                B = d.add(e.INDUCTOR2, d='right',label=str('{:.3g}'.format( ListaDeLosGFiltro[0] )))
                d.push() # GUARDO LA POSICION PARA LUEGO RECUPERARLO
                L = d.add(e.LINE, d='right')
                R = d.add(e.RES, d='down') #Resistencia de carga (load) -> Rl
                Tierra = d.add(e.GND)
                  
            else:
                def anidir_bobina(posicion_bobina, ListaDeLosGFiltro):
                    d.pop()  #RECUPERO LA POSICION
                    B = d.add(e.INDUCTOR2, d='right',label=str('{:.3g}'.format( ListaDeLosGFiltro[posicion_bobina] )))
                    d.push() # GUARDO LA POSICION PARA LUEGO RECUPERARLO
                
                    
                def anidiar_condensador(posicion_condensador, ListaDeLosGFiltro):
                    if (posicion_condensador == (len(ListaDeLosGFiltro))):
                        L = d.add(e.LINE, d='right')
                        R = d.add(e.RES, d='down') #Resistencia de carga (load) -> Rl
                        Tierra = d.add(e.GND)
                
                    else:
                        if (posicion_condensador == (len(ListaDeLosGFiltro)-1)):
                            C = d.add(e.CAP,d='down',label=str('{:.3g}'.format( ListaDeLosGFiltro[posicion_condensador] ))) 
                            Tierra = d.add(e.GND)
                            d.pop()  #RECUPERO LA POSICION
                            L = d.add(e.LINE, d='right')
                            R = d.add(e.RES, d='down') #Resistencia de carga (load) -> Rl
                            Tierra = d.add(e.GND)
                        else:
                            C = d.add(e.CAP,d='down',label=str('{:.3g}'.format( ListaDeLosGFiltro[posicion_condensador] ))) 
                            Tierra = d.add(e.GND)
                
                posicion_bobina = 0 
                posicion_condensador = 1
                for i in range(0,  math.ceil( len(ListaDeLosGFiltro) / 2 ) ):
                    #Para recorre cada malla lo que haga es round(len(ListaDeLosGFiltro)/2)
                    #En cada malla aniado una bobina 
                    anidir_bobina(posicion_bobina,ListaDeLosGFiltro)
                    #En cada malla aniado un condensador siempre que la posicion del condensador no sea la longitud de la ListaDeLosGFiltro, ya que eso quiere decir que en esa
                    #malla no habra condensador.
                    #Si tengo un array de 3 posiciones sera que hay bobina pos[0], condensador pos[1], bobina pos[2]. La longitud de la ListaDeLosGFiltro es 3 y la posicion del siguiente condensador sera 3
                    #por lo que pos[3] == 3 entonces no existe en la ListaDeLosGFiltro la pos[3] por lo que va a tierra 
                    anidiar_condensador(posicion_condensador,ListaDeLosGFiltro)
                    posicion_bobina = posicion_condensador + 1
                    posicion_condensador = posicion_bobina + 1
                            
            pathImagen = (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+settings.MEDIA_FPB)
            #name_id_Filtro es el nombre del filtro y el la primary key del filtro para aniadirlo a la url
            #Pongo la doble \\ porque tengo que escapar la barra \
            name_id_Filtro = ('\\'+'Dibujo_Prototipo_Filtro_'+InstanciaFiltro.nameFilter+'_'+str(InstanciaFiltro.id)+'.png')
            d.draw()
            d.save(pathImagen+name_id_Filtro)
            #Leo del pc la imagen del filtro para guardarla en la BBDD
            InstanciaFiltro.imagePrototipoFiltro = (pathImagen+name_id_Filtro)
            
        except:
            pass
        
    #=========================================================================
    #  SOLO BUTTERWORTH - Desnormalizar en frecuencia
    #=========================================================================   
    def Desnormalizar_Frecuencia_Omegamenos3db_Butterworth(self,Omegamenos3db,Lista_G_Filtro):
        try:
            for i in range(0, len(Lista_G_Filtro)):
                Lista_G_Filtro[i]=Lista_G_Filtro[i]/Omegamenos3db
            return (Lista_G_Filtro)
        except:
            return ( 0 )
    
    #=========================================================================
    #  5 Desnormalizacion en frecuencia a Wp y en resistencia generador Rg
    #========================================================================= 
    def Desnormalizar_Frecuencia_Impedancia(self,Fp_Hz,Rg_Ohm,Lista_G_Filtro):
        for i in range(0, len(Lista_G_Filtro)):
            if i%2 == 0: #Posiciones pares lista, porque son bobinas
                Lista_G_Filtro[i]=Lista_G_Filtro[i]*(Rg_Ohm/(2*math.pi*Fp_Hz))
            else:
                Lista_G_Filtro[i]=Lista_G_Filtro[i]*(1/(Rg_Ohm*2*math.pi*Fp_Hz))  
        return (Lista_G_Filtro)
    
    #=========================================================================
    #  6 Dibujo el circuito desnormalizado frecuencia e impedancia
    #========================================================================= 
    def Dibujar_Filtro_Desnormalizado(self,ListaDeLosGFiltro,InstanciaFiltro):
        try:
            d = schem.Drawing()
            Tierra = d.add(e.GND)
            V = d.add(e.SOURCE_SIN)
            R = d.add(e.RES, d='right') #Resistencia del generador -> Rg
            
            if round( len(ListaDeLosGFiltro) / 2 ) == 0:
                B = d.add(e.INDUCTOR2, d='right',label=str('{:.3g}'.format( ListaDeLosGFiltro[0] )))
                d.push() # GUARDO LA POSICION PARA LUEGO RECUPERARLO
                L = d.add(e.LINE, d='right')
                R = d.add(e.RES, d='down') #Resistencia de carga (load) -> Rl
                Tierra = d.add(e.GND)
                  
            else:
                def anidir_bobina(posicion_bobina, ListaDeLosGFiltro):
                    d.pop()  #RECUPERO LA POSICION
                    B = d.add(e.INDUCTOR2, d='right',label=str('{:.3g}'.format( ListaDeLosGFiltro[posicion_bobina] )))
                    d.push() # GUARDO LA POSICION PARA LUEGO RECUPERARLO
                
                    
                def anidiar_condensador(posicion_condensador, ListaDeLosGFiltro):
                    if (posicion_condensador == (len(ListaDeLosGFiltro))):
                        L = d.add(e.LINE, d='right')
                        R = d.add(e.RES, d='down') #Resistencia de carga (load) -> Rl
                        Tierra = d.add(e.GND)
                
                    else:
                        if (posicion_condensador == (len(ListaDeLosGFiltro)-1)):
                            C = d.add(e.CAP,d='down',label=str('{:.3g}'.format( ListaDeLosGFiltro[posicion_condensador] ))) 
                            Tierra = d.add(e.GND)
                            d.pop()  #RECUPERO LA POSICION
                            L = d.add(e.LINE, d='right')
                            R = d.add(e.RES, d='down') #Resistencia de carga (load) -> Rl
                            Tierra = d.add(e.GND)
                        else:
                            C = d.add(e.CAP,d='down',label=str('{:.3g}'.format( ListaDeLosGFiltro[posicion_condensador] ) )) 
                            Tierra = d.add(e.GND)
                
                posicion_bobina = 0 
                posicion_condensador = 1
                for i in range(0,  math.ceil( len(ListaDeLosGFiltro) / 2 ) ):
                    #Para recorre cada malla lo que haga es round(len(ListaDeLosGFiltro)/2)
                    #En cada malla aniado una bobina 
                    anidir_bobina(posicion_bobina,ListaDeLosGFiltro)
                    #En cada malla aniado un condensador siempre que la posicion del condensador no sea la longitud de la ListaDeLosGFiltro, ya que eso quiere decir que en esa
                    #malla no habra condensador.
                    #Si tengo un array de 3 posiciones sera que hay bobina pos[0], condensador pos[1], bobina pos[2]. La longitud de la ListaDeLosGFiltro es 3 y la posicion del siguiente condensador sera 3
                    #por lo que pos[3] == 3 entonces no existe en la ListaDeLosGFiltro la pos[3] por lo que va a tierra 
                    anidiar_condensador(posicion_condensador,ListaDeLosGFiltro)
                    posicion_bobina = posicion_condensador + 1
                    posicion_condensador = posicion_bobina + 1
                            
            pathImagen = (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+settings.MEDIA_FPB)
            #name_id_Filtro es el nombre del filtro y el la primary key del filtro para aniadirlo a la url
            #Pongo la doble \\ porque tengo que escapar la barra \
            name_id_Filtro = ('\\'+'Dibujo_Filtro_Desnormalizado_'+InstanciaFiltro.nameFilter+'_'+str(InstanciaFiltro.id)+'.png')
            d.draw()
            d.save(pathImagen+name_id_Filtro)
            #Leo del pc la imagen del filtro para guardarla en la BBDD
            InstanciaFiltro.imageDesnormalizadaFreImp = (pathImagen+name_id_Filtro)
            
        except:
            pass    
    
    #=========================================================================
    #  LLAMADA DE METODOS
    #=========================================================================  
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
            (Lista_G_Filtro) = FPB.Prototipo_Filtro_Butterworth(OrdenFiltro)
            # 4 Dibujo los prototipos del filtro
            FPB.Dibujar_Prototipo_Filtro(Lista_G_Filtro,InstanciaFiltro)
            #  SOLO BUTTERWORTH - Desnormalizar en frecuencia
            (Lista_G_Filtro_Des) = FPB.Desnormalizar_Frecuencia_Omegamenos3db_Butterworth(Omegamenos3db,Lista_G_Filtro)
            # 5 Desnormalizacion en frecuencia a Wp y en resistencia generador Rg
            (Lista_G_Filtro_Des_Fre_Imp) = FPB.Desnormalizar_Frecuencia_Impedancia(Fp_Hz,Rg_Ohm,Lista_G_Filtro_Des)
            # 6 Dibujo el circuito desnormalizado frecuencia e impedancia
            FPB.Dibujar_Filtro_Desnormalizado(Lista_G_Filtro_Des_Fre_Imp,InstanciaFiltro)
            
        elif (tipo_Filtro == "Chebyshev") :
            # 1 Dibujar la plantilla y plantilla normalizada del filtro
            FPB.Dibujar_Plantilla_Filtro(InstanciaFiltro,id_Filtro,Ap,As,Fp,Fs,OMEGAp,OMEGAs,Etiqueta_F,Etiqueta_DB,escala_max_F,escala_max_DB)
            # 2 Calcular el orden del filtro
            (OrdenFiltro,epsilonCuadrado) = FPB.Calcular_Orden_Filtro_Chebyshev(As_db,Ap_db,OMEGAs)
            # 3 Creo prototipo del filtro
            (Lista_G_Filtro) = FPB.Prototipo_Filtro_Chebyshev(OrdenFiltro)
            # 4 Dibujo los prototipos del filtro
            FPB.Dibujar_Prototipo_Filtro(Lista_G_Filtro,InstanciaFiltro)
            # 5 Desnormalizacion en frecuencia a Wp y en resistencia generador Rg
            (Lista_G_Filtro_Des_Fre_Imp) =FPB.Desnormalizar_Frecuencia_Impedancia(Fp_Hz,Rg_Ohm,Lista_G_Filtro)
            # 6 Dibujo el circuito desnormalizado frecuencia e impedancia
            FPB.Dibujar_Filtro_Desnormalizado(Lista_G_Filtro_Des_Fre_Imp,InstanciaFiltro)