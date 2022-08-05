from pathlib import Path
import os, re

dirpath = Path.cwd()

def clean_directory():

    test = re.compile('(\d+\.\d+\.\d+)_')
    file_regex = re.compile('\w{4}-\d+-\d+-\d+-')
    # folder_regex = re.compile('\S*\D*\S*files')
    file_number = re.compile('(\d+)')

    file_names = input()
    need_download = 'E-v1.js.download'

    for root, dirs, files in os.walk(dirpath):
        for f in files: 
            # The download for video players
            if f == need_download:
                print(f'Saving Downdload: {f}')
            # deleting all left over html files
            elif f.endswith('.html') and not test.match(f):
                if 'retrieve' in f:
                    # print(f)
                    # pass
                    os.remove(os.path.join(root, f))
                elif 'saved' in f:
                    # print(f)
                    # pass
                    os.remove(os.path.join(root, f))
                elif 'xdomain' in f:
                    # print(f)
                    # pass
                    os.remove(os.path.join(root, f))
                else:
                    print(f'Saving: {f}')
                    continue
            # html images
            elif file_regex.match(f):
                new_image = file_regex.sub('', f)
                # os.rename(f, new_image)
                os.rename(os.path.join(root, f), os.path.join(root, new_image))
            # html file names
            elif test.match(f):
                new_file_list = file_number.findall(f)
                new_file = f'{file_names}_{str(new_file_list[0])}{str(new_file_list[1])}{str(new_file_list[2])}.html'
                os.rename(f, new_file)
                # print(new_file)

            # save the scripts
            elif f.endswith('.ipynb') or f.endswith('.py'):
                print(f'Saving Files: {f}')
            # remove everything else and hope there's nothing important
            else:
                try:
                    # pass
                    # print(f)
                    os.remove(os.path.join(root, f))
                except:
                    print('File already removed')

    for dir in os.listdir(dirpath):
        try:
            new_folder_list = file_number.findall(dir)
            new_folder = f'{file_names}_{str(new_folder_list[0])}{str(new_folder_list[1])}{str(new_folder_list[2])}'
            os.rename(dir, new_folder)
        except:
            pass

