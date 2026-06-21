import os
import wave
import array
import shutil
import io
import tempfile
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import winsound

# ================= VERSIÓN =================
VERSION = "0.8 (Filter & Sort Implementation)"

# ================= DICCIONARIO DE IDIOMAS =================
TEXTOS = {
    "Español": {
        "titulo": "Diogenes Audio Mod",
        "carpeta": "Carpeta de origen:",
        "explorar": "Explorar...",
        "cortar": "Segundos a cortar (inicio):",
        "volumen": "Volumen (%):",
        "normalizar": "Normalizar al pico máximo",
        "sufijo": "Sufijo al guardar (ej. _C4):",
        "oto": "Generar oto.ini base",
        "metodo": "Método:",
        "cargar_oto": "Cargar OTO.ini",
        "sel_todas": "☑ Seleccionar Todas",
        "des_todas": "☐ Deseleccionar Todas",
        "filtro_lbl": "Filtrar por:",
        "filtro_az": "A-Z",
        "filtro_za": "Z-A",
        "filtro_new": "Más Recientes",
        "filtro_old": "Más Antiguos",
        "lista_audios": "Lista de Audios:",
        "previsualizar": "Previsualizar Modificaciones",
        "procesando_tit": "Procesando Audios...",
        "procesando_txt": "Generando: {} de {}",
        "guardar_solo": "Guardar SOLO Modificados",
        "guardar_todos": "Guardar TODOS (Mod. + Orig.)",
        "titulo_prev": "Audios Modificados (Escúchalos antes de guardar):",
        "ayuda_tit": "Ayuda y Guía de Uso",
        "ayuda_txt": (
            "GUÍA RÁPIDA DE USO:\n\n"
            "1. Carpeta de origen: Selecciona la carpeta donde guardaste tus grabaciones originales (.wav).\n\n"
            "2. Segundos a cortar: Elimina tiempos muertos, respiraciones o clics del ratón al inicio de la grabación. Usa los botones + o - para ser preciso.\n\n"
            "3. Volumen y Normalizar: \n"
            "   - 'Volumen' ajusta el sonido usando un porcentaje fijo.\n"
            "   - 'Normalizar' ignora el % y sube el audio al máximo volumen posible sin que se sature o distorsione (Muy Recomendado).\n\n"
            "4. Sufijo: Texto que se pegará al final de cada archivo. Por ejemplo, si escribes '_C4', tu audio 'ka.wav' se guardará como 'ka_C4.wav' (Ideal para grabar Voicebanks Multipitch).\n\n"
            "5. OTO.ini Base:\n"
            "   - Selecciona el Método (CV, VCV, etc.) para que la aplicación escriba automáticamente el nombre de las sílabas con el formato correcto.\n"
            "   - Cargar OTO: Si subes el archivo 'oto.ini' de una versión anterior de tu Voicebank, el programa copiará inteligentemente todos tus números (Offset, Overlap, Consonant, etc.) para los nuevos audios, ahorrándote horas de trabajo."
        ),
        "msg_sel_todas": "Todas las casillas ya están seleccionadas.",
        "msg_des_todas": "Todas las casillas ya están deseleccionadas.",
        "msg_sin_audios": "No hay audios cargados en la lista para procesar.",
        "msg_error_num": "Asegúrate de poner números válidos en los campos de Segundos y Volumen.",
        "msg_error_proc": "Ocurrieron errores al procesar algunos archivos.",
        "msg_sin_sel": "No has marcado ningún audio en la lista para modificar.",
        "msg_exito": "¡Éxito! Archivos y OTO generados en:\n\n",
        "msg_dir_tit": "Selecciona dónde quieres crear la nueva carpeta",
        "msg_nombre_tit": "Nombre de la Carpeta",
        "msg_nombre_txt": "¿Qué nombre quieres ponerle a tu nueva carpeta?\n(Si lo dejas en blanco, se usará el nombre por defecto)",
        "def_folder": "Voicebank_Procesado",
        "msg_oto_exito": "Archivo OTO.ini enlazado correctamente.\nMétodo detectado automáticamente:",
        "msg_oto_quitado": "El archivo OTO.ini fue descartado de la memoria."
    },
    "English": {
        "titulo": "Diogenes Audio Mod",
        "carpeta": "Source Folder:",
        "explorar": "Browse...",
        "cortar": "Seconds to trim (start):",
        "volumen": "Volume (%):",
        "normalizar": "Normalize to max peak",
        "sufijo": "Suffix on save (e.g. _C4):",
        "oto": "Generate base oto.ini",
        "metodo": "Method:",
        "cargar_oto": "Load OTO.ini",
        "sel_todas": "☑ Select All",
        "des_todas": "☐ Deselect All",
        "filtro_lbl": "Sort by:",
        "filtro_az": "A-Z",
        "filtro_za": "Z-A",
        "filtro_new": "Newest First",
        "filtro_old": "Oldest First",
        "lista_audios": "Audio List:",
        "previsualizar": "Preview Modifications",
        "procesando_tit": "Processing Audios...",
        "procesando_txt": "Generating: {} of {}",
        "guardar_solo": "Save ONLY Modified",
        "guardar_todos": "Save ALL (Mod. + Orig.)",
        "titulo_prev": "Modified Audios (Listen before saving):",
        "ayuda_tit": "Help & Quick Guide",
        "ayuda_txt": (
            "QUICK USER GUIDE:\n\n"
            "1. Source Folder: Select the folder containing your original .wav recordings.\n\n"
            "2. Seconds to trim: Remove dead time, breaths, or mouse clicks from the start of the audio using the + and - buttons.\n\n"
            "3. Volume & Normalize: \n"
            "   - 'Volume' adjusts the gain using a fixed percentage.\n"
            "   - 'Normalize' ignores the % and boosts the audio to the maximum safe peak without clipping (Highly Recommended).\n\n"
            "4. Suffix: Text appended to the end of each file. Ex: Typing '_C4' changes 'ka.wav' into 'ka_C4.wav' (Perfect for Multipitch Voicebanks).\n\n"
            "5. Base OTO.ini:\n"
            "   - Select the Method (CV, VCV, etc.) so the app automatically writes the alias with the correct format.\n"
            "   - Load OTO: If you upload a previous 'oto.ini', the software will intelligently inherit all your numerical parameters (Offset, Overlap, Consonant, etc.) for the new audios, saving you hours of configuration."
        ),
        "msg_sel_todas": "All checkboxes are already selected.",
        "msg_des_todas": "All checkboxes are already deselected.",
        "msg_sin_audios": "No audios loaded in the list to process.",
        "msg_error_num": "Make sure to enter valid numbers in Seconds and Volume.",
        "msg_error_proc": "There were errors processing some files.",
        "msg_sin_sel": "You haven't checked any audio to modify.",
        "msg_exito": "Success! Files and OTO generated at:\n\n",
        "msg_dir_tit": "Select where you want to create the new folder",
        "msg_nombre_tit": "Folder Name",
        "msg_nombre_txt": "What do you want to name your new folder?\n(If left blank, the default name will be used)",
        "def_folder": "Processed_Voicebank",
        "msg_oto_exito": "OTO.ini file successfully linked.\nAutomatically detected method:",
        "msg_oto_quitado": "OTO.ini file discarded from memory."
    },
    "Português": {
        "titulo": "Diogenes Audio Mod",
        "carpeta": "Pasta de origem:",
        "explorar": "Procurar...",
        "cortar": "Segundos para cortar (início):",
        "volumen": "Volume (%):",
        "normalizar": "Normalizar pico máximo",
        "sufijo": "Sufixo ao salvar (ex. _C4):",
        "oto": "Gerar oto.ini base",
        "metodo": "Método:",
        "cargar_oto": "Carregar OTO.ini",
        "sel_todas": "☑ Selecionar Todas",
        "des_todas": "☐ Desmarcar Todas",
        "filtro_lbl": "Ordenar por:",
        "filtro_az": "A-Z",
        "filtro_za": "Z-A",
        "filtro_new": "Mais Recentes",
        "filtro_old": "Mais Antigos",
        "lista_audios": "Lista de Áudios:",
        "previsualizar": "Pré-visualizar Mudanças",
        "procesando_tit": "Processando Áudios...",
        "procesando_txt": "Gerando: {} de {}",
        "guardar_solo": "Salvar SÓ Modificados",
        "guardar_todos": "Salvar TODOS (Mod. + Orig.)",
        "titulo_prev": "Áudios Modificados (Ouça antes de salvar):",
        "ayuda_tit": "Ajuda e Guia Rápido",
        "ayuda_txt": (
            "GUIA RÁPIDO DE USO:\n\n"
            "1. Pasta de origem: Selecione a pasta com suas gravações originais (.wav).\n\n"
            "2. Segundos para cortar: Elimina tempos mortos, respirações ou cliques no início do áudio. Use os botões + ou -.\n\n"
            "3. Volume e Normalizar: \n"
            "   - 'Volume' ajusta o ganho usando uma porcentagem fixa.\n"
            "   - 'Normalizar' ignora o % e aumenta o áudio para o pico máximo seguro sem distorcer (Muito Recomendado).\n\n"
            "4. Sufixo: Texto anexado ao final de cada arquivo. Ex: Se você digitar '_C4', seu áudio 'ka.wav' será salvo como 'ka_C4.wav' (Ideal para Multipitch).\n\n"
            "5. OTO.ini Base:\n"
            "   - Selecione o Método (CV, VCV, etc.) para que o app escreva os nomes das sílabas no formato correto.\n"
            "   - Carregar OTO: Se você enviar um 'oto.ini' anterior, o programa herdará inteligentemente todos os seus números (Offset, Overlap, Consonant, etc.) para os novos áudios."
        ),
        "msg_sel_todas": "Todas as caixas já estão selecionadas.",
        "msg_des_todas": "Todas as caixas já estão desmarcadas.",
        "msg_sin_audios": "Não há áudios carregados na lista para processar.",
        "msg_error_num": "Certifique-se de inserir números válidos em Segundos e Volume.",
        "msg_error_proc": "Houve erros ao processar alguns arquivos.",
        "msg_sin_sel": "Você não marcou nenhum áudio para modificar.",
        "msg_exito": "Sucesso! Arquivos e OTO gerados em:\n\n",
        "msg_dir_tit": "Selecione onde deseja criar a nova pasta",
        "msg_nombre_tit": "Nome da Pasta",
        "msg_nombre_txt": "Que nome deseja dar à sua nova pasta?\n(Se deixado em branco, o nome padrão será usado)",
        "def_folder": "Voicebank_Processado",
        "msg_oto_exito": "Arquivo OTO.ini vinculado com sucesso.\nMétodo detectado automaticamente:",
        "msg_oto_quitado": "Arquivo OTO.ini descartado da memória."
    }
}

