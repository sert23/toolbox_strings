
#ifile="C:/Users/Ernesto/Downloads/human_virus.fasta"
#ifile="C:/Users/Ernesto/Downloads/invertebrates.fasta"
#ifile="C:/Users/Ernesto/Downloads/human_prokaryotes.csv"
# ifile="C:/Users/Ernesto/Downloads/plants_prokaryotes.csv"
ifile="C:/Users/Ernesto/PycharmProjects/Ensembl_parser/releaseAug2020/all_virus.fasta"
#out_path="C:/Users/Ernesto/Downloads/human_tagged_virus2.fasta"
# out_path="C:/Users/Ernesto/Downloads/invertebrates_tagged_virus.fasta"
out_path="C:/Users/Ernesto/PycharmProjects/Ensembl_parser/releaseAug2020/all_virus_tagged.fasta"
tag=":all_virus"

def make_strings(input_table,output_file):
    with open(input_table, 'rb') as f:
        reader = f.readlines()
        with open(output_file, "wb") as g:
            for line in reader:
                if line.startswith("#"):
                    g.write(line)
                else:
                    row=line.split("\t")
                    to_file="genome="+";".join(row)+"\n"
                    g.write(to_file)


def add_sufix(input_file,out_file,tag):
    with open(input_file, 'rb') as f:
        valid=False
        to_file=""
        reader = f.readlines()
        with open(out_file, "wb") as g:
            for line in reader:
                if line.startswith(">"):
                    if line.endswith(", complete genome\n"):
                        valid=True
                        row = line.split(",")
                        first_half = "_".join(row[:-1])
                        first_half = first_half.replace(" ","_")
                        to_file = first_half.replace(":","_") + tag
                        print(to_file)

                    else:
                        valid=False
                elif valid :
                    to_file=line.rstrip()
                if valid:
                    g.write(to_file+"\n")


def table_parser(input_table):
    NC_list=[]
    import csv
    with open(ifile, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #NC_line=row[9].split(":")[1]
            if str(row[9]).startswith("chromosome"):
                NC_line=str(row[9]).split(":")[1].split(";")[0]
                if "/" in NC_line:
                    NC_list.append(NC_line.split("/")[0])
                else:
                    NC_list.append(NC_line)
        return NC_list



add_sufix(ifile,out_path,tag)
exit()

bacteria=table_parser(ifile)

thefile = open('plants_bacteria.txt', 'w')
for item in bacteria:
  print>>thefile, item