import requests
import json
from modulku import StemNstopW as stm
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def save(data, nama):
    with open(dir_path+'/data/'+nama, 'w') as f:
        json.dump(data, f)

def get_data(name):
    with open(dir_path+"/data/"+str(name), "r") as filename:
        return json.load(filename)

kateglo = get_data('kateglo.json')
# kateglo = {}

def find_sianto(cek):
    list_sinonim = list()
    list_antonim = list()
    # if cek not in kateglo:
    if cek not in kateglo:
        # print("tidak ada =>", cek)
    # if True:
        try:
            list_objek = requests.get('http://kateglo.com/api.php?format=json&phrase='+str(cek)).json()['kateglo']['all_relation']
            for objek in list_objek:
                try:
                    kata = objek['related_phrase']
                    # print(kata, )
                    tipe = objek['rel_type_name']
                    # print(kata,"|",tipe )
                    # if len(kata.split())>0 and tipe == 'Sinonim':
                    if tipe == 'Sinonim':
                        if kata not in list_sinonim and kata != cek:
                            list_sinonim.append(kata)
                    elif tipe == 'Antonim':
                        if kata not in list_antonim and kata != cek:
                            list_antonim.append(kata)
                    # print(list_sinonim)
                except:
                    pass
            try:
                hasil = {"sinonim":list(set(list_sinonim)), "antonim":list(set(list_antonim))}
                if cek not in kateglo:
                    # print("simpan")
                    kateglo.update({cek: hasil}) 
                    # print(cek,"|",hasil)
                    save(kateglo, "kateglo.json")
            except:
                pass
        except:
            pass
        try:
            return hasil
        except:
            return {"sinonim":list_sinonim, "antonim":list_antonim }
    else:
        # print(cek,"|",kateglo[cek])
        return kateglo[cek]

def get_all_sinonim(kk):
    if type(kk)!=list:
        if type(kk)!=str:
            kk = str(kk)
        kk = [kk]
    kamus_ = {}
    for k in kk:
        hasil = find_sianto(k)["sinonim"]
        if len(hasil)>0:
            kamus_.update( {k : hasil} )
    return kamus_

def get_all_antonim(kk):
    if type(kk)!=list:
        if type(kk)!=str:
            kk = str(kk)
        kk = [kk]
    kamus_ = {}
    for k in kk:
        hasil = find_sianto(k)["antonim"]
        if len(hasil)>0:
            kamus_.update( {k : hasil} )
    return kamus_

def stem_dulu (list_kata):
    n_list = list()
    for i in list_kata:
        i = stm.stemmer_kata(i)
        n_list.append(i)
    return list(set(n_list))

def query_expantion(kalimat, stem = False):
    kaimat = kalimat.split()
    list_kalimat = list()
    for k in kaimat:
        a = list((find_sianto(k)["sinonim"]))
        if stem == True:
            a = stem_dulu (a)
        a = " ".join(a) 
        list_kalimat.append(a)
    return " ".join(kaimat + list_kalimat)