class EditorAudioApp:
    def __init__(self, root):
        self.root = root
        self.idioma_actual = "Español"
        
        # Configuración Visual CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.geometry("820x850")
        
        # Paleta de Colores Uniforme
        self.PURPLE_BASE = "#36165e" 
        self.PURPLE_HOVER = "#552791"
        self.RED_BASE = "#7a1a1a"
        self.RED_HOVER = "#a82424"
        self.GRAY_FRAME = "#1e1e1e"
        self.GRAY_INNER = "#2b2b2b"
        self.FONT_MAIN = ("Roboto", 13)
        self.FONT_TITLE = ("Roboto", 14, "bold")
        
        self.carpeta_base = ""
        self.archivos_data = [] 
        self.audios_memoria = {} 
        self.custom_oto_data = {} 
        self.metodo_origen_oto = "CV" 
        
        self.filtro_actual = "A-Z"
        self.filtro_prev_actual = "A-Z"
        
        self.btn_reproduciendo = None
        self.after_id = None 
        self.ruta_temp = os.path.join(tempfile.gettempdir(), "temp_preview_audio.wav")

        self.crear_interfaz_principal()
        self.actualizar_textos()

    def t(self, clave):
        return TEXTOS[self.idioma_actual][clave]

    def cambiar_idioma(self, valor):
        self.idioma_actual = valor
        self.actualizar_textos()

    def _get_filter_text(self, internal_filter):
        mapping = {
            "A-Z": "filtro_az",
            "Z-A": "filtro_za",
            "NEW": "filtro_new",
            "OLD": "filtro_old"
        }
        return self.t(mapping.get(internal_filter, "filtro_az"))

    def actualizar_textos(self):
        self.root.title(f"{self.t('titulo')} v{VERSION}")
        self.lbl_carpeta.configure(text=self.t("carpeta"))
        self.btn_explorar.configure(text=self.t("explorar"))
        self.lbl_cortar.configure(text=self.t("cortar"))
        self.lbl_volumen.configure(text=self.t("volumen"))
        self.chk_normalizar.configure(text=self.t("normalizar"))
        self.lbl_sufijo.configure(text=self.t("sufijo"))
        self.chk_oto.configure(text=self.t("oto"))
        self.lbl_metodo.configure(text=self.t("metodo"))
        self.btn_cargar_oto.configure(text=self.t("cargar_oto"))
        self.btn_sel_todas.configure(text=self.t("sel_todas"))
        self.btn_des_todas.configure(text=self.t("des_todas"))
        
        self.lbl_filtro.configure(text=self.t("filtro_lbl"))
        filtros_lista = [self.t("filtro_az"), self.t("filtro_za"), self.t("filtro_new"), self.t("filtro_old")]
        self.combo_filtro.configure(values=filtros_lista)
        self.combo_filtro.set(self._get_filter_text(self.filtro_actual))
        
        self.lbl_lista.configure(text=self.t("lista_audios"))
        self.btn_previsualizar.configure(text=self.t("previsualizar"))

    # ================= SISTEMA DE ALERTAS PERSONALIZADAS CTK =================
    def mostrar_alerta(self, titulo, mensaje, tipo="info"):
        alerta = ctk.CTkToplevel(self.root)
        alerta.title(titulo)
        alerta.geometry("400x220")
        alerta.resizable(False, False)
        alerta.transient(self.root)
        alerta.grab_set()
        
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 110
        alerta.geometry(f"+{x}+{y}")
        
        color_titulo = self.PURPLE_BASE if tipo == "info" else self.RED_BASE
        
        ctk.CTkLabel(alerta, text=titulo, font=self.FONT_TITLE, text_color=color_titulo).pack(pady=(20, 5))
        ctk.CTkLabel(alerta, text=mensaje, font=self.FONT_MAIN, wraplength=340).pack(expand=True, padx=20, pady=5)
        
        btn_ok = ctk.CTkButton(alerta, text="OK", width=120, fg_color=self.GRAY_INNER, hover_color="#444444", command=alerta.destroy)
        btn_ok.pack(pady=(0, 20))

    def mostrar_ayuda(self):
        ayuda_win = ctk.CTkToplevel(self.root)
        ayuda_win.title(self.t("ayuda_tit"))
        ayuda_win.geometry("580x480")
        ayuda_win.transient(self.root)
        ayuda_win.grab_set()
        
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 290
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 240
        ayuda_win.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(ayuda_win, text=self.t("ayuda_tit"), font=("Roboto", 18, "bold"), text_color=self.PURPLE_HOVER).pack(pady=(20, 10))
        
        txt_box = ctk.CTkTextbox(ayuda_win, font=self.FONT_MAIN, width=520, height=350, fg_color=self.GRAY_FRAME, wrap="word", corner_radius=10)
        txt_box.pack(padx=20, pady=10)
        txt_box.insert("0.0", self.t("ayuda_txt"))
        txt_box.configure(state="disabled") 

    def crear_interfaz_principal(self):
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- PANEL SUPERIOR ---
        panel_superior = ctk.CTkFrame(main_container, fg_color=self.GRAY_FRAME, corner_radius=10)
        panel_superior.pack(fill="x", pady=(0, 15))
        
        panel_inner = ctk.CTkFrame(panel_superior, fg_color="transparent")
        panel_inner.pack(fill="x", padx=20, pady=15)

        # Fila 0: Idioma y Ayuda
        frame_top = ctk.CTkFrame(panel_inner, fg_color="transparent")
        frame_top.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(frame_top, text="🌐", font=self.FONT_MAIN).pack(side="left")
        
        self.combo_idioma = ctk.CTkComboBox(frame_top, values=["Español", "English", "Português"], 
                                            state="readonly", width=120, font=self.FONT_MAIN,
                                            fg_color=self.PURPLE_BASE, border_color=self.PURPLE_HOVER, 
                                            button_color=self.PURPLE_BASE, button_hover_color=self.PURPLE_HOVER,
                                            command=self.cambiar_idioma)
        self.combo_idioma.set("Español")
        self.combo_idioma.pack(side="left", padx=10)
        
        ctk.CTkButton(frame_top, text="❓", width=35, font=self.FONT_TITLE, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=self.mostrar_ayuda).pack(side="right")

        def create_row(parent):
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", pady=6)
            return row

        # Fila 1: Carpeta
        row1 = create_row(panel_inner)
        self.lbl_carpeta = ctk.CTkLabel(row1, text="", font=self.FONT_MAIN, width=170, anchor="w")
        self.lbl_carpeta.pack(side="left")
        self.ent_carpeta = ctk.CTkEntry(row1, font=self.FONT_MAIN)
        self.ent_carpeta.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.btn_explorar = ctk.CTkButton(row1, text="", font=self.FONT_MAIN, width=110, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=self.seleccionar_carpeta)
        self.btn_explorar.pack(side="right")

        # Fila 2: Segundos a cortar (+/- Steppers)
        row2 = create_row(panel_inner)
        self.lbl_cortar = ctk.CTkLabel(row2, text="", font=self.FONT_MAIN, width=170, anchor="w")
        self.lbl_cortar.pack(side="left")
        
        frame_sec_stepper = ctk.CTkFrame(row2, fg_color="transparent")
        frame_sec_stepper.pack(side="left")
        
        ctk.CTkButton(frame_sec_stepper, text="-", width=30, font=self.FONT_TITLE, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=self.decrementar_segundos).pack(side="left")
        self.ent_segundos = ctk.CTkEntry(frame_sec_stepper, width=60, font=self.FONT_MAIN, justify="center")
        self.ent_segundos.insert(0, "1.0")
        self.ent_segundos.pack(side="left", padx=5)
        ctk.CTkButton(frame_sec_stepper, text="+", width=30, font=self.FONT_TITLE, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=self.incrementar_segundos).pack(side="left")

        # Fila 3: Volumen (+/- Steppers)
        row3 = create_row(panel_inner)
        self.lbl_volumen = ctk.CTkLabel(row3, text="", font=self.FONT_MAIN, width=170, anchor="w")
        self.lbl_volumen.pack(side="left")
        
        frame_vol_stepper = ctk.CTkFrame(row3, fg_color="transparent")
        frame_vol_stepper.pack(side="left")
        
        ctk.CTkButton(frame_vol_stepper, text="-", width=30, font=self.FONT_TITLE, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=self.decrementar_volumen).pack(side="left")
        self.ent_volumen = ctk.CTkEntry(frame_vol_stepper, width=60, font=self.FONT_MAIN, justify="center")
        self.ent_volumen.insert(0, "100")
        self.ent_volumen.pack(side="left", padx=5)
        ctk.CTkButton(frame_vol_stepper, text="+", width=30, font=self.FONT_TITLE, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=self.incrementar_volumen).pack(side="left")
        
        self.var_normalizar = tk.BooleanVar(value=False)
        self.chk_normalizar = ctk.CTkCheckBox(row3, text="", variable=self.var_normalizar, font=self.FONT_MAIN, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER)
        self.chk_normalizar.pack(side="left", padx=20)

        # Fila 4: Sufijo
        row4 = create_row(panel_inner)
        self.lbl_sufijo = ctk.CTkLabel(row4, text="", font=self.FONT_MAIN, width=170, anchor="w")
        self.lbl_sufijo.pack(side="left")
        self.ent_sufijo = ctk.CTkEntry(row4, width=130, font=self.FONT_MAIN)
        self.ent_sufijo.pack(side="left")

        # Fila 5: Opciones OTO.ini
        row5 = create_row(panel_inner)
        self.var_oto = tk.BooleanVar(value=True)
        self.chk_oto = ctk.CTkCheckBox(row5, text="", variable=self.var_oto, font=self.FONT_TITLE, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=self.toggle_estado_oto)
        self.chk_oto.pack(side="left")

        self.lbl_metodo = ctk.CTkLabel(row5, text="", font=self.FONT_MAIN)
        self.lbl_metodo.pack(side="left", padx=(15, 5))

        self.combo_metodo = ctk.CTkComboBox(row5, values=["CV", "VCV", "CVVC", "VCCV"], state="readonly", width=85, font=self.FONT_MAIN, fg_color=self.PURPLE_BASE, border_color=self.PURPLE_HOVER, button_color=self.PURPLE_BASE, button_hover_color=self.PURPLE_HOVER)
        self.combo_metodo.set("CV")
        self.combo_metodo.pack(side="left", padx=5)

        self.btn_cargar_oto = ctk.CTkButton(row5, text="", width=120, font=self.FONT_MAIN, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=self.cargar_oto_personalizado)
        self.btn_cargar_oto.pack(side="left", padx=10)

        self.lbl_oto_estado = ctk.CTkLabel(row5, text="[-]", text_color="gray", font=self.FONT_MAIN)
        self.lbl_oto_estado.pack(side="left")

        self.btn_quitar_oto = ctk.CTkButton(row5, text="❌", width=30, fg_color=self.RED_BASE, hover_color=self.RED_HOVER, command=self.quitar_oto_personalizado)

        # --- PANEL DE SELECCIÓN Y FILTROS ---
        frame_selecciones = ctk.CTkFrame(main_container, fg_color="transparent")
        frame_selecciones.pack(fill="x", pady=(5, 5))
        
        self.btn_sel_todas = ctk.CTkButton(frame_selecciones, text="", width=150, font=self.FONT_MAIN, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=lambda: self._cambiar_seleccion_todas(True))
        self.btn_sel_todas.pack(side="left", padx=(0, 10))
        self.btn_des_todas = ctk.CTkButton(frame_selecciones, text="", width=150, font=self.FONT_MAIN, fg_color=self.GRAY_INNER, hover_color="#444444", command=lambda: self._cambiar_seleccion_todas(False))
        self.btn_des_todas.pack(side="left")
        
        frame_filtro = ctk.CTkFrame(main_container, fg_color="transparent")
        frame_filtro.pack(fill="x", pady=(5, 5))
        
        self.lbl_filtro = ctk.CTkLabel(frame_filtro, text="", font=self.FONT_MAIN)
        self.lbl_filtro.pack(side="left", padx=(0, 10))
        self.combo_filtro = ctk.CTkComboBox(frame_filtro, values=["A-Z"], state="readonly", width=140, font=self.FONT_MAIN, fg_color=self.GRAY_INNER, border_color=self.PURPLE_BASE, button_color=self.PURPLE_BASE, button_hover_color=self.PURPLE_HOVER, command=self.aplicar_filtro_lista)
        self.combo_filtro.pack(side="left")

        # --- PANEL CENTRAL (SCROLL MODERNO) ---
        self.lbl_lista = ctk.CTkLabel(main_container, text="", font=self.FONT_TITLE)
        self.lbl_lista.pack(anchor="w", pady=(5, 5))
        
        self.frame_interior = ctk.CTkScrollableFrame(main_container, fg_color=self.GRAY_FRAME, corner_radius=10)
        self.frame_interior.pack(fill="both", expand=True)

        # --- PANEL INFERIOR ---
        self.btn_previsualizar = ctk.CTkButton(main_container, text="", font=("Roboto", 15, "bold"), height=45, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER, command=self.previsualizar)
        self.btn_previsualizar.pack(pady=(15, 0))

    # ================= FUNCIONES DE LOS BOTONES +/- =================
    def incrementar_segundos(self):
        try:
            val = float(self.ent_segundos.get())
            self.ent_segundos.delete(0, 'end')
            self.ent_segundos.insert(0, str(round(val + 0.5, 1)))
        except ValueError: pass

    def decrementar_segundos(self):
        try:
            val = float(self.ent_segundos.get())
            if val >= 0.5:
                self.ent_segundos.delete(0, 'end')
                self.ent_segundos.insert(0, str(round(val - 0.5, 1)))
        except ValueError: pass

    def incrementar_volumen(self):
        try:
            val = int(self.ent_volumen.get())
            self.ent_volumen.delete(0, 'end')
            self.ent_volumen.insert(0, str(val + 10))
        except ValueError: pass

    def decrementar_volumen(self):
        try:
            val = int(self.ent_volumen.get())
            if val >= 10:
                self.ent_volumen.delete(0, 'end')
                self.ent_volumen.insert(0, str(val - 10))
        except ValueError: pass

    def toggle_estado_oto(self):
        estado = "normal" if self.var_oto.get() else "disabled"
        self.combo_metodo.configure(state="readonly" if self.var_oto.get() else "disabled")
        self.btn_cargar_oto.configure(state=estado)
        if not self.var_oto.get() and self.custom_oto_data:
            self.quitar_oto_personalizado(mostrar_aviso=False)

    # ================= LÓGICA OTO.INI CUSTOM =================
    def cargar_oto_personalizado(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos INI", "*.ini")])
        if not ruta: return

        self.custom_oto_data.clear()
        conteo_vcv = 0
        conteo_cvvc = 0

        try:
            with open(ruta, 'r', encoding='shift_jis', errors='ignore') as f:
                lineas = f.readlines()

            for linea in lineas:
                linea = linea.strip()
                if not linea or "=" not in linea: continue

                partes = linea.split("=")
                wav_name = partes[0]
                resto = partes[1].split(",")

                alias = resto[0]
                params = resto[1:] if len(resto) > 1 else ["0","0","0","0","0"]

                if wav_name not in self.custom_oto_data:
                    self.custom_oto_data[wav_name] = []
                
                self.custom_oto_data[wav_name].append({"alias": alias, "params": params})

                if alias.startswith("- ") or " " in alias:
                    if len(alias.split(" ")) == 2:
                        p1, p2 = alias.split(" ")
                        if p1 in ["-", "a", "i", "u", "e", "o", "n"]:
                            conteo_vcv += 1
                        else:
                            conteo_cvvc += 1

            total_entradas = sum(len(v) for v in self.custom_oto_data.values())
            self.metodo_origen_oto = "CV"
            if total_entradas > 0:
                if conteo_vcv > total_entradas * 0.3:
                    self.metodo_origen_oto = "VCV"
                elif conteo_cvvc > total_entradas * 0.3:
                    self.metodo_origen_oto = "CVVC"

            self.combo_metodo.set(self.metodo_origen_oto)
            self.lbl_oto_estado.configure(text=f"[{os.path.basename(ruta)}]", text_color="#2ECC71")
            self.btn_quitar_oto.pack(side="left", padx=5)
            self.mostrar_alerta("OTO.ini", f"{self.t('msg_oto_exito')} {self.metodo_origen_oto}")

        except Exception as e:
            self.mostrar_alerta("Error", f"Error al leer OTO.ini: {e}", tipo="error")

    def quitar_oto_personalizado(self, mostrar_aviso=True):
        self.custom_oto_data.clear()
        self.metodo_origen_oto = "CV"
        self.combo_metodo.set("CV")
        self.lbl_oto_estado.configure(text="[-]", text_color="gray")
        self.btn_quitar_oto.pack_forget()
        if mostrar_aviso:
            self.mostrar_alerta("Aviso", self.t("msg_oto_quitado"))

    def formatear_alias(self, alias_original, nombre_base, metodo_destino):
        if self.metodo_origen_oto == metodo_destino:
            return alias_original

        alias_limpio = alias_original
        if self.metodo_origen_oto == "VCV" and (" " in alias_original):
            alias_limpio = alias_original.split(" ", 1)[-1]

        if metodo_destino == "VCV":
            return f"- {alias_limpio}"
        else:
            return alias_limpio

    # ================= LÓGICA DE FILTROS =================
    def aplicar_filtro_lista(self, valor):
        if valor == self.t("filtro_az"):
            self.filtro_actual = "A-Z"
        elif valor == self.t("filtro_za"):
            self.filtro_actual = "Z-A"
        elif valor == self.t("filtro_new"):
            self.filtro_actual = "NEW"
        elif valor == self.t("filtro_old"):
            self.filtro_actual = "OLD"
        
        self.renderizar_lista_audios()

    def _ordenar_datos(self, data_list, filtro):
        if filtro == "A-Z":
            data_list.sort(key=lambda x: x["nombre"].lower())
        elif filtro == "Z-A":
            data_list.sort(key=lambda x: x["nombre"].lower(), reverse=True)
        elif filtro == "NEW":
            data_list.sort(key=lambda x: x["mtime"], reverse=True)
        elif filtro == "OLD":
            data_list.sort(key=lambda x: x["mtime"])

    # ================= LÓGICA DE SELECCIÓN =================
    def _cambiar_seleccion_todas(self, estado_deseado):
        if not self.archivos_data: return
        if all(dato["var"].get() == estado_deseado for dato in self.archivos_data):
            msg_clave = "msg_sel_todas" if estado_deseado else "msg_des_todas"
            self.mostrar_alerta("Aviso", self.t(msg_clave))
        else:
            for dato in self.archivos_data: 
                dato["var"].set(estado_deseado)

    # ================= LÓGICA DE REPRODUCCIÓN =================
    def detener_audio(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        if self.btn_reproduciendo:
            self.btn_reproduciendo.configure(text="▶", fg_color=self.GRAY_INNER, hover_color="#444444")
            self.btn_reproduciendo = None

    def auto_reset_boton(self):
        if self.btn_reproduciendo:
            self.btn_reproduciendo.configure(text="▶", fg_color=self.GRAY_INNER, hover_color="#444444")
            self.btn_reproduciendo = None
        self.after_id = None

    def calcular_duracion_ms(self, fuente, es_memoria=False):
        try:
            fuente_abrir = io.BytesIO(fuente) if es_memoria else fuente
            with wave.open(fuente_abrir, 'rb') as w:
                return int((w.getnframes() / w.getframerate()) * 1000)
        except Exception:
            return 1000

    def _toggle_reproducir(self, fuente, btn, es_memoria):
        if self.btn_reproduciendo == btn:
            self.detener_audio()
            return
            
        self.detener_audio()
        self.btn_reproduciendo = btn
        btn.configure(text="⏹", fg_color=self.RED_BASE, hover_color=self.RED_HOVER)
        
        if es_memoria:
            with open(self.ruta_temp, "wb") as f:
                f.write(fuente)
            ruta_reproducir = self.ruta_temp
        else:
            ruta_reproducir = fuente
            
        duracion_ms = self.calcular_duracion_ms(fuente, es_memoria)
        winsound.PlaySound(ruta_reproducir, winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.after_id = self.root.after(duracion_ms, self.auto_reset_boton)

    # ================= LÓGICA PRINCIPAL =================
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.carpeta_base = carpeta
            self.ent_carpeta.delete(0, 'end')
            self.ent_carpeta.insert(0, carpeta)
            self.cargar_lista_audios()

    def cargar_lista_audios(self):
        self.archivos_data.clear()
        
        for raiz, _, archivos in os.walk(self.carpeta_base):
            for archivo in archivos:
                if archivo.lower().endswith(".wav"):
                    ruta_abs = os.path.join(raiz, archivo)
                    ruta_rel = os.path.relpath(ruta_abs, self.carpeta_base)
                    mtime = os.path.getmtime(ruta_abs)
                    var_check = tk.BooleanVar(value=True)
                    
                    self.archivos_data.append({
                        "nombre": archivo, 
                        "ruta_absoluta": ruta_abs, 
                        "ruta_relativa": ruta_rel, 
                        "mtime": mtime,
                        "var": var_check
                    })
                    
        self.renderizar_lista_audios()

    def renderizar_lista_audios(self):
        for widget in self.frame_interior.winfo_children(): widget.destroy()
        self._ordenar_datos(self.archivos_data, self.filtro_actual)
        
        for dato in self.archivos_data:
            row_frame = ctk.CTkFrame(self.frame_interior, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            chk = ctk.CTkCheckBox(row_frame, text="", variable=dato["var"], width=30, checkbox_width=20, checkbox_height=20, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER)
            chk.pack(side="left", padx=5)
            
            btn_play = ctk.CTkButton(row_frame, text="▶", width=40, font=self.FONT_MAIN, fg_color=self.GRAY_INNER, hover_color="#444444")
            btn_play.configure(command=lambda r=dato["ruta_absoluta"], b=btn_play: self._toggle_reproducir(r, b, es_memoria=False))
            btn_play.pack(side="left", padx=5)
            
            ctk.CTkLabel(row_frame, text=dato["ruta_relativa"], font=self.FONT_MAIN, anchor="w").pack(side="left", fill="x", expand=True)

    def procesar_audio_a_memoria(self, ruta_in, segundos_cortar, porcentaje_vol, normalizar):
        with wave.open(ruta_in, 'rb') as wav_in:
            params = wav_in.getparams()
            if params.sampwidth != 2: raise ValueError("El audio no es de 16-bits.")
            
            framerate = params.framerate
            frames_a_cortar = int(segundos_cortar * framerate)
            
            if params.nframes > frames_a_cortar:
                wav_in.setpos(frames_a_cortar)
                frames_restantes = wav_in.readframes(params.nframes - frames_a_cortar)
            else:
                frames_restantes = b""
                
            muestras = array.array('h', frames_restantes)
            
            if normalizar:
                if muestras:
                    pico_maximo = max(abs(max(muestras)), abs(min(muestras)))
                    factor = 32767.0 / pico_maximo if pico_maximo > 0 else 1.0
                else:
                    factor = 1.0
            else:
                factor = porcentaje_vol / 100.0
                
            for i in range(len(muestras)):
                muestras[i] = max(-32768, min(32767, int(muestras[i] * factor)))
                
        archivo_virtual = io.BytesIO()
        with wave.open(archivo_virtual, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(muestras.tobytes())
            
        return archivo_virtual.getvalue()

    # ================= PANTALLA DE CARGA Y PREVISUALIZACIÓN =================
    def previsualizar(self):
        self.detener_audio()
        if not self.archivos_data:
            self.mostrar_alerta("Aviso", self.t("msg_sin_audios"))
            return
            
        try:
            segundos = float(self.ent_segundos.get())
            volumen = float(self.ent_volumen.get())
            normalizar = self.var_normalizar.get()
        except ValueError:
            self.mostrar_alerta("Error", self.t("msg_error_num"), tipo="error")
            return

        archivos_seleccionados = [dato for dato in self.archivos_data if dato["var"].get()]
        total_seleccionados = len(archivos_seleccionados)
        
        if total_seleccionados == 0:
            self.mostrar_alerta("Aviso", self.t("msg_sin_sel"))
            return

        ventana_carga = ctk.CTkToplevel(self.root)
        ventana_carga.title(self.t("procesando_tit"))
        ventana_carga.geometry("380x180")
        ventana_carga.resizable(False, False)
        
        ventana_carga.transient(self.root)
        ventana_carga.grab_set()
        
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (380 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (180 // 2)
        ventana_carga.geometry(f"+{x}+{y}")
        
        lbl_estado = ctk.CTkLabel(ventana_carga, text=self.t("procesando_tit"), font=self.FONT_TITLE)
        lbl_estado.pack(pady=(30, 10))
        
        progreso = ctk.CTkProgressBar(ventana_carga, width=300, progress_color=self.PURPLE_BASE)
        progreso.pack(pady=10)
        progreso.set(0)
        
        self.audios_memoria.clear()
        errores = 0
        procesados_actuales = 0
        
        for dato in archivos_seleccionados:
            procesados_actuales += 1
            
            txt_progreso = self.t("procesando_txt").format(procesados_actuales, total_seleccionados)
            lbl_estado.configure(text=txt_progreso)
            progreso.set(procesados_actuales / total_seleccionados)
            ventana_carga.update()
            
            try:
                bytes_wav = self.procesar_audio_a_memoria(dato["ruta_absoluta"], segundos, volumen, normalizar)
                self.audios_memoria[dato["ruta_relativa"]] = {
                    "bytes": bytes_wav,
                    "nombre": dato["nombre"],
                    "mtime": dato["mtime"]
                }
            except Exception as e:
                print(f"Error procesando {dato['nombre']}: {e}")
                errores += 1
                
        ventana_carga.destroy()
                    
        if errores > 0: self.mostrar_alerta("Atención", self.t("msg_error_proc"))
        self.abrir_ventana_previsualizacion()

    def abrir_ventana_previsualizacion(self):
        self.ventana_prev = ctk.CTkToplevel(self.root)
        self.ventana_prev.title(self.t("previsualizar"))
        self.ventana_prev.geometry("600x520")
        self.ventana_prev.protocol("WM_DELETE_WINDOW", lambda: (self.detener_audio(), self.ventana_prev.destroy()))
        
        self.ventana_prev.transient(self.root)
        self.ventana_prev.grab_set()
        
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 300
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 260
        self.ventana_prev.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self.ventana_prev, text=self.t("titulo_prev"), font=self.FONT_TITLE).pack(pady=10)
        
        frame_filtro_prev = ctk.CTkFrame(self.ventana_prev, fg_color="transparent")
        frame_filtro_prev.pack(fill="x", padx=20, pady=(0, 5))
        
        ctk.CTkLabel(frame_filtro_prev, text=self.t("filtro_lbl"), font=self.FONT_MAIN).pack(side="left", padx=(0, 10))
        filtros_lista = [self.t("filtro_az"), self.t("filtro_za"), self.t("filtro_new"), self.t("filtro_old")]
        self.combo_filtro_prev = ctk.CTkComboBox(frame_filtro_prev, values=filtros_lista, state="readonly", width=140, font=self.FONT_MAIN, fg_color=self.GRAY_INNER, border_color=self.PURPLE_BASE, button_color=self.PURPLE_BASE, button_hover_color=self.PURPLE_HOVER, command=self.aplicar_filtro_prev)
        self.combo_filtro_prev.set(self._get_filter_text(self.filtro_prev_actual))
        self.combo_filtro_prev.pack(side="left")
        
        self.frame_int_prev = ctk.CTkScrollableFrame(self.ventana_prev, fg_color=self.GRAY_FRAME, corner_radius=10)
        self.frame_int_prev.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.renderizar_lista_prev()
            
        frame_botones = ctk.CTkFrame(self.ventana_prev, fg_color="transparent")
        frame_botones.pack(pady=15)
        
        ctk.CTkButton(frame_botones, text=self.t("guardar_solo"), font=self.FONT_MAIN, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER,
                      command=lambda: self.guardar_audios(solo_modificados=True, ventana=self.ventana_prev)).pack(side="left", padx=10)
        ctk.CTkButton(frame_botones, text=self.t("guardar_todos"), font=self.FONT_MAIN, fg_color=self.PURPLE_BASE, hover_color=self.PURPLE_HOVER,
                      command=lambda: self.guardar_audios(solo_modificados=False, ventana=self.ventana_prev)).pack(side="left", padx=10)

    def aplicar_filtro_prev(self, valor):
        if valor == self.t("filtro_az"):
            self.filtro_prev_actual = "A-Z"
        elif valor == self.t("filtro_za"):
            self.filtro_prev_actual = "Z-A"
        elif valor == self.t("filtro_new"):
            self.filtro_prev_actual = "NEW"
        elif valor == self.t("filtro_old"):
            self.filtro_prev_actual = "OLD"
            
        self.renderizar_lista_prev()

    def renderizar_lista_prev(self):
        for widget in self.frame_int_prev.winfo_children(): widget.destroy()
        
        lista_ordenada = []
        for ruta_rel, info in self.audios_memoria.items():
            lista_ordenada.append({
                "ruta_relativa": ruta_rel,
                "nombre": info["nombre"],
                "mtime": info["mtime"],
                "bytes": info["bytes"]
            })
            
        self._ordenar_datos(lista_ordenada, self.filtro_prev_actual)
        
        for dato in lista_ordenada:
            row_frame = ctk.CTkFrame(self.frame_int_prev, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            btn_play = ctk.CTkButton(row_frame, text="▶", width=40, font=self.FONT_MAIN, fg_color=self.GRAY_INNER, hover_color="#444444")
            btn_play.configure(command=lambda b_wav=dato["bytes"], b=btn_play: self._toggle_reproducir(b_wav, b, es_memoria=True))
            btn_play.pack(side="left", padx=5)
            
            ctk.CTkLabel(row_frame, text=dato["ruta_relativa"], font=self.FONT_MAIN, anchor="w").pack(side="left", fill="x", expand=True)

    # ================= GUARDADO =================
    def guardar_audios(self, solo_modificados, ventana):
        self.detener_audio()
        
        directorio_padre = filedialog.askdirectory(title=self.t("msg_dir_tit"))
        if not directorio_padre: return 
        
        dialog = ctk.CTkInputDialog(text=self.t("msg_nombre_txt"), title=self.t("msg_nombre_tit"))
        nombre_carpeta = dialog.get_input()
        
        if nombre_carpeta is None:
            return 
        elif nombre_carpeta.strip() == "":
            nombre_carpeta = self.t("def_folder")
            
        carpeta_salida = os.path.join(directorio_padre, nombre_carpeta)
        sufijo = self.ent_sufijo.get().strip()
        generar_oto = self.var_oto.get()
        metodo_destino = self.combo_metodo.get()
        carpetas_para_oto = {} 
        
        try:
            for dato in self.archivos_data:
                ruta_in = dato["ruta_absoluta"]
                ruta_rel_original = dato["ruta_relativa"]
                nombre_wav_original = dato["nombre"]
                
                nombre_base, ext = os.path.splitext(nombre_wav_original)
                nuevo_nombre = f"{nombre_base}{sufijo}{ext}"
                
                dir_rel = os.path.dirname(ruta_rel_original)
                ruta_rel_nueva = os.path.join(dir_rel, nuevo_nombre) if dir_rel else nuevo_nombre
                ruta_out = os.path.join(carpeta_salida, ruta_rel_nueva)
                directorio_out = os.path.dirname(ruta_out)
                
                os.makedirs(directorio_out, exist_ok=True)
                esta_seleccionado = dato["var"].get()

                if esta_seleccionado:
                    with open(ruta_out, 'wb') as f:
                        f.write(self.audios_memoria[ruta_rel_original]["bytes"])
                elif not solo_modificados:
                    shutil.copy2(ruta_in, ruta_out)

                if generar_oto and (esta_seleccionado or not solo_modificados):
                    if directorio_out not in carpetas_para_oto:
                        carpetas_para_oto[directorio_out] = []
                        
                    if self.custom_oto_data and nombre_wav_original in self.custom_oto_data:
                        for linea_data in self.custom_oto_data[nombre_wav_original]:
                            alias_viejo = linea_data["alias"]
                            parametros = ",".join(linea_data["params"])
                            
                            alias_adaptado = self.formatear_alias(alias_viejo, nombre_base, metodo_destino)
                            alias_final = f"{alias_adaptado}{sufijo}"
                            
                            linea_oto = f"{nuevo_nombre}={alias_final},{parametros}\n"
                            carpetas_para_oto[directorio_out].append(linea_oto)
                    
                    else:
                        if metodo_destino == "VCV":
                            alias_base = f"- {nombre_base}"
                        else:
                            alias_base = nombre_base
                            
                        alias_final = f"{alias_base}{sufijo}"
                        linea_oto = f"{nuevo_nombre}={alias_final},0,0,0,0,0\n"
                        carpetas_para_oto[directorio_out].append(linea_oto)

            if generar_oto:
                for carpeta_dest, lineas in carpetas_para_oto.items():
                    ruta_oto = os.path.join(carpeta_dest, "oto.ini")
                    with open(ruta_oto, "w", encoding="shift_jis", errors="replace") as f:
                        f.writelines(lineas)

            ventana.destroy()
            self.mostrar_alerta("Proceso Terminado", f"{self.t('msg_exito')}{carpeta_salida}")
        except Exception as e:
            self.mostrar_alerta("Error", f"Error: {e}", tipo="error")

if __name__ == "__main__":
    root = ctk.CTk()
    app = EditorAudioApp(root)
    root.mainloop()