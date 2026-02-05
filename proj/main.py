import pandas as pd
import app.analyzer as analyzer

def menu():
    print("Menu")
    print("1. The number of SNPs from the panel that are found in the GRPM Nutrigen dataset.")
    print("2. For each MeSH term, the number and proportion of SNPs associated with it.")
    print("3. The Shannon diversity index of MeSH terms per SNP.")
    print("4. The Shannon diversity index of SNPs per MeSH term.")
    print("0. Exit ")
    while True:
        option = input("Select an option: ")
        match option:
            case '1':
                analyzer_instance = analyzer.Analyzer()
                analyzer_instance.number_of_snps_matching()
            case '2':
                analyzer_instance = analyzer.Analyzer()
                mesh_results = analyzer_instance.mesh_statistics()
                print(mesh_results)
            case '3':
                analyzer_instance = analyzer.Analyzer()
                shannon_results = analyzer_instance.shannon_index_per_snp()
                print(shannon_results)
            case '4':
                analyzer_instance = analyzer.Analyzer()
                shannon_results_mesh = analyzer_instance.shannon_index_per_mesh()
                print(shannon_results_mesh)
            case '0':
                break
            case _:
                print("Invalid option.")

def main():
    menu()

if __name__ == "__main__":
    main()