## 📋 Sistema de Versiones - Guía Rápida

### Versión Actual: 0.2

---

### Para la próxima actualización (ej: 0.3):

#### 1️⃣ **Actualiza el número de versión en el código:**
Edita `Diogenes_Audio_Mod.py` línea ~13:
```python
VERSION = "0.3"
```

#### 2️⃣ **Actualiza el archivo version.txt:**
Edita `version.txt`:
```
0.3
```

#### 3️⃣ **Commit a GitHub:**
```powershell
git add .
git commit -m "Version 0.3: Descripción de cambios"
```

#### 4️⃣ **Crea un TAG (opcional pero recomendado):**
```powershell
git tag v0.3
git push origin main
git push origin v0.3
```

#### 5️⃣ **Crea Release en GitHub (opcional):**
- Ve a: https://github.com/Dagg001/Diogenes-Audio-Mod/releases
- Haz clic en "Create a new release"
- Tag: `v0.3`
- Título: `Version 0.3`
- Descripción: Cambios realizados

---

### ✅ La versión se mostrará automáticamente en la ventana:
**"Diogenes Audio Mod v0.3"**

