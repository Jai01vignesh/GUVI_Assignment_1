# importing dependencies
import pandas as pd
import docx2txt

df_temp = pd.read_excel("census_2011.xlsx")
#print(df_temp.head())


#Task 1: Rename the Column names - using rename function
renamed_col_dict ={'District code':'District_code',
                   'State name': 'State/UT',
                   'District name': 'District',
                   'Male_Literate': 'Literate_Male',
                   'Female_Literate': 'Literate_Female',
                   'Rural_Households': 'Households_Rural',
                   'Urban_ Households': 'Households_Urban',
                   'Age_Group_0_29': 'Young_and_Adult',
                   'Age_Group_30_49': 'Middle_Aged',
                   'Age_Group_50': 'Senior_Citizen',
                   'Age not stated': 'Age_Not_Stated'}
df_temp.rename(columns =renamed_col_dict,inplace=True)
print(df_temp.columns)

#Task 2: Task 2: Rename State/UT Names
def rename_state(name):
    name_lst = name.split()
    cnvrtd_name_lst = []
    for nme in name_lst:
        if nme  == "AND":
            cnvrtd_name_lst.append(nme.lower())
        else:
            cnvrtd_name_lst.append(nme.capitalize())
    return(" ".join(cnvrtd_name_lst))


df_temp["State/UT"] = df_temp["State/UT"].apply(rename_state)
print(df_temp['State/UT'].unique())

#Task 3: New State/UT formation

my_text = docx2txt.process("Telangana.docx")

def rename_state(df_temp):
    for nme in my_text.split():
        df_temp.loc[df_temp['District'] == nme, 'State/UT'] ="Telangana"
    df_temp.loc[df_temp['District'].isin (['Leh(Ladakh)','Kargil']), 'State/UT'] ="Ladakh"

rename_state(df_temp)
print(df_temp['District'].loc[df_temp['State/UT'] .isin (['Ladakh','Telangana'])])