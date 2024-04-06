# importing dependencies
import pandas as pd
import docx2txt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


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

def impute_missing_values2(total,col1,col2,col3,col4,col5):
    if  col1 != col1:
        col1 = total - col2 - col3 - col4- col5
    elif col2 != col2:
        col2 = total - col1 - col3 - col4- col5
    elif col3 != col3:
        col3 = total - col1 - col2 - col4- col5
    elif col4 != col4:
        col4 = total - col1 - col2 - col3- col5
    elif col5 != col5:
        col5 = total - col1 - col2 - col3 - col4
    else:
        col1, col2, col3, col4,col5
    
    return col1, col2, col3, col4,col5



def impute_missing_values3(total,col1,col2,col3,col4,col5,col6,col7,col8):
    if  total != total:
        total =col1 + col2 + col3 + col4 + col5 + col6+col7 +col8
    elif col1 != col1:
        col1 = total - col2 - col3 - col4- col5- col6-col7 -col8
    elif col2 != col2:
        col2 = total - col1 - col3 - col4- col5- col6-col7 -col8
    elif col3 != col3:
        col3 = total - col1 - col2 - col4- col5- col6-col7 -col8
    elif col4 != col4:
        col4 = total - col1 - col2 - col3- col5- col6-col7-col8
    elif col5 != col5:
        col5 = total - col1 - col2 - col3 - col4- col6-col7 -col8
    elif col6 != col6:
        col6 = total - col1 - col2 - col3 - col4- col5-col7 -col8
    elif col7 != col7:
        col7 = total - col1 - col2 - col3 - col4- col5 -col6 - col8
    elif col8 != col8:
        col8 = total - col1 - col2 - col3 - col4- col5 - col6 -col7
    else:
        total,col1, col2, col3, col4, col5, col6, col7, col8
    
    return total,col1, col2, col3, col4, col5, col6, col7, col8


def impute_missing_values4(total,col1,col2,col3,col4,col5,col6,col7):
    if  total != total:
        total =col1 + col2 + col3 + col4 + col5 + col6+col7 
    elif col1 != col1:
        col1 = total - col2 - col3 - col4- col5- col6-col7
    elif col2 != col2:
        col2 = total - col1 - col3 - col4- col5- col6-col7 
    elif col3 != col3:
        col3 = total - col1 - col2 - col4- col5- col6-col7 
    elif col4 != col4:
        col4 = total - col1 - col2 - col3- col5- col6-col7
    elif col5 != col5:
        col5 = total - col1 - col2 - col3 - col4- col6-col7 
    elif col6 != col6:
        col6 = total - col1 - col2 - col3 - col4- col5-col7
    elif col7 != col7:
        col7 = total - col1 - col2 - col3 - col4- col5 -col6 
    else:
        total,col1, col2, col3, col4, col5, col6, col7
    
    return total,col1, col2, col3, col4, col5, col6, col7


print(df_temp.isnull().sum(axis=0))
df_temp[['Population','Male','Female']] = df_temp.apply(lambda row :impute_missing_values1(row['Population'],row['Male'],row['Female']),axis=1,result_type= 'expand')
df_temp[['Literate','Literate_Male','Literate_Female']] = df_temp.apply(lambda row :impute_missing_values1(row['Literate'],row['Literate_Male'],row['Literate_Female']),axis=1,result_type= 'expand')
df_temp[['Households','Households_Rural','Households_Urban']] = df_temp.apply(lambda row :impute_missing_values1(row['Households'],row['Households_Rural'],row['Households_Urban']),axis=1,result_type= 'expand')
df_temp[['SC','Male_SC','Female_SC']] = df_temp.apply(lambda row :impute_missing_values1(row['SC'],row['Male_SC'],row['Female_SC']),axis=1,result_type= 'expand')
df_temp[['ST','Male_ST','Female_ST']] = df_temp.apply(lambda row :impute_missing_values1(row['ST'],row['Male_ST'],row['Female_ST']),axis=1,result_type= 'expand')
df_temp[['Workers','Male_Workers','Female_Workers']] = df_temp.apply(lambda row :impute_missing_values1(row['Workers'],row['Male_Workers'],row['Female_Workers']),axis=1,result_type= 'expand')
df_temp[['Workers','Main_Workers','Marginal_Workers']] = df_temp.apply(lambda row :impute_missing_values1(row['Workers'],row['Main_Workers'],row['Marginal_Workers']),axis=1,result_type= 'expand')
df_temp[['Total_Education','Literate_Education','Illiterate_Education']] = df_temp.apply(lambda row :impute_missing_values1(row['Total_Education'],row['Literate_Education'],row['Illiterate_Education']),axis=1,result_type= 'expand')


df_temp[['Young_and_Adult','Middle_Aged','Senior_Citizen','Age_Not_Stated']] = df_temp.apply(lambda row :impute_missing_values(row['Population'],row['Young_and_Adult'],row['Middle_Aged'],row['Senior_Citizen'],row['Age_Not_Stated']),axis=1,result_type= 'expand')

df_temp[['Non_Workers','Cultivator_Workers','Agricultural_Workers','Household_Workers','Other_Workers']] = df_temp.apply(lambda row :impute_missing_values2(row['Population'],row['Non_Workers'],row['Cultivator_Workers'],row['Agricultural_Workers'],row['Household_Workers'],row['Other_Workers']),axis=1,result_type= 'expand')

df_temp[['Population','Hindus','Muslims','Christians','Sikhs','Buddhists','Jains','Others_Religions','Religion_Not_Stated']] = df_temp.apply(lambda row :impute_missing_values3(row['Population'],row['Hindus'],row['Muslims'],row['Christians'],row['Sikhs'],row['Buddhists'],row['Jains'],row['Others_Religions'],row['Religion_Not_Stated']),axis=1,result_type= 'expand')
df_temp[['Literate_Education','Below_Primary_Education','Primary_Education','Middle_Education','Secondary_Education','Higher_Education','Graduate_Education','Other_Education']] = df_temp.apply(lambda row :impute_missing_values4(row['Literate_Education'],row['Below_Primary_Education'],row['Primary_Education'],row['Middle_Education'],row['Secondary_Education'],row['Higher_Education'],row['Graduate_Education'],row['Other_Education']),axis=1,result_type= 'expand')

print(df_temp.isnull().sum(axis=0))
#df_temp.to_csv("new.csv")