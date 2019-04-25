import face_recognition
import os
import shutil

persons_list = []
index = {}
potraits = {}
faces_in_image = {}
dir_path = 'img/' # Path to the sub-directory which contains the images 


def sort(file_name):
    '''
    Checks if a given file contains faces, if any new found, then add to persons_list
    '''
    global persons_list, index
    image = face_recognition.load_image_file(dir_path + file_name)
    try:
        face_encodings = face_recognition.face_encodings(image)
        faces_in_image[file_name] = len(face_encodings)
        print(f'{len(face_encodings)} faces found in {file_name}')
    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images.")
    if face_encodings:
        if not persons_list:
            persons_list += face_encodings
            for i, f in enumerate(face_encodings):
                index[f'person{i+1}'] = [file_name]

        else:
            for f in face_encodings:
                results = face_recognition.compare_faces(
                    persons_list, f, tolerance=0.6)

                if True not in results:
                    persons_list.append(f)

                    index[f'person{len(index)+1}'] = [file_name]

                else:
                    ind = results.index(True)
                    index[f'person{ind+1}'].append(file_name)


def getFiles():
    files = []
    with os.scandir(dir_path) as entries:
        for entry in entries:
            if entry.is_file():
                files.append(entry.name)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    return files


def move():
    if (1 in faces_in_image.values()):
        print('\nMoving...')
        potraits_list = []
        for file, faces in faces_in_image.items():
            if faces == 1:
                potraits_list.append(file)
        for p in potraits_list:
            for person, files in index.items():
                if p in files:
                    if person not in potraits.keys():
                        potraits[person] = [p]
                    else:
                        potraits[person].append(p)
        for person, files in potraits.items():
            os.mkdir(dir_path + person)
            for file in files:
                shutil.move(dir_path + file, dir_path + person)
                print(f'Moving {file} to {dir_path + person}')
    else:
        print('\nNo potraits found!')


def displayIndex():
    for person, files in index.items():
        print(f'\n{person} has {len(files)} images:')
        for i, file in enumerate(files):
            print(f'  ({i+1}) {file}')


if __name__ == '__main__':
    files = getFiles()
    for file in files:
        sort(file)
    print(f'\n[ {len(persons_list)} unique faces found in total ]\n')
    displayIndex()
    move()
