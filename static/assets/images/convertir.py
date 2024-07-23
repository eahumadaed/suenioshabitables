import os
from PIL import Image

def convert_images_to_jpg(directory):
    if not os.path.exists(directory):
        print(f"El directorio {directory} no existe.")
        return
    
    files = os.listdir(directory)
    
    for index, file in enumerate(files, start=1):
        file_path = os.path.join(directory, file)
        
        try:
            image = Image.open(file_path)
            new_file_path = os.path.join(directory, f'c{index}.jpg')
            image = image.convert('RGB')
            image.save(new_file_path, 'JPEG')
            print(f"Convertido {file} a {new_file_path}")
        except Exception as e:
            print(f"No se pudo convertir {file}: {e}")

# Directorio de ejemplo
directory = 'explore'

convert_images_to_jpg(directory)
