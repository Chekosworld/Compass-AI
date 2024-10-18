import streamlit as st
from PIL import Image
import os

# Definir la carpeta para almacenar las fotos subidas
photos_path = './photos'

# Asegurarse de que la carpeta de fotos existe
if not os.path.exists(photos_path):
    os.makedirs(photos_path)

# Título de la galería
st.title('Galería de Fotos - Compass AI')

# Barra de navegación
st.sidebar.title("Navegación")
st.sidebar.button("Inicio")
st.sidebar.button("Galería")
st.sidebar.button("Configuración")

# Función para mostrar notificaciones si el archivo no es compatible
def notify_incompatible_file():
    st.error("Archivo no compatible. Solo se permiten formatos JPG, JPEG y PNG.")

# Subida de imágenes
st.subheader("Sube tus fotos aquí")
uploaded_file = st.file_uploader("Arrastra o selecciona tu archivo (formatos aceptados: JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

# Si el usuario sube un archivo, se guarda en la carpeta correspondiente
if uploaded_file is not None:
    try:
        # Guardar la imagen en la carpeta de fotos
        image_path = os.path.join(photos_path, uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"La imagen {uploaded_file.name} se subió correctamente.")
    except Exception as e:
        notify_incompatible_file()

# Mostrar la galería de fotos subidas
st.subheader("Galería de Fotos")

# Obtener la lista de fotos en la carpeta
photo_files = os.listdir(photos_path)

if len(photo_files) == 0:
    st.info("No hay fotos subidas.")
else:
    # Mostrar las fotos en una cuadrícula de 3 columnas
    cols = st.columns(3)
    for index, photo in enumerate(photo_files):
        image_path = os.path.join(photos_path, photo)
        image = Image.open(image_path)

        # Mostrar la imagen en su respectiva columna
        with cols[index % 3]:
            st.image(image, caption=photo, use_column_width=True)
