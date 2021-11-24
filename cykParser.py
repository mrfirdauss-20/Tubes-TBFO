import re

# mapRegex = {
#     r'[A-Za-z_][A-Za-z_0-9]*' : ["variable"],
#     r'[0-9]*' : ["number"],
#     r'[A-z0-9]*' : ["string"],
# }
# listRegex = [r'[0-9]*', r'[A-Za-z_][A-Za-z_0-9]*', r'[A-z0-9]*']

global CNF
CNF = {}

def getCNF(pathCFG):
    file = open(pathCFG).read()
    grammarCNF = file.split('\n')
    lengthGrammar = len(grammarCNF) - 1

    for rule in range (lengthGrammar):
        #melakukan split antara lhs dengan rhs dan menghapus space antar item
        lhs = grammarCNF[rule].split(' -> ')[0]
        rhs = grammarCNF[rule].split(' -> ')[1]
        rhs = rhs.replace(" ", "")
        rhs = rhs.split('|')
        lengthRHS = len(rhs)
        #iterasi setiap item di RHS dan memetakan kemunculannya ada di LHS mana
        for item in range(lengthRHS):
            value = CNF.get(rhs[item])
            #jika belum pernah muncul, maka buat key baru
            if (value == None):
                CNF.update({rhs[item]: [lhs]})
            #jika sudah pernah muncul, maka tambahkan LHS kemunculan item dari RHS
            else:
                CNF[rhs[item]].append(lhs)
    print(CNF)

def cykParser(input):
    inputLength = len(input)
    print(inputLength)
    #inisialisasi pada tabel CYK
    table = [[[] for j in range(i)] for i in range((inputLength), 0, -1)]
    print(table)
    #mengisi baris awal dengan mencari apakah ada production yang cocok dengan input
    for i in range(inputLength):
        #apabila ada aturan produksi yang cocok dengan input, masukkan aturan produksi ke tabel
        try:
            table[0][i].extend(CNF[input[i]])
        except KeyError:
            continue
        #jika tidak ada, coba cek apakah itu sebuah string/number/variabel dengan regex
        # except KeyError:
        #     for targetText in listRegex:
        #         #jika ternyata string/number/variabel, masukkan aturan produksi tempat kemunculan hasil
        #         if(re.match(targetText, input[i])):
        #             for result in mapRegex[targetText]:
        #                 try:
        #                     table[0][i].extend(CNF[result])
        #                 except KeyError:
        #                     continue
    #mengisi tabel dengan algoritma CYK                    
    for i in range(1, inputLength):
        for j in range(inputLength-i):
            for k in range(i):
                #mencari semua aturan produksi dari hasil produksi
                for result1 in table[i-k-1][j]:
                    for result2 in table[k][j+i-k]:
                        try:
                            table[i][j] = CNF[result1+result2]
                        except KeyError:
                            continue
    
    for x in table:
        print(x)


    if("S" in table[inputLength-1][0]):
        print("Accepted")
    else:
        print("wrong syntax")
        for i in range(1, inputLength):
            for j in range(inputLength-i):
                for k in range(i):
                    #mencari semua aturan produksi dari hasil produksi
                    for result1 in table[i-k-1][j]:
                        for result2 in table[k][j+i-k]:
                            try:
                                table[i][j] = CNF[result1+result2]
                            except KeyError:
                                print("Error in : "+str(input[i]))   
                                return 0 
        
