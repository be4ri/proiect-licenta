import pandas as pd
import logic.analyzer as analyzer
import logic.add_snp_command as add_snp_command
import logic.remove_snp_command as remove_snp_command
import logic.snp_command_invoker as snp_command_invoker
import logic.filtering_patient_snp as filtering_patient_snp

def menu():
    print("Menu")
    print("1. The number of SNPs from the panel that are found in the GRPM Nutrigen dataset.")
    print("2. For each MeSH term, the number and proportion of SNPs associated with it.")
    print("3. The Shannon diversity index of MeSH terms per SNP.")
    print("4. The Shannon diversity index of SNPs per MeSH term.")
    print("5. Get the patients rsid.")
    print("6. Create a CSV file with the patients rsid.")
    print("7. Get the merged patients GRPM Nutrigen.")
    print("8. Add a new SNP to the patients CSV file.")
    print("9. Remove a SNP from the patients CSV file.")
    print("10. Undo last action.")
    print("11. Redo last undone action.")
    print("12. Filter patients by rsid.")
    print("13. Filter patients by chromosome.")
    print("14. Filter patients by position.")
    print("15. Filter patients by EXCG46.")
    print("0. Exit ")
    analyzer_instance = analyzer.Analyzer()
    editor = snp_command_invoker.SNPCommandInvoker(analyzer_instance.patients_panel)
    filtering_patients_instance = filtering_patient_snp.FilteringPatientSNP()
    while True:
        option = input("Select an option: ")
        match option:
            case '1':
                #analyzer_instance = analyzer.Analyzer()
                analyzer_instance.number_of_snps_matching()
                matching_snps = analyzer_instance.matching_snps()
                print("Matching SNPs:", matching_snps)
            case '2':
                #analyzer_instance = analyzer.Analyzer()
                mesh_results = analyzer_instance.mesh_statistics()
                print(mesh_results)
            case '3':
                #analyzer_instance = analyzer.Analyzer()
                shannon_results = analyzer_instance.shannon_index_per_snp()
                print(shannon_results)
            case '4':
                #analyzer_instance = analyzer.Analyzer()
                shannon_results_mesh = analyzer_instance.shannon_index_per_mesh()
                print(shannon_results_mesh)
            case '5':
                #analyzer_instance = analyzer.Analyzer()
                print("Nothing to show")
            case '6':
                #analyzer_instance = analyzer.Analyzer()
                analyzer_instance.create_csv_file_patients_rsid()
                print("CSV file with patients rsid created successfully.")
            case '7':
                #analyzer_instance = analyzer.Analyzer()
                merged_patients_grpm_nutrigen = analyzer_instance.get_merged_patients_grpm_nutrigen()
                print(merged_patients_grpm_nutrigen)
            case '8':
                #analyzer_instance = analyzer.Analyzer()
                try:
                    GRPM_RSID = input("Enter the GRPM_RSID: ")
                    Chr = input("Enter the Chr: ")  
                    Position = input("Enter the Position: ")
                    EXCG46 = input("Enter the EXCG46: ")
                except ValueError as ve:
                    print(ve)
                    continue
                add_command = add_snp_command.AddSNPCommand(analyzer_instance.patients_panel, GRPM_RSID, Chr, Position, EXCG46)
                editor.execute_add(GRPM_RSID, Chr, Position, EXCG46)
                print("SNP added successfully.")
            case '9':
                #analyzer_instance = analyzer.Analyzer()
                try:
                    GRPM_RSID = input("Enter the GRPM_RSID: ")
                    Chr = input("Enter the Chr: ")  
                    Position = input("Enter the Position: ")
                    EXCG46 = input("Enter the EXCG46: ")
                except ValueError as ve:
                    print(ve)
                    continue
                remove_command = remove_snp_command.RemoveSNPCommand(analyzer_instance.patients_panel, GRPM_RSID, Chr, Position, EXCG46)
                editor.execute_remove(GRPM_RSID, Chr, Position, EXCG46)
                print("SNP removed successfully.")
            case '10':
                #analyzer_instance = analyzer.Analyzer()
                editor.undo()
                print("Last action undone.")
            case '11':
                #analyzer_instance = analyzer.Analyzer()
                editor.redo()
                print("Last undone action redone.")
            case '12':
                rsid = input("Enter the GRPM_RSID to filter by: ")
                filtered_by_rsid = filtering_patients_instance.filter_by_rsid(rsid)
                print(filtered_by_rsid)
            case '13':
                chr_val = input("Enter the chromosome to filter by: ")
                filtered_by_chr = filtering_patients_instance.filter_by_chr(chr_val)
                print(filtered_by_chr)
            case '14':
                position = input("Enter the position to filter by: ")
                filtered_by_position = filtering_patients_instance.filter_by_position(position)
                print(filtered_by_position)
            case '15':
                excg46 = input("Enter the EXCG46 value to filter by: ")
                filtered_by_excg46 = filtering_patients_instance.filter_by_excg46(excg46)
                print(filtered_by_excg46)
            case '0':
                break
            case _:
                print("Invalid option.")

def main():
    menu()

if __name__ == "__main__":
    main()