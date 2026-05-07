import os
import wave
import array
import shutil
import io
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk 
import winsound

# ================= VERSIÓN =================
VERSION = "0.2"

# ================= DICCIONARIO DE IDIOMAS =================
TEXTOS = {
    "Español": {
        "titulo": "Diogenes Audio Mod",
        "carpeta": "Carpeta de origen:",
        "explorar": "Explorar...",
        "cortar": "Segundos a cortar (inicio):",
        "volumen": "Volumen (%):",
        "normalizar": "Normalizar al pico máximo (Ignora el %)",
        "sufijo": "Sufijo al guardar (ej. _C4):",
        "oto": "Generar oto.ini base automáticamente",
        "sel_todas": "☑ Seleccionar Todas",
        "des_todas": "☐ Deseleccionar Todas",
        "lista_audios": "Lista de Audios:",
        "previsualizar": "Previsualizar Modificaciones",
        "guardar_solo": "Guardar SOLO Modificados",
        "guardar_todos": "Guardar TODOS (Mod. + Originales)",
        "titulo_prev": "Audios Modificados (Escúchalos antes de guardar):",
        "ayuda_tit": "Ayuda / Guía",
        "ayuda_txt": (
            "Resumen de Funciones:\n\n"
            "• Carpeta de origen: Selecciona la carpeta principal con tus archivos .wav.\n"
            "• Segundos a cortar: Elimina exactamente ese tiempo al inicio de cada audio.\n"
            "• Volumen (%): Sube o baja el volumen de forma fija (100 = Original, 50 = Mitad).\n"
            "• Normalizar: Ignora el %, analiza el audio y sube su volumen al máximo límite posible sin que se distorsione el sonido.\n"
            "• Sufijo: Texto que se añade automáticamente al final de cada archivo guardado (ej. escribir '_C4' cambia 'ka.wav' a 'ka_C4.wav').\n"
            "• Generar oto.ini: Crea un archivo 'oto.ini' codificado en Shift-JIS dentro de la carpeta exportada, con los parámetros en cero listos para UTAU."
        ),
        "msg_sel_todas": "Todas las casillas ya están seleccionadas.",
        "msg_des_todas": "Todas las casillas ya están deseleccionadas.",
        "msg_sin_audios": "No hay audios cargados para procesar.",
        "msg_error_num": "Asegúrate de poner números válidos en segundos y volumen.",
        "msg_error_proc": "Hubo errores al procesar algunos archivos.",
        "msg_sin_sel": "No seleccionaste ningún audio para modificar.",
        "msg_exito": "¡Éxito! Archivos y OTO guardados en:\n",
        "msg_dir_tit": "Selecciona dónde quieres crear la carpeta de resultados",
        "msg_nombre_tit": "Nombre de Carpeta",
        "msg_nombre_txt": "¿Qué nombre quieres ponerle a la carpeta?",
        "def_folder": "Voicebank_Procesado"
    },
    "English": {
        "titulo": "Diogenes Audio Mod",
        "carpeta": "Source Folder:",
        "explorar": "Browse...",
        "cortar": "Seconds to cut (start):",
        "volumen": "Volume (%):",
        "normalizar": "Normalize to max peak (Ignores %)",
        "sufijo": "Suffix on save (e.g. _C4):",
        "oto": "Auto-generate base oto.ini",
        "sel_todas": "☑ Select All",
        "des_todas": "☐ Deselect All",
        "lista_audios": "Audio List:",
        "previsualizar": "Preview Modifications",
        "guardar_solo": "Save ONLY Modified",
        "guardar_todos": "Save ALL (Mod. + Originals)",
        "titulo_prev": "Modified Audios (Listen before saving):",
        "ayuda_tit": "Help / Guide",
        "ayuda_txt": (
            "App Features Overview:\n\n"
            "• Source Folder: Select the root folder containing your .wav files.\n"
            "• Seconds to cut: Trims the specified exact time from the start of each audio.\n"
            "• Volume (%): Changes the volume by a fixed multiplier (100 = Original, 50 = Half).\n"
            "• Normalize: Ignores %, analyzes each audio, and boosts it to its maximum safe peak without distortion.\n"
            "• Suffix: Text appended to the end of each saved file name (e.g., typing '_C4' turns 'ka.wav' into 'ka_C4.wav').\n"
            "• Generate oto.ini: Creates an 'oto.ini' file (Shift-JIS encoded) in the output folder with base parameters (0,0,0,0,0) ready for UTAU."
        ),
        "msg_sel_todas": "All checkboxes are already selected.",
        "msg_des_todas": "All checkboxes are already deselected.",
        "msg_sin_audios": "No audios loaded to process.",
        "msg_error_num": "Make sure to enter valid numbers in seconds and volume.",
        "msg_error_proc": "There were errors processing some files.",
        "msg_sin_sel": "You didn't select any audio to modify.",
        "msg_exito": "Success! Files and OTO saved to:\n",
        "msg_dir_tit": "Select where you want to create the output folder",
        "msg_nombre_tit": "Folder Name",
        "msg_nombre_txt": "What do you want to name the folder?",
        "def_folder": "Processed_Voicebank"
    },
    "Português": {
        "titulo": "Diogenes Audio Mod",
        "carpeta": "Pasta de origem:",
        "explorar": "Procurar...",
        "cortar": "Segundos para cortar (início):",
        "volumen": "Volume (%):",
        "normalizar": "Normalizar para o pico máximo (Ignora o %)",
        "sufijo": "Sufixo ao salvar (ex. _C4):",
        "oto": "Gerar oto.ini base automaticamente",
        "sel_todas": "☑ Selecionar Todas",
        "des_todas": "☐ Desmarcar Todas",
        "lista_audios": "Lista de Áudios:",
        "previsualizar": "Pré-visualizar Modificações",
        "guardar_solo": "Salvar APENAS Modificados",
        "guardar_todos": "Salvar TODOS (Mod. + Originais)",
        "titulo_prev": "Áudios Modificados (Ouça antes de salvar):",
        "ayuda_tit": "Ajuda / Guia",
        "ayuda_txt": (
            "Visão Geral das Funções:\n\n"
            "• Pasta de origem: Selecione a pasta principal com os seus arquivos .wav.\n"
            "• Segundos para cortar: Elimina o tempo exato do início de cada áudio.\n"
            "• Volume (%): Altera o volume de forma fixa (100 = Original, 50 = Metade).\n"
            "• Normalizar: Ignora o %, analisa cada áudio e aumenta para o pico máximo seguro sem distorcer.\n"
            "• Sufixo: Texto anexado ao final de cada arquivo salvo (ex: digitar '_C4' muda 'ka.wav' para 'ka_C4.wav').\n"
            "• Gerar oto.ini: Cria um arquivo 'oto.ini' codificado em Shift-JIS na pasta de saída com parâmetros base (0,0,0,0,0) pronto para UTAU."
        ),
        "msg_sel_todas": "Todas as caixas já estão selecionadas.",
        "msg_des_todas": "Todas as caixas já estão desmarcadas.",
        "msg_sin_audios": "Não há áudios carregados para processar.",
        "msg_error_num": "Certifique-se de inserir números válidos em segundos e volume.",
        "msg_error_proc": "Houve erros ao processar alguns arquivos.",
        "msg_sin_sel": "Você não selecionou nenhum áudio para modificar.",
        "msg_exito": "Sucesso! Arquivos e OTO salvos em:\n",
        "msg_dir_tit": "Selecione onde deseja criar a pasta de resultados",
        "msg_nombre_tit": "Nome da Pasta",
        "msg_nombre_txt": "Que nome deseja dar à pasta?",
        "def_folder": "Voicebank_Processado"
    }
}

