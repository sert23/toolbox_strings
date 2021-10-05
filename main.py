import os

import json
import csv
import re

exceptions={"Dog":"Canis familiaris","Gorilla" : "Gorilla gorilla"}
exceptions2={"Dog":"Canis lupus familiaris","Gorilla" : "Gorilla gorilla gorilla"}

def grab_assembly_name(gname,csv_table):
    with open(csv_table, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
        #re.match(pattern, string, flags=0)
            if re.match("^"+gname+"$", row[0]):
                output=row[3].replace(" ","_")
                return output.replace(".","_")

def grab_scientific_name(gname,csv_table):
    if (gname in exceptions.keys()):
        return exceptions[gname]
    with open(csv_table, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
        #re.match(pattern, string, flags=0)
            if re.match("^"+gname+"$", row[0]):
                return row[1]
def grab_taxon_ID(gname,csv_table):
    with open(csv_table, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
        #re.match(pattern, string, flags=0)
            if re.match("^"+gname+"$", row[0]):
                return row[2]

def grab_short_name(scientific, hairpins):
    short_name_list=list()
    with open(hairpins, "r+") as f:
        lines=f.readlines()
        for line in lines:
            larger_than=re.match(">([a-zA-Z0-9]+)", line)
            if larger_than:
                chunks=line.split()
                sc_name=chunks[2]+" "+chunks[3]
                if re.match(scientific, sc_name):
                    short_name_list.append(larger_than.group(1))
        import warnings
        if len(short_name_list)==0:
            return "---"
        if len(list(set(short_name_list))) > 1:
            warnings.warn('more than one short name found for '+scientific)
        return list(set(short_name_list))[0]

def grab_kegg_name(scientific_name):
    import re, urllib
    page = urllib.urlopen("http://www.genome.jp/kegg/catalog/org_list.html").read()
    urls = re.findall("<td.*</td>", page)
    pattern=re.compile(scientific_name)
    three_pattern=re.compile("<td align=center><a href=\'.*\?org=([a-z][a-z][a-z])\'>[a-z][a-z][a-z]</a></td>")

    #filtered = [i for i in list_of_names if not pre_pattern.search(i)]
    #\n<td.*</td>"
                      #+
                      #"<td align=center><a.*org=([a-za-za-za-z]).*\n"+
                      #".*"+scientific_name+".*</td>"
    #"<td align=center><a href='/kegg-bin/show_organism?org="
    for url in urls:
        new=url
        mo=pattern.search(new)
        if mo:
            #print new
            #print old
            tpm=three_pattern.search(old)
            if tpm:
                return tpm.group(1)
        old=url

def make_genome_link(scientific_name,release):
    import httplib2
    from BeautifulSoup import BeautifulSoup, SoupStrainer
    species_name=scientific_name.lower()
    species_string=species_name.replace(" ", "_")
    directory="http://ftp.ensembl.org/pub/release-"+str(release)+"/fasta/"+species_string+"/dna/"
    directoryf="ftp://ftp.ensembl.org/pub/release-"+str(release)+"/fasta/"+species_string+"/dna/"
    http = httplib2.Http()
    status, response = http.request(directory)
    gpattern= ".*\"(.*\.dna\.primary_assembly\.fa\.gz)\""
    gpattern1= ".*\"(.*\.dna\.toplevel\.fa\.gz)\""
    m=False
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        match= re.match(gpattern, str(link))
        if match:
            return directoryf+ match.group(1)
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        match= re.match(gpattern1, str(link))
        if match:
            return directoryf+ match.group(1)

def make_cdna_link(scientific_name,release):
    import httplib2
    from BeautifulSoup import BeautifulSoup, SoupStrainer
    species_name=scientific_name.lower()
    species_string=species_name.replace(" ", "_")
    directory="http://ftp.ensembl.org/pub/release-"+str(release)+"/fasta/"+species_string+"/cdna/"
    directoryf="ftp://ftp.ensembl.org/pub/release-"+str(release)+"/fasta/"+species_string+"/cdna/"
    http = httplib2.Http()
    status, response = http.request(directory)
    cpattern= ".*\"(.*\.cdna\.all\.fa\.gz)\""
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        match= re.match(cpattern, str(link))
        if match:
            return directoryf + match.group(1)

def make_cds_link(scientific_name,release):
    import httplib2
    from BeautifulSoup import BeautifulSoup, SoupStrainer
    species_name=scientific_name.lower()
    species_string=species_name.replace(" ", "_")
    directory="http://ftp.ensembl.org/pub/release-"+str(release)+"/fasta/"+species_string+"/cds/"
    directoryf="ftp://ftp.ensembl.org/pub/release-"+str(release)+"/fasta/"+species_string+"/cds/"
    http = httplib2.Http()
    status, response = http.request(directory)
    cpattern= ".*\"(.*\.cds\.all\.fa\.gz)\""
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        match= re.match(cpattern, str(link))
        if match:
            return directoryf + match.group(1)

def make_ncrna_link(scientific_name,release):
    import httplib2
    from BeautifulSoup import BeautifulSoup, SoupStrainer
    species_name=scientific_name.lower()
    species_string=species_name.replace(" ", "_")
    directory="http://ftp.ensembl.org/pub/release-"+str(release)+"/fasta/"+species_string+"/ncrna/"
    directoryf="ftp://ftp.ensembl.org/pub/release-"+str(release)+"/fasta/"+species_string+"/ncrna/"
    http = httplib2.Http()
    status, response = http.request(directory)
    cpattern= ".*\"(.*\.ncrna\.fa\.gz)\""
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        match= re.match(cpattern, str(link))
        if match:
            return directoryf + match.group(1)
#
def make_gff_link(scientific_name,release):
    import httplib2
    from BeautifulSoup import BeautifulSoup, SoupStrainer
    species_name=scientific_name.lower()
    species_string=species_name.replace(" ", "_")
    directory="http://ftp.ensembl.org/pub/release-"+str(release)+"/gff3/"+species_string+"/"
    directoryf="ftp://ftp.ensembl.org/pub/release-"+str(release)+"/gff3/"+species_string+"/"
    http = httplib2.Http()
    status, response = http.request(directory)
    #cpattern= ".*\"(.*\."+str(release)+"\.gff3\.gz)\""
    cpattern = ".*\"(.*\." + str(release) + "\.gff3\.gz)\""
    cpattern_1=".*\"(.*\." + str(release-1) + "\.gff3\.gz)\""
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        match= re.match(cpattern, str(link))
        match1=re.match(cpattern_1, str(link))
        if match:
            return directoryf + match.group(1)
        elif match1:
            return directoryf + match1.group(1)
    return "---"


#print grab_kegg_name("Felis catus")
#print make_gff_link("Mus caroli",91)

#print grab_kegg_name("Rattus norvegicus")

#mirbase file with hairpins
mirbase_hairpins="C:\Users\Ernesto\Desktop\hairpin.fa"
#ensembl table

#ensembl_csv="genome_table.csv" #downloaded from http://www.ensembl.org/info/about/species.html
ensembl_csv="genoTable91.csv" #downloaded from http://www.ensembl.org/info/about/species.html
#list of species (common name) to be included
path_to_list="list_of_genomes.json"
ensembl_url="http://www.ensembl.org/info/data/ftp/index.html"

with open(path_to_list) as json_data:
    list_of_genomes = json.load(json_data)

for e in list_of_genomes:
    print grab_assembly_name(e,"genome_table.csv")
    print grab_scientific_name(e,"genome_table.csv" )
    print grab_taxon_ID(e, "genome_table.csv")
    print grab_short_name(grab_scientific_name(e,"genome_table.csv" ), mirbase_hairpins)
    print
    print


#make list of species

list_of_names=list()
with open(ensembl_csv, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        list_of_names.append(row[0])

list_of_names.pop(0)
#\(Pre\)
pre_pattern= re.compile("\(Pre\)")
filtered = [i for i in list_of_names if not pre_pattern.search(i)]
rem=[i for i in list_of_names if pre_pattern.search(i)]

print len(filtered),len(list_of_names)

filtered=["Gorilla gorilla"]

# for e in filtered:
#     print e
#     #print grab_assembly_name(e,"genome_table.csv")
#     #print grab_scientific_name(e,"genome_table.csv" )
#     #print grab_taxon_ID(e, "genome_table.csv")
#
#     print make_genome_link(e, 88)
#     print grab_short_name(e, mirbase_hairpins)
#     print make_cdna_link(e, 88)
#     print make_cds_link(e, 88)
#     print make_ncrna_link(e, 88)
#     print make_gff_link(e,88)
#
#     print

def build_input_table(release, input_file):

    name_bits = input_file.split(".")[:-1]
    name_bits[-1] = name_bits[-1] + "_strings.txt"

    output_file = ".".join(name_bits)
    print(output_file)

    ensembl_csv = input_file

    list_of_names=list()
    with open(ensembl_csv, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            list_of_names.append(row[0])

    list_of_names.pop(0)
    pre_pattern = re.compile("\(Pre\)")
    filtered = [i for i in list_of_names if not pre_pattern.search(i)]
    #filtered= ["Dog"]
    with open(output_file, "wb") as g:
        for n in filtered:
            print "writing " +n
            str8= grab_scientific_name(n,ensembl_csv)
            str0= make_genome_link(str8,release)
            str1= grab_assembly_name(n,ensembl_csv)
            str2= str1+"_mp"
            str4=grab_short_name(str8,mirbase_hairpins)

            str5= make_cdna_link(str8,release)
            str6= make_cds_link(str8,release)
            str7= make_ncrna_link(str8,release)
            str9="animal"
            str10= grab_taxon_ID(n,ensembl_csv)
            str11= make_gff_link(str8,release)
            str12=n
            str13= "true"
            if str4 == "---":
                str14= "false"
            else:
                str14= "true"
            if str4 == "---":
                str3 = grab_kegg_name(str8)

                if str3:
                    str4=str3
                    str3=":"+str3
                else:
                    str3=":"+str8.replace(" ","_")
            else:
                str3= ":"+str4

            #line="genome=" + ";".join([str0,str1,str2,str3,str4,str5,str6,str7,str8,str9,str10,str11,str12,str13,str14])
            if (n in exceptions.keys()):
                str8=exceptions[n]+":"+exceptions2[n]
            if  not any(elem is None for elem in [str0, str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11, str12, str13, str14]):
                line =  "\t".join([str0, str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11, str12, str13, str14])

            else:
                col=['Not found' if v is None else v for v in [str0, str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11, str12, str13, str14] ]
                line="\t".join(col)
                print "######Some empty fields!!!"
            g.write("#" + str8 + "\n")
            g.write(line + "\n")

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



#build_input_table(91,"animals91.tsv")
make_strings("plants37.tsv", "plants37_v1.txt")

#base de datos de virus: https://www.viprbrc.org/brc/home.spg?decorator=vipr
#y de virus de plantas: http://www.dpvweb.net/

#ncbi viruses
#https://www.ncbi.nlm.nih.gov/genomes/GenomesGroup.cgi?taxid=10239#


exit()



list_of_names=list()
with open(ensembl_csv, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        list_of_names.append(row[0])

print list_of_names

list_of_names.pop(0)
pre_pattern = re.compile("\(Pre\)")
filtered = [i for i in list_of_names if not pre_pattern.search(i)]
#filtered= ["Dog"]
for n in filtered:
    print grab_scientific_name(n,ensembl_csv)
    print grab_kegg_name(grab_scientific_name(n,ensembl_csv))
exit()


grab_kegg_name("Rattus norvegicus")

exit()
make_strings("here.txt", "animal.txt")

exit()





#

build_input_table(88, "here.txt")


