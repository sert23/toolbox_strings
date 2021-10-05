import csv
import re

mirbase_hairpins = "C:/Users/Ernesto/PycharmProjects/Ensembl_parser/releaseSept2019/hairpin.fa"

exceptions={"Oryza sativa Indica":"Oryza indica","Oryza sativa Japonica" : "Oryza sativa", "Beta vulgaris subsp. vulgaris": "Beta vulgaris"}
exceptions2={"Oryza indica":"Oryza sativa:Oryza sativa indica","Oryza sativa" : "Oryza sativa:Oryza sativa Japonica", "Beta vulgaris":"Beta vulgaris:Beta vulgaris subsp. vulgaris"}

def grab_assembly_name(scientific,csv_table):
    with open(csv_table, 'rb') as f:
        # reader = csv.reader(f)
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
        #re.match(pattern, string, flags=0)
            if re.match("^"+scientific+"$", row[1]):
                output = row[4].replace(" ", "_")
                return output.replace(".", "_")

def grab_taxon_ID(scientific,csv_table):
    with open(csv_table, 'rb') as f:
        # reader = csv.reader(f)
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
        #re.match(pattern, string, flags=0)
            if re.match("^"+scientific+"$", row[1]):
                return row[3]

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

def make_genome_1(scientific_name,release):
    import httplib2
    from BeautifulSoup import BeautifulSoup, SoupStrainer
    species_name=scientific_name.lower()
    species_string=species_name.replace(" ", "_")
    directory="http://ftp.ensemblgenomes.org/pub/release-"+str(release)+"/plants/fasta/"+species_string+"/dna/"
    directoryf="ftp://ftp.ensemblgenomes.org/release-"+str(release)+"/plants/fasta/"+species_string+"/dna/"
    #ftp: // ftp.ensemblgenomes.org / pub / release - 35 / plants / fasta / aegilops_tauschii / dna /

    http = httplib2.Http()
    status, response = http.request(directoryf)
    gpattern= ".*\"(.*\.dna\.toplevel\.fa\.gz)\""

    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        match= re.match(gpattern, str(link))
        if match:
            return directoryf+ match.group(1)

def make_genome_link(scientific_name,release):
    from ftplib import FTP
    scientific_name= re.sub(" subsp\. [a-zA-Z]+", "",scientific_name )
    species_name = scientific_name.lower()
    species_string = species_name.replace(" ", "_")
    start_directory = "ftp.ensemblgenomes.org"
    directory="/pub/release-" + str(release) + "/plants/fasta/" + species_string + "/dna/"
    gpattern = "(.*\.dna\.toplevel\.fa\.gz)"

    #print start_directory + directory
    ftp = FTP(start_directory)  # connect to host, default port
    ftp.login()
    ftp.cwd(directory)
    files = ftp.nlst()
    for link in files:
        match = re.match(gpattern, link)
        if match:
            return "ftp://"+start_directory+directory+match.group(1)

def make_cdna_link(scientific_name,release):
    from ftplib import FTP
    scientific_name = re.sub(" subsp\. [a-zA-Z]+", "", scientific_name)
    species_name = scientific_name.lower()
    species_string = species_name.replace(" ", "_")
    start_directory = "ftp.ensemblgenomes.org"
    directory = "/pub/release-" + str(release) + "/plants/fasta/" + species_string + "/cdna/"
    cpattern= "(.*\.cdna\.all\.fa\.gz)"
    # print start_directory + directory
    ftp = FTP(start_directory)  # connect to host, default port
    ftp.login()
    ftp.cwd(directory)
    files = ftp.nlst()
    for link in files:
        match = re.match(cpattern, link)
        if match:
            return "ftp://" + start_directory + directory + match.group(1)