class EditorAudioApp:
    def __init__(self, root):
        self.root = root
        self.idioma_actual = "Español" # Idioma por defecto
        
        self.root.geometry("700x750")
        
        self.carpeta_base = ""
        self.archivos_data = [] 
        self.audios_memoria = {} 
        
        self.btn_reproduciendo = None
        self.after_id = None 
        self.ruta_temp = os.path.join(tempfile.gettempdir(), "temp_preview_audio.wav")

        self.crear_interfaz_principal()
        self.actualizar_textos() # Aplica el idioma inicial

    def t(self, clave):
        """Atajo para obtener el texto en el idioma actual."""
        return TEXTOS[self.idioma_actual][clave]

    def cambiar_idioma(self, event):
        self.idioma_actual = self.combo_idioma.get()
        self.actualizar_textos()

    def actualizar_textos(self):
        """Actualiza todos los textos de la interfaz principal sin reiniciarla."""
        self.root.title(f"{self.t('titulo')} v{VERSION}")
        self.lbl_carpeta.config(text=self.t("carpeta"))
        self.btn_explorar.config(text=self.t("explorar"))
        self.lbl_cortar.config(text=self.t("cortar"))
        self.lbl_volumen.config(text=self.t("volumen"))
        self.chk_normalizar.config(text=self.t("normalizar"))
        self.lbl_sufijo.config(text=self.t("sufijo"))
        self.chk_oto.config(text=self.t("oto"))
        self.btn_sel_todas.config(text=self.t("sel_todas"))
        self.btn_des_todas.config(text=self.t("des_todas"))
        self.lbl_lista.config(text=self.t("lista_audios"))
        self.btn_previsualizar.config(text=self.t("previsualizar"))

    def crear_interfaz_principal(self):
        # --- PANEL SUPERIOR ---
        panel_superior = tk.Frame(self.root, padx=10, pady=10)
        panel_superior.pack(fill="x")

        # Fila 0: Idioma y Ayuda
        frame_top = tk.Frame(panel_superior)
        frame_top.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        tk.Label(frame_top, text="🌐").pack(side="left")
        self.combo_idioma = ttk.Combobox(frame_top, values=["Español", "English", "Português"], state="readonly", width=12)
        self.combo_idioma.set("Español")
        self.combo_idioma.pack(side="left", padx=5)
        self.combo_idioma.bind("<<ComboboxSelected>>", self.cambiar_idioma)
        
        tk.Button(frame_top, text="❓", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", command=self.mostrar_ayuda).pack(side="right")

        # Fila 1: Carpeta
        self.lbl_carpeta = tk.Label(panel_superior, text="")
        self.lbl_carpeta.grid(row=1, column=0, sticky="w")
        self.ent_carpeta = tk.Entry(panel_superior, width=45)
        self.ent_carpeta.grid(row=1, column=1, padx=5, sticky="w")
        self.btn_explorar = tk.Button(panel_superior, text="", command=self.seleccionar_carpeta)
        self.btn_explorar.grid(row=1, column=2, padx=5)

        # Fila 2: Segundos a cortar
        self.lbl_cortar = tk.Label(panel_superior, text="")
        self.lbl_cortar.grid(row=2, column=0, sticky="w", pady=5)
        self.ent_segundos = tk.Entry(panel_superior, width=10)
        self.ent_segundos.insert(0, "1")
        self.ent_segundos.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Fila 3: Volumen y Normalización
        self.lbl_volumen = tk.Label(panel_superior, text="")
        self.lbl_volumen.grid(row=3, column=0, sticky="w")
        
        frame_vol = tk.Frame(panel_superior)
        frame_vol.grid(row=3, column=1, columnspan=2, sticky="w", padx=5)
        
        self.ent_volumen = tk.Entry(frame_vol, width=10)
        self.ent_volumen.insert(0, "100")
        self.ent_volumen.pack(side="left")
        
        self.var_normalizar = tk.BooleanVar(value=False)
        self.chk_normalizar = tk.Checkbutton(frame_vol, text="", variable=self.var_normalizar)
        self.chk_normalizar.pack(side="left", padx=10)

        # Fila 4: Sufijo
        self.lbl_sufijo = tk.Label(panel_superior, text="")
        self.lbl_sufijo.grid(row=4, column=0, sticky="w", pady=5)
        self.ent_sufijo = tk.Entry(panel_superior, width=15)
        self.ent_sufijo.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Fila 5: Generar OTO.ini
        self.var_oto = tk.BooleanVar(value=True)
        self.chk_oto = tk.Checkbutton(panel_superior, text="", variable=self.var_oto, font=("Arial", 9, "bold"))
        self.chk_oto.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

        # --- PANEL DE SELECCIÓN ---
        frame_selecciones = tk.Frame(self.root, padx=10)
        frame_selecciones.pack(fill="x", pady=(5, 0))
        
        self.btn_sel_todas = tk.Button(frame_selecciones, text="", command=self.seleccionar_todas)
        self.btn_sel_todas.pack(side="left", padx=(0, 5))
        self.btn_des_todas = tk.Button(frame_selecciones, text="", command=self.deseleccionar_todas)
        self.btn_des_todas.pack(side="left")

        # --- PANEL CENTRAL ---
        self.lbl_lista = tk.Label(self.root, text="", font=("Arial", 10, "bold"))
        self.lbl_lista.pack(anchor="w", padx=10, pady=(10, 0))
        
        marco_lista = tk.Frame(self.root, bd=2, relief="sunken")
        marco_lista.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(marco_lista)
        scrollbar = tk.Scrollbar(marco_lista, orient="vertical", command=self.canvas.yview)
        self.frame_interior = tk.Frame(self.canvas)

        self.frame_interior.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame_interior, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- PANEL INFERIOR ---
        self.btn_previsualizar = tk.Button(self.root, text="", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.previsualizar)
        self.btn_previsualizar.pack(pady=15)

    def mostrar_ayuda(self):
        messagebox.showinfo(self.t("ayuda_tit"), self.t("ayuda_txt"))

    # ================= LOGICA DE SELECCIÓN =================
    def seleccionar_todas(self):
        if not self.archivos_data: return
        todas_marcadas = all(dato["var"].get() for dato in self.archivos_data)
        if todas_marcadas:
            messagebox.showinfo("Aviso", self.t("msg_sel_todas"))
        else:
            for dato in self.archivos_data: dato["var"].set(True)

    def deseleccionar_todas(self):
        if not self.archivos_data: return
        ninguna_marcada = all(not dato["var"].get() for dato in self.archivos_data)
        if ninguna_marcada:
            messagebox.showinfo("Aviso", self.t("msg_des_todas"))
        else:
            for dato in self.archivos_data: dato["var"].set(False)

    # ================= LOGICA DE REPRODUCCIÓN =================
    def detener_audio(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        if self.btn_reproduciendo:
            self.btn_reproduciendo.config(text="▶", fg="black")
            self.btn_reproduciendo = None

    def auto_reset_boton(self):
        if self.btn_reproduciendo:
            self.btn_reproduciendo.config(text="▶", fg="black")
            self.btn_reproduciendo = None
        self.after_id = None

    def calcular_duracion_ms(self, ruta_o_bytes, es_memoria=False):
        try:
            if es_memoria:
                with wave.open(io.BytesIO(ruta_o_bytes), 'rb') as w:
                    return int((w.getnframes() / w.getframerate()) * 1000)
            else:
                with wave.open(ruta_o_bytes, 'rb') as w:
                    return int((w.getnframes() / w.getframerate()) * 1000)
        except Exception:
            return 1000

    def toggle_reproducir_archivo(self, ruta, btn):
        if self.btn_reproduciendo == btn:
            self.detener_audio()
        else:
            self.detener_audio()
            self.btn_reproduciendo = btn
            btn.config(text="⏹", fg="red")
            duracion_ms = self.calcular_duracion_ms(ruta)
            winsound.PlaySound(ruta, winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.after_id = self.root.after(duracion_ms, self.auto_reset_boton)

    def toggle_reproducir_memoria(self, bytes_audio, btn):
        if self.btn_reproduciendo == btn:
            self.detener_audio()
        else:
            self.detener_audio()
            self.btn_reproduciendo = btn
            btn.config(text="⏹", fg="red")
            with open(self.ruta_temp, "wb") as f:
                f.write(bytes_audio)
            duracion_ms = self.calcular_duracion_ms(bytes_audio, es_memoria=True)
            winsound.PlaySound(self.ruta_temp, winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.after_id = self.root.after(duracion_ms, self.auto_reset_boton)

    # ================= LOGICA PRINCIPAL =================
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.carpeta_base = carpeta
            self.ent_carpeta.delete(0, tk.END)
            self.ent_carpeta.insert(0, carpeta)
            self.cargar_lista_audios()

    def cargar_lista_audios(self):
        for widget in self.frame_interior.winfo_children(): widget.destroy()
        self.archivos_data.clear()
        fila = 0
        for raiz, _, archivos in os.walk(self.carpeta_base):
            for archivo in archivos:
                if archivo.lower().endswith(".wav"):
                    ruta_abs = os.path.join(raiz, archivo)
                    ruta_rel = os.path.relpath(ruta_abs, self.carpeta_base)
                    var_check = tk.BooleanVar(value=True)
                    self.archivos_data.append({"nombre": archivo, "ruta_absoluta": ruta_abs, "ruta_relativa": ruta_rel, "var": var_check})
                    chk = tk.Checkbutton(self.frame_interior, variable=var_check)
                    chk.grid(row=fila, column=0, sticky="w", padx=5)
                    btn_play = tk.Button(self.frame_interior, text="▶", bg="#ddd", fg="black", width=3)
                    btn_play.config(command=lambda r=ruta_abs, b=btn_play: self.toggle_reproducir_archivo(r, b))
                    btn_play.grid(row=fila, column=1, padx=5, pady=2)
                    tk.Label(self.frame_interior, text=ruta_rel, anchor="w").grid(row=fila, column=2, sticky="w")
                    fila += 1

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
                pico_maximo = max((abs(x) for x in muestras), default=0)
                if pico_maximo > 0:
                    factor = 32767.0 / pico_maximo
                else:
                    factor = 1.0
            else:
                factor = porcentaje_vol / 100.0
                
            for i in range(len(muestras)):
                val = int(muestras[i] * factor)
                if val > 32767: val = 32767
                elif val < -32768: val = -32768
                muestras[i] = val
                
        archivo_virtual = io.BytesIO()
        with wave.open(archivo_virtual, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(muestras.tobytes())
        return archivo_virtual.getvalue()

    def previsualizar(self):
        self.detener_audio()
        if not self.archivos_data:
            messagebox.showwarning("Aviso", self.t("msg_sin_audios"))
            return
        try:
            segundos = float(self.ent_segundos.get())
            volumen = float(self.ent_volumen.get())
            normalizar = self.var_normalizar.get()
        except ValueError:
            messagebox.showerror("Error", self.t("msg_error_num"))
            return
            
        self.audios_memoria.clear()
        errores = 0
        
        for dato in self.archivos_data:
            if dato["var"].get(): 
                try:
                    bytes_wav = self.procesar_audio_a_memoria(dato["ruta_absoluta"], segundos, volumen, normalizar)
                    self.audios_memoria[dato["ruta_relativa"]] = bytes_wav
                except Exception as e:
                    print(f"Error procesando {dato['nombre']}: {e}")
                    errores += 1
                    
        if errores > 0: messagebox.showwarning("Atención", self.t("msg_error_proc"))
        if not self.audios_memoria:
            messagebox.showinfo("Aviso", self.t("msg_sin_sel"))
            return
        self.abrir_ventana_previsualizacion()

    def abrir_ventana_previsualizacion(self):
        ventana_prev = tk.Toplevel(self.root)
        ventana_prev.title(self.t("previsualizar"))
        ventana_prev.geometry("550x400")
        ventana_prev.protocol("WM_DELETE_WINDOW", lambda: (self.detener_audio(), ventana_prev.destroy()))
        
        tk.Label(ventana_prev, text=self.t("titulo_prev"), font=("Arial", 10, "bold")).pack(pady=10)
        
        marco = tk.Frame(ventana_prev, bd=2, relief="sunken")
        marco.pack(fill="both", expand=True, padx=10, pady=5)
        canvas_prev = tk.Canvas(marco)
        scroll_prev = tk.Scrollbar(marco, orient="vertical", command=canvas_prev.yview)
        frame_int_prev = tk.Frame(canvas_prev)
        
        frame_int_prev.bind("<Configure>", lambda e: canvas_prev.configure(scrollregion=canvas_prev.bbox("all")))
        canvas_prev.create_window((0, 0), window=frame_int_prev, anchor="nw")
        canvas_prev.configure(yscrollcommand=scroll_prev.set)
        canvas_prev.pack(side="left", fill="both", expand=True)
        scroll_prev.pack(side="right", fill="y")
        
        for i, (ruta_rel, bytes_wav) in enumerate(self.audios_memoria.items()):
            btn_play = tk.Button(frame_int_prev, text="▶", bg="#ddd", fg="black", width=3)
            btn_play.config(command=lambda b_wav=bytes_wav, b=btn_play: self.toggle_reproducir_memoria(b_wav, b))
            btn_play.grid(row=i, column=0, padx=5, pady=2)
            tk.Label(frame_int_prev, text=ruta_rel, anchor="w").grid(row=i, column=1, sticky="w")
            
        frame_botones = tk.Frame(ventana_prev)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text=self.t("guardar_solo"), bg="#2196F3", fg="white",
                  command=lambda: self.guardar_audios(solo_modificados=True, ventana=ventana_prev)).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones, text=self.t("guardar_todos"), bg="#FF9800", fg="white",
                  command=lambda: self.guardar_audios(solo_modificados=False, ventana=ventana_prev)).grid(row=0, column=1, padx=10)

    # ================= GUARDADO CON SUFIJOS Y OTO.INI =================
    def guardar_audios(self, solo_modificados, ventana):
        self.detener_audio()
        
        directorio_padre = filedialog.askdirectory(title=self.t("msg_dir_tit"))
        if not directorio_padre: return 
        
        nombre_carpeta = simpledialog.askstring(self.t("msg_nombre_tit"), self.t("msg_nombre_txt"), initialvalue=self.t("def_folder"))
        if not nombre_carpeta: return 
            
        carpeta_salida = os.path.join(directorio_padre, nombre_carpeta)
        sufijo = self.ent_sufijo.get().strip()
        generar_oto = self.var_oto.get()
        carpetas_para_oto = {} 
        
        try:
            for dato in self.archivos_data:
                ruta_in = dato["ruta_absoluta"]
                ruta_rel_original = dato["ruta_relativa"]
                
                nombre_base, ext = os.path.splitext(dato["nombre"])
                nuevo_nombre = f"{nombre_base}{sufijo}{ext}"
                alias_oto = f"{nombre_base}{sufijo}"
                
                dir_rel = os.path.dirname(ruta_rel_original)
                ruta_rel_nueva = os.path.join(dir_rel, nuevo_nombre) if dir_rel else nuevo_nombre
                
                ruta_out = os.path.join(carpeta_salida, ruta_rel_nueva)
                directorio_out = os.path.dirname(ruta_out)
                os.makedirs(directorio_out, exist_ok=True)

                esta_seleccionado = dato["var"].get()

                if esta_seleccionado:
                    with open(ruta_out, 'wb') as f:
                        f.write(self.audios_memoria[ruta_rel_original])
                else:
                    if not solo_modificados:
                        shutil.copy2(ruta_in, ruta_out)

                if generar_oto and (esta_seleccionado or not solo_modificados):
                    linea_oto = f"{nuevo_nombre}={alias_oto},0,0,0,0,0\n"
                    if directorio_out not in carpetas_para_oto:
                        carpetas_para_oto[directorio_out] = []
                    carpetas_para_oto[directorio_out].append(linea_oto)

            if generar_oto:
                for carpeta_dest, lineas in carpetas_para_oto.items():
                    ruta_oto = os.path.join(carpeta_dest, "oto.ini")
                    with open(ruta_oto, "w", encoding="shift_jis", errors="replace") as f:
                        f.writelines(lineas)

            ventana.destroy()
            messagebox.showinfo("Proceso Terminado", f"{self.t('msg_exito')}{carpeta_salida}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EditorAudioApp(root)
    root.mainloop()