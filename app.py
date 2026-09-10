import streamlit as st
from PIL import Image
import pytesseract
import io

# Configuración de la página
st.set_page_config(page_title="Buscador de Referencias en Fotos (Cloud)", layout="wide")

st.title("☁️ Buscador de Referencias en la Nube")
st.markdown("Sube o arrastra tus fotos aquí y escribe la referencia que deseas localizar.")

# Componente para cargar múltiples fotos desde cualquier dispositivo o navegador
uploaded_files = st.file_uploader(
    "Sube tus imágenes (PNG, JPG, JPEG, WEBP):", 
    type=["png", "jpg", "jpeg", "webp"], 
    accept_multiple_files=True
)

# Barra de búsqueda
referencia_buscada = st.text_input("Ingresa la referencia a buscar:", "")

btn_buscar = st.button("Ejecutar Búsqueda", type="primary")

if btn_buscar:
    if not uploaded_files:
        st.warning("Por favor, sube al menos una imagen antes de buscar.")
    elif not referencia_buscada:
        st.warning("Por favor, ingresa una referencia para buscar.")
    else:
        with st.spinner("Analizando imágenes (nombre y contenido OCR)..."):
            resultados = []
            
            for uploaded_file in uploaded_files:
                archivo_nombre = uploaded_file.name
                coincidencia = False
                tipo_coincidencia = ""
                
                # A. Buscar en el nombre del archivo
                if referencia_buscada.lower() in archivo_nombre.lower():
                    coincidencia = True
                    tipo_coincidencia = "Nombre de archivo"
                else:
                    # B. Buscar dentro de la imagen usando OCR
                    try:
                        image_bytes = uploaded_file.read()
                        imagen = Image.open(io.BytesIO(image_bytes))
                        
                        texto_imagen = pytesseract.image_to_string(imagen)
                        if referencia_buscada.lower() in texto_imagen.lower():
                            coincidencia = True
                            tipo_coincidencia = "Contenido (OCR)"
                    except Exception:
                        pass
                
                if coincidencia:
                    uploaded_file.seek(0)
                    resultados.append({
                        "archivo": uploaded_file,
                        "nombre": archivo_nombre,
                        "tipo": tipo_coincidencia
                    })

        # Mostrar resultados en pantalla
        if resultados:
            st.success(f"¡Se encontraron {len(resultados)} coincidencias!")
            
            grid_cols = st.columns(3)
            for idx, res in enumerate(resultados):
                current_col = grid_cols[idx % 3]
                with current_col:
                    img = Image.open(res["archivo"])
                    st.image(
                        img, 
                        caption=f"📄 {res['nombre']}\n📌 Tipo: {res['tipo']}", 
                        use_container_width=True
                    )
        else:
            st.info("No se encontró ninguna coincidencia con esa referencia en las fotos subidas.")