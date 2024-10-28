import numpy as np
import pandas as pd
from glob import glob

def founder_transe(f, s, ifA):
    ifA = int(ifA)
    l = (np.array(f[2:], float)>0).astype(int) * ifA
    l += (np.array(s[2:], float)>0).astype(int) * (not ifA)
    l = l.astype(str)
    l[l=="0"] = "B"
    l[l=="1"] = "A"
    return list(l)


chrlist = list(range(1,20))+['X']
dir_name = r"happy_to_rqtl2\Happy_files\genotypes\\"

for chr in chrlist:
    alleles = []
    map = []
    cc_geno = {}
    founder_genome = []
    rqtl2_founders_geno = pd.read_csv(f".\cc\MMnGM\MMnGM_foundergeno{chr}.csv", skiprows=3)
    al_file_name = glob(f"{dir_name}chr{chr}*alleles")[0]
    marker_names = []

    
    with open(al_file_name) as al_file:
        line = al_file.readline()
        l = line.split()
        marker_count = int(l[1])
        line = al_file.readline()
        while line:
            if line.startswith("marker"):
                l = line.split()
                marker_name = l[1]
                if marker_name in marker_names:
                    marker_name+="_b"
                marker_names.append(marker_name)
                marker_pos = l[4]
                line_first = al_file.readline().split()
                line_secound = al_file.readline().split()
                line_NA = al_file.readline().split()
                is_first_A = np.sum(np.array(line_first[2:], float)>0) >= 4 #TODO
                if np.sum(rqtl2_founders_geno["marker"] == marker_name):
                    rqtl2_conv = rqtl2_founders_geno[rqtl2_founders_geno["marker"]==marker_name]
                    if np.sum(np.array(line_first[2:], float)>0) != 4:
                        is_first_A = bool(np.sum(np.array(line_first[2:], float)>0) == (rqtl2_conv == 'A').values.sum())
                    else:
                        is_first_A = bool((any(rqtl2_conv["A"] == "A") and float(line_first[2])) or (any(rqtl2_conv["A"] == "B") and float(line_secound[2])))
                a_name = line_first[1]
                b_name = line_secound[1]
                if not is_first_A:
                    a_name, b_name = b_name, a_name
                founder_line = founder_transe(line_first, line_secound, is_first_A)
                founder_line = [marker_name] + founder_line
                founder_genome.append(founder_line)
                alleles.append([marker_name, marker_pos, a_name, b_name])
            line = al_file.readline()


    map_file_name = glob(f"{dir_name}chr{chr}*map")[0]
    pmap = pd.read_csv(map_file_name, sep="\t")
    
    def modify_duplicates(df, column_name):
        # Create a mask for duplicate values
        mask = df.duplicated(subset=[column_name], keep='first')
        
        # Modify the duplicates by adding '_b'
        df.loc[mask, column_name] = df.loc[mask, column_name] + '_b'
        
        return df

    pmap = modify_duplicates(pmap, "marker")


    data_file_name = glob(f"{dir_name}chr{chr}*data")[0]
    with open(data_file_name) as data_file:
        line = data_file.readline()
        while line:
            l = line.split("\t")
            line_alle = []
            if len(l) == marker_count+1:
                header = l[0].split()
                mouse_line_name = header[1]
                for i in range(1,len(l)):
                    al = l[i].split()
                    if al[0] == "NA" and al[1] == "NA":
                        a = '-'
                    elif al[0] == alleles[i-1][2] and al[1] == alleles[i-1][2]:
                        a = "A"
                    elif al[0] == alleles[i-1][3] and al[1] == alleles[i-1][3]:
                        a = "B"
                    else:
                        a = "-"
                    line_alle.append(a)
                cc_geno[mouse_line_name] = line_alle
            else:
                l = line.split()
                if len(l) == marker_count*2+6:
                    mouse_line_name = l[1]
                    for i in range(6, len(l), 2):
                        al = l[i], l[i+1]
                        if al[0] == "NA" and al[1] == "NA":
                            a = '-'
                        elif al[0] == alleles[(i-6)//2][2] and al[1] == alleles[(i-6)//2][2]:
                            a = "A"
                        elif al[0] == alleles[(i-6)//2][3] and al[1] == alleles[(i-6)//2][3]:
                            a = "B"
                        else:
                            a = "-"
                        line_alle.append(a)
                    cc_geno[mouse_line_name] = line_alle
            line = data_file.readline()

    
   
    line_index = [n[0] for n in alleles]
    geno = pd.DataFrame(cc_geno, line_index)
    founder_genome = founder_genome
    foundergeno = pd.DataFrame(founder_genome)
    gmap = [[n[0], chr, n[1]] for n in alleles]
    gmap = pd.DataFrame(gmap, columns=["marker","chr","pos"])
    pmap["bp"] /= 1e6

    def create_header_and_save(file_name, df, index=False, index_label=None):
        with open(file_name, 'w') as fs:
            fs.write("#\n")
            rows = len(df)
            col = len(df.columns) + int(index)
            fs.write(f"# nrow {rows}\n")
            fs.write(f"# ncol {col}\n")
        df.to_csv(file_name, index=index, index_label=index_label, mode='a')



    file_base_name = f"new_files\\chr{chr}_"
    create_header_and_save(file_base_name+"geno.csv", geno, True, index_label="marker")
    create_header_and_save(file_base_name+"founders.csv", foundergeno)
    create_header_and_save(file_base_name+"gmap.csv", gmap)
    create_header_and_save(file_base_name+"pmap.csv", pmap)
    # geno.to_csv(file_base_name+"geno.csv", index_label="marker")
    # foundergeno.to_csv(file_base_name+"founders.csv", index=False)
    # gmap.to_csv(file_base_name+"gmap.csv", index=False)
    # pmap.to_csv(file_base_name+"pmap.csv", index=False)

