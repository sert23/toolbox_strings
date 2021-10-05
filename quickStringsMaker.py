from clean_strings import build_input_table,make_strings, grab_short_name
from plant_strings import build_input_table as build_plants_table
from metazoan_strings import build_input_table as build_metazoa_table




print("hey")
mirbase_hairpins = "C:/Users/Ernesto/PycharmProjects/Ensembl_parser/releaseSept2019/hairpin.fa"

#new functions

def run_string_maker(input_file,release):
    parsed_table = build_input_table(release, input_file)
    strings_file = parsed_table.replace("_parsed.tsv","_strings.txt")
    make_strings(parsed_table,strings_file)

def run_plant_string_maker(input_file,release):
    parsed_table = build_plants_table(release, input_file)
    strings_file = parsed_table.replace("_parsed.tsv", "_strings.txt")
    make_strings(parsed_table, strings_file)

def run_metazoan_string_maker(input_file,release):
    parsed_table = build_metazoa_table(release, input_file)
    strings_file = parsed_table.replace("_parsed.tsv", "_strings.txt")
    make_strings(parsed_table, strings_file)

#ensembl

#first download table from here ensembl http://www.ensembl.org/info/about/species.html
#go to table upper right corner and click on the Excel-like icon and then download whole table
#file name is Species.csv

# print(grab_short_name("Aedes aegypti", mirbase_hairpins))
#
# exit()

# run_string_maker("C:/Users/Ernesto/PycharmProjects/Ensembl_parser/data_sept19/ensembl/97/genomes.csv", 97)
# run_metazoan_string_maker("C:/Users/Ernesto/PycharmProjects/Ensembl_parser/data_sept19/ensembl_metazoa/44/genomes.tsv", 44)
run_plant_string_maker("C:/Users/Ernesto/PycharmProjects/Ensembl_parser/data_sept19/ensembl_plants/44/genomes.tsv", 44)

# run_string_maker("C:/Users/Ernesto/PycharmProjects/Ensembl_parser/test/ensembl_short.csv", 97)
# "C:\Users\Ernesto\PycharmProjects\Ensembl_parser\data_sept19\ensembl\97\genomes.csv"


exit()