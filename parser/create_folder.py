import os


def create_folder(path):
    os.mkdir(path)
    print('Successfully create: '.upper() + path)


for i in range(2, 28):
    create_folder('inf_tasks/' + str(i))
