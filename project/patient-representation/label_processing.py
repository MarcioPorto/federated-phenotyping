import pandas

d_icd = "/Users/saksham/Desktop/os/federated-phenotyping/project/patient-representation/DIAGNOSES_ICD.csv"
p_icd = "/Users/saksham/Desktop/os/federated-phenotyping/project/patient-representation/PROCEDURES_ICD.csv"
code_col = "ICD9_CODE"
prefix = "diag"
num_digits = 3
# maps subj_id to set of icd9 codes
subj2codes = {}

def map_subjects_to_codes(code_file,code_col,num_digits):
    frame = pandas.read_csv(code_file)
    for subj_id, code in zip(frame.SUBJECT_ID, frame[code_col]):
        if subj_id not in subj2codes:
            subj2codes[subj_id] = set()
        # short_code = '%s_%s' % (prefix, str(code)[0:num_digits])
        short_code = str(code)[0:num_digits]
        subj2codes[subj_id].add(short_code)

map_subjects_to_codes(d_icd,code_col,3)
map_subjects_to_codes(p_icd,code_col,2)

for key in subj2codes:
    file_path = "/Users/saksham/Desktop/os/federated-phenotyping/project/patient-representation/labels/" + str(key) + ".txt"
    f = open(file_path, "a")
    for code in subj2codes[key]:
        f.write(code)
        f.write("\n")
    f.close()