def make_cds_link(scientific_name,release):
    from ftplib import FTP
    scientific_name = re.sub(" subsp\. [a-zA-Z]+", "", scientific_name)
    species_name = scientific_name.lower()
    species_string = species_name.replace(" ", "_")
    start_directory = "ftp.ensemblgenomes.org"
    directory = "/pub/release-" + str(release) + "/plants/fasta/" + species_string + "/cds/"
    cpattern = "(.*\.cds\.all\.fa\.gz)"
    # print start_directory + directory
    ftp = FTP(start_directory)  # connect to host, default port
    ftp.login()
    ftp.cwd(directory)
    files = ftp.nlst()
    for link in files:
        match = re.match(cpattern, link)
        if match:
            return "ftp://" + start_directory + directory + match.group(1)

def make_ncrna_link(scientific_name,release):
    from ftplib import FTP
    scientific_name = re.sub(" subsp\. [a-zA-Z]+", "", scientific_name)
    species_name = scientific_name.lower()
    species_string = species_name.replace(" ", "_")
    start_directory = "ftp.ensemblgenomes.org"
    directory = "/pub/release-" + str(release) + "/plants/fasta/" + species_string + "/ncrna/"
    cpattern = "(.*\.ncrna\.fa\.gz)"
    # print start_directory + directory
    ftp = FTP(start_directory)  # connect to host, default port
    ftp.login()
    ftp.cwd(directory)
    files = ftp.nlst()
    for link in files:
        match = re.match(cpattern, link)
        if match:
            return "ftp://" + start_directory + directory + match.group(1)
    return "---"
#
def make_gff_link(scientific_name,release):
    from ftplib import FTP
    scientific_name = re.sub(" subsp\. [a-zA-Z]+", "", scientific_name)
    species_name = scientific_name.lower()
    species_string = species_name.replace(" ", "_")
    start_directory = "ftp.ensemblgenomes.org"
    directory = "/pub/release-" + str(release) + "/plants/gff3/" + species_string+ "/"
    cpattern = "(.*\." + str(release) + "\.gff3\.gz)"
    # print start_directory + directory
    ftp = FTP(start_directory)  # connect to host, default port
    ftp.login()
    ftp.cwd(directory)
    files = ftp.nlst()
    #print files
    for link in files:
        match = re.match(cpattern, link)
        if match:
            return "ftp://" + start_directory + directory + match.group(1)

#
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

def build_input_table(release, input_file):
    list_of_names=list()
    list_of_scientific=list()

    name_bits = input_file.split(".")[:-1]
    name_bits[-1] = name_bits[-1] + "_parsed.tsv"
    output_file = ".".join(name_bits)
    ensembl_csv = input_file
    with open(ensembl_csv, 'rb') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            list_of_names.append(row[1])
            list_of_scientific.append(row[0])

    list_of_scientific.pop(0)
    list_of_names.pop(0)
    pre_pattern = re.compile("(.*) subsp\. [a-zA-Z]+")
    filtered=list_of_names
        #[re.sub(" subsp\. [a-zA-Z]+","",w) for w in list_of_names ]
    with open(output_file, "wb") as g:
        for i, n in enumerate(filtered):
            print "writing " +n
            if (n in exceptions.keys()):
                str8=exceptions[n]
            else:
                str8 = list_of_scientific[i]

            str0= make_genome_link(n,release)
            str1= grab_assembly_name(n,ensembl_csv)
            str2= str1+"_mp"
            str4=grab_short_name(str8,mirbase_hairpins)

            str5= make_cdna_link(n,release)
            str6= make_cds_link(n,release)
            str7= make_ncrna_link(n,release)
            str9="plant"
            str10= grab_taxon_ID(n,ensembl_csv)
            str11= make_gff_link(n,release)
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
                str8=exceptions2[str8]
            if  not any(elem is None for elem in [str0, str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11, str12, str13, str14]):
                line =  "\t".join([str0, str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11, str12, str13, str14])

            else:
                col=['Not found' if v is None else v for v in [str0, str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11, str12, str13, str14] ]
                line="\t".join(col)
                print "######Some empty fields!!!"
            g.write("#" + str8 + "\n")
            g.write(line + "\n")

    return output_file
