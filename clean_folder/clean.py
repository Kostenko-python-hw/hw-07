from pathlib import Path
import shutil 
import sys
import re


categories = {
    'images': [],
    'movies': [],
    'documents': [],
    'audios': [],
    'archives': [],
    'other': []
}


ignored_folders = ('archives', 'video', 'audio', 'documents', 'images', 'other')

images_extensions =  ('JPEG', 'PNG', 'JPG', 'SVG')
movies_extensions=  ('AVI', 'MP4', 'MOV', 'MKV')
documents_extensions =  ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
audios_extensions =  ('MP3', 'OGG', 'WAV', 'AMR')
archives_extensions =  ('ZIP', 'GZ', 'TAR')

existing_known_extensions = set()
existing_unknown_extensions = set()

folders = set()

transliteration_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': "'", 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'IE', 'Ж': 'ZH', 'З': 'Z',
        'И': 'Y', 'І': 'I', 'Ї': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
        'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
        'Ь': "'", 'Ю': 'IU', 'Я': 'IA'
    }




def arg_check():

    if len(sys.argv) <= 1:
        print('In args you need to pass the path')
        return False
    
    p = Path(sys.argv[1])

    if not p.is_dir():
        print('In args you need to pass the path to the folder')
        return False
    
    return True




def categorize_files(path):

    for i in path.iterdir():
        if i.is_dir():
            if str(i) in ignored_folders:
                continue
            categorize_files(i)
            folders.add(i)
        else:
            sorting_file_names_by_category(i)




def normalize(str):

    transliterated_string = ''.join(transliteration_dict.get(char, char) for char in str)
    result = re.sub(r'[^a-zA-Z0-9]', '_', transliterated_string)

    return result




def normalize_and_replace_files(path):

    for key, category in categories.items():
        if(len(category) > 0):
            Path(f'{path}/{key}').mkdir(parents=True, exist_ok=True)
            for file in category:
                normilized_name = normalize(file['name'])
                extension = file['extension']
                if key == 'archives':
                    extract_dir = f'{path}/{key}/{normilized_name}'
                    shutil.unpack_archive(file['path'], extract_dir)
                    Path.unlink(file['path'])
                else:
                    new_path = f'{path}/{key}/{normilized_name}.{extension}'
                    file['path'].rename(Path(new_path))
                
    for folder in folders:
        if folder.exists():
            shutil.rmtree(folder) 





def sorting_file_names_by_category(path):
    file_extension = str(path).split('.')[-1].upper()
    file_name_with_extension = str(path).split('/')[-1]
    file_name = file_name_with_extension.rsplit('.', 1)[0]
    if file_extension in images_extensions:
        categories['images'].append({'name': file_name, 'path': path, 'extension': file_extension})
        existing_known_extensions.add(file_extension)
    elif file_extension in movies_extensions:
        categories['movies'].append({'name': file_name, 'path': path, 'extension': file_extension})
        existing_known_extensions.add(file_extension)
    elif file_extension in documents_extensions:
        categories['documents'].append({'name': file_name, 'path': path, 'extension': file_extension})
        existing_known_extensions.add(file_extension)
    elif file_extension in audios_extensions:
        categories['audios'].append({'name': file_name, 'path': path, 'extension': file_extension})
        existing_known_extensions.add(file_extension)
    elif file_extension in archives_extensions:
        categories['archives'].append({'name': file_name, 'path': path, 'extension': file_extension})
        existing_known_extensions.add(file_extension)
    else:
        categories['other'].append({'name': file_name, 'path': path, 'extension': file_extension})
        existing_unknown_extensions.add(file_extension)




def main():
    isPathCorrect = arg_check()

    if isPathCorrect:

        p = Path(sys.argv[1])
        categorize_files(p)
        normalize_and_replace_files(p)
        
    
        


if __name__ == '__main__':
    main()


