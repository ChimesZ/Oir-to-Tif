import os
import re

def get_file_list(num_files):
    """
    formats number of files in olympus format
    :param num_files:
    :return: list of file numbers
    """
    file_list = ['0001', '0002', '0003', '0004']
    """
    for num in range(1, num_files+1):
        num = str(num)
        to_add = 4-len(num)
        final = '0'*to_add+num
        file_list.append(final)

    return file_list
    """


def make_macro_3_channels(data_dir, save_dir, file_name_prefixes, file_nums, macro_save_dir,tif_name):
    """

    :param data_dir: directory with .oir files
    :param save_dir: directory where .tif files will be saved
    :param file_name_prefix: common component of name of .oir files from experiment
           ex: "8-10-2018 exp 2 attempt 1 phase 1_A01_G001_"
    :param file_nums: output of get_file_list
    :param macro_save_dir: full path of location for macro to save
    :return: saves a macro file
    """

    file_object = open(macro_save_dir+"oir_macro.ijm", "w")

    inp = 'input="{}";'.format(data_dir)

    bio_import = 'run("Bio-Formats Importer", "open=["+ input + filename +"] view=Hyperstack split_channels stack_order=XYCZT");'
    run = 'run("Z Project...", "projection=[Max Intensity]");'
    close = 'close();'

    i=0
    for file_name_prefix in file_name_prefixes:

        for file_num in file_nums:
            filename = 'filename="{}{}.oir"'.format(file_name_prefix, file_num)
            two = 'selectWindow("{}{}{}.oir - C=0");'.format(data_dir,file_name_prefix, file_num) # For windows, data_dir is needed. Not for MacOS
            four = 'saveAs("Tiff", "{}MAX_DG_{} {}.tif");'.format(save_dir, file_num, tif_name[i])
        

            command = inp+"\n"+filename+"\n"+bio_import+"\n"+two+"\n"+run+"\n"+four+"\n"+close+"\n"+close
    
            file_object.write(command+"\n")

        i+=1

    file_object.close()
    """
    This part is for multichannel processing
    two_1 = 'selectWindow("{}{}.oir - C=1");'.format(file_name_prefix, file_num)
        four_1 = 'saveAs("Tiff", "{}MAX_{}{}.oir - C=1.tif");'.format(save_dir, file_name_prefix, file_num)
        two_2 = 'selectWindow("{}{}.oir - C=2");'.format(file_name_prefix, file_num)
        four_2 = 'saveAs("Tiff", "{}MAX_{}{}.oir - C=2.tif");'.format(save_dir, file_name_prefix, file_num)
                   two_1+"\n"+run+"\n"+four_1+"\n"+close+"\n"+close+"\n"+ \
                  two_2+"\n"+run+"\n"+four_2+"\n"+close+"\n"+close
    """
def get_name_list(path):   
    name_list=os.listdir(path)
    rule = r"000\d.oir"
    repl = ""
    for i in range(0,len(name_list)):
        name_list[i] = re.sub(rule, repl, name_list[i],count=0,flags=0)
    name = list(set(name_list))
    name.sort(key = name_list.index)
    return name

def get_tif_name(names):
    pattern = r"(?<=[(green)(red)]\s).+(?=_A01)"
    re.findall(pattern,names[12])
    tif_labels=[]
    for name in names:
        tif_labels.extend(re.findall(pattern,name))
    tif_labels
    tif_names = []
    for tif_label in tif_labels:
        if re.findall("\d",tif_label):
            tif_names.append("{}_recall_".format(re.findall(r"\d[a-z][a-z]",tif_label)[0]))
        elif re.findall("TR",tif_label):
            tif_names.append("ref_")
        elif re.findall("baseline",tif_label):
            tif_names.append("0th_recall_")
        elif re.findall("NC",tif_label):
            tif_names.append("10th_recall_")
        elif re.findall("remote",tif_label):
            tif_names.append("11th_recall_")
        else:
            tif_names.append(input(tif_label))
    i=0
    for name in names:
        if re.findall("green",name):
            tif_names[i]+="green"
        else:
            tif_names[i]+="red"
        i+=1
    return(tif_names)