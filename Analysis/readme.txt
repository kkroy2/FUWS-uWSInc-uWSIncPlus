partition_init_.py

input: Files/datasets/accidents_sp.txt (which is already assgined with probability)

generates folder under Files/accidents

            sub-folder name accidents_(p0 size %)_(no of increments)

                        Files/accidents/accidents_10_9

                        and create files accidents_i.txt

                                   Files/accidents/accidents_10_9/accidents_0.txt
                                   Files/accidents/accidents_10_9/accidents_1.txt

---------------------------

analysis_init_.py

input dataset name: sign
input folder (relative path): Files/sign/sign_50_5
then 4 different threshold to run

