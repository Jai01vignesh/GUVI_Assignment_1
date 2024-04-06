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
                   'Urban_Households': 'Households_Urban',
                   'Age_Group_0_29': 'Young_and_Adult',
                   'Age_Group_30_49': 'Middle_Aged',
                   'Age_Group_50': 'Senior_Citizen',
                   'Age not stated': 'Age_Not_Stated'}
df_temp.rename(columns =renamed_col_dict,inplace=True)
#-Ans print(df_temp.columns)

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
#-Ans print(df_temp['State/UT'].unique())

#Task 3: New State/UT formation

my_text = docx2txt.process("Telangana.docx")

def rename_state(df_temp):
    for nme in my_text.split():
        df_temp.loc[df_temp['District'] == nme, 'State/UT'] ="Telangana"
    df_temp.loc[df_temp['District'].isin (['Leh(Ladakh)','Kargil']), 'State/UT'] ="Ladakh"

rename_state(df_temp)
#-Ans print(df_temp['District'].loc[df_temp['State/UT'] .isin (['Ladakh','Telangana'])])

#Task 4: Find and process Missing Data
def impute_missing_values1(total,col1,col2):
    if total != total:
       total = col1 + col2
    elif col1 != col1:
        col1 = total - col2
    elif col2 != col2:
        col2 = total - col1
    else:
        total, col1, col2
    
    return total, col1, col2


def impute_missing_values(total,col1,col2,col3,col4):
    if  col1 != col1:
        col1 = total - col2 - col3 - col4
    elif col2 != col2:
        col2 = total - col1 - col3 - col4
    elif col3 != col3:
        col3 = total - col1 - col2 - col4
    elif col4 != col4:
        col4 = total - col1 - col2 - col3
    else:
        col1, col2, col3, col4
    
    return col1, col2, col3, col4

print(df_temp.isnull().sum(axis=0))
df_temp[['Population','Male','Female']] = df_temp.apply(lambda row :impute_missing_values1(row['Population'],row['Male'],row['Female']),axis=1,result_type= 'expand')
df_temp[['Literate','Literate_Male','Literate_Female']] = df_temp.apply(lambda row :impute_missing_values1(row['Literate'],row['Literate_Male'],row['Literate_Female']),axis=1,result_type= 'expand')
df_temp[['Households','Households_Rural','Households_Urban']] = df_temp.apply(lambda row :impute_missing_values1(row['Households'],row['Households_Rural'],row['Households_Urban']),axis=1,result_type= 'expand')
df_temp[['Young_and_Adult','Middle_Aged','Senior_Citizen','Age_Not_Stated']] = df_temp.apply(lambda row :impute_missing_values(row['Population'],row['Young_and_Adult'],row['Middle_Aged'],row['Senior_Citizen'],row['Age_Not_Stated']),axis=1,result_type= 'expand')

print(df_temp.isnull().sum(axis=0))
#df_temp.to_csv("1.csv")