import sys
import os

# Agregar ruta del paquete cod al path del sistema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cod')))

import streamlit as st
import streamlit.components.v1 as components
from Mapa import Mapa
from Distancias import Distancias
from Enrutamiento import Enrutamiento
from MapaInteractivo import MapaInteractivo
from Graficar import Graficar
import matplotlib.pyplot as plt


class StreamlitApp:
    def __init__(self):
        '''
        Constructor de la clase StreamlitApp

        Returns
        -------
        None.

        '''
        self.__ubicaciones = []


    def __str__(self):
        '''
        Método STR de la clase StreamlitApp

        Returns
        -------
        str
            DESCRIPTION.

        '''
        return f"StreamlitApp con ubicaciones: {self.__ubicaciones}"

    @property
    def ubicaciones(self):
        '''
        Getter del atributo ubicaciones

        Returns
        -------
        list
            Lista de ubicaciones. Serán proporcionadas por el usuario

        '''
        return self.__ubicaciones

    @ubicaciones.setter
    def ubicaciones(self, value: list):
        '''
        Setter del atributo ubicaciones.

        Parameters
        ----------
        value : list
            Nueva lista de ubicaciones.

        Returns
        -------
        None.

        '''
        self.__ubicaciones = value

    def mostrar_dashboard(self):
        '''
        Método principal que despliega el dashboard interactivo con Streamlit.
        Crea internamente las instancias necesarias para calcular y visualizar
        la ruta óptima a partir de las ubicaciones.
    
        Returns
        -------
        None.
        '''
        st.set_page_config(page_title="Rutas Óptimas", layout="wide")
        st.title("Dashboard de Optimización de Rutas de Entrega")
    
        # Entrada de ubicaciones
        ubicaciones_input = st.text_area(
            "Ingrese las ubicaciones (una por línea):",
            "Tibás\nEscazú\nCurridabat"
        )
        self.ubicaciones = [line.strip() for line in ubicaciones_input.splitlines() if line.strip()]
        if self.ubicaciones:
            st.write("Ubicaciones procesadas:", self.ubicaciones)
    
        # Botón para generar rutas
        if st.button("Generar Ruta"):
            with st.spinner("Calculando la mejor ruta..."):
                try:
                    mapa = Mapa(self.ubicaciones)
                    dist = Distancias(mapa)
                    matriz_km = dist.distancias()
                    ruta = Enrutamiento(matriz_km, depot=0)
                    solucion = ruta.enrutar()
    
                    st.subheader("Ruta óptima")
                    lugares_ruta = [self.ubicaciones[i] for i in solucion["Ruta"]]
                    st.write(" → ".join(lugares_ruta))
                    st.write(f"Distancia total: {solucion['Recorrido total']}")
    
                    tab1, tab2 = st.tabs(["Mapa Interactivo", "Tramos"])
    
                    # Mapa interactivo con botón de pantalla completa
                    with tab1:
                        st.subheader("Mapa interactivo")
                        mapa_folium = MapaInteractivo(mapa, solucion).crear_mapa_interactivo()
                        html_path = "mapa_interactivo.html"
                        mapa_folium.save(html_path)
    
                        if os.path.exists(html_path):
                            with open(html_path, "r", encoding="utf-8") as f:
                                content = f.read().replace('"', '&quot;')
                                iframe = f"""
                                <div style='text-align: center;'>
                                    <iframe srcdoc="{content}" width='100%' height='600' id='mapaFrame' style='border:2px solid #ccc; border-radius: 8px;'></iframe>
                                    <br><br>
                                    <button style="
                                        background-color: #007BFF;
                                        color: white;
                                        padding: 10px 20px;
                                        font-size: 16px;
                                        border: none;
                                        border-radius: 8px;
                                        cursor: pointer;
                                        transition: background-color 0.3s ease;"
                                        onmouseover="this.style.backgroundColor='#0056b3';"
                                        onmouseout="this.style.backgroundColor='#007BFF';"
                                        onclick="document.getElementById('mapaFrame').requestFullscreen()">
                                        Ver en pantalla completa
                                    </button>
                                </div>
                                """
                                components.html(iframe, height=680)
                        else:
                            st.error("No se pudo generar el mapa interactivo.")
    
                    # Ruta estática usando la clase Graficar
                    with tab2:
                        st.subheader("Tramos de Ruta Óptima")
                        graficador = Graficar(mapa, solucion)
                        for i in range(1, len(solucion["Ruta"])):
                            st.markdown(f"**Tramo {i}:**")
                            fig = graficador.graficar_una(i)
                            st.pyplot(fig)
    
                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")

