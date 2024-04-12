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
print(df_temp.isnull().sum(axis=0).sum())
#Task 4: Find and process Missing Data
def fill_missing_values(df_temp):
    if df_temp['Population'] != df_temp['Population'] :
        if df_temp['Male'] == df_temp['Male'] and df_temp['Female'] == df_temp['Female']:
            df_temp['Population'] = df_temp['Male'] + df_temp['Female']
        elif df_temp['Main_Workers'] == df_temp['Main_Workers']and df_temp['Marginal_Workers'] == df_temp['Marginal_Workers']and df_temp['Non_Workers'] == df_temp['Non_Workers']:
            df_temp['Population'] = df_temp['Main_Workers'] + df_temp['Marginal_Workers']+ df_temp['Non_Workers']
    
    if df_temp['Male'] != df_temp['Male'] :
        if df_temp['Population'] == df_temp['Population']and df_temp['Female'] == df_temp['Female']:
            df_temp['Male'] = df_temp['Population'] - df_temp['Female']

    if df_temp['Female'] != df_temp['Female'] :
        if df_temp['Population'] == df_temp['Population']and df_temp['Male'] == df_temp['Male']:
            df_temp['Female'] = df_temp['Population'] - df_temp['Male']



    if df_temp['Literate'] != df_temp['Literate'] and  df_temp['Literate_Female'] == df_temp['Literate_Female'] and df_temp['Literate_Male'] == df_temp['Literate_Male']:
        df_temp['Literate']  = df_temp['Literate_Male'] + df_temp['Literate_Female']
    elif df_temp['Literate'] == df_temp['Literate'] and df_temp['Literate_Male'] == df_temp['Literate_Male']:
         df_temp['Literate_Female'] = df_temp['Literate'] - df_temp['Literate_Male']
    elif df_temp['Literate'] == df_temp['Literate'] and df_temp['Literate_Female'] == df_temp['Literate_Female']:
         df_temp['Literate_Male'] = df_temp['Literate'] - df_temp['Literate_Female']       


    if df_temp['Female_SC'] == df_temp['Female_SC'] and df_temp['Male_SC'] == df_temp['Male_SC'] and df_temp['SC'] != df_temp['SC']:
        df_temp['SC']  = df_temp['Male_SC'] + df_temp['Female_SC']
    elif df_temp['SC'] == df_temp['SC'] and df_temp['Male_SC'] == df_temp['Male_SC']:
         df_temp['Female_SC'] = df_temp['SC'] - df_temp['Male_SC']
    elif df_temp['SC'] == df_temp['SC'] and df_temp['Female_SC'] == df_temp['Female_SC']:
         df_temp['Male_SC'] = df_temp['SC'] - df_temp['Female_SC']



    if df_temp['ST'] != df_temp['ST'] and df_temp['Female_ST'] == df_temp['Female_ST'] and df_temp['Male_ST'] == df_temp['Male_ST']:
            df_temp['ST']  = df_temp['Male_ST'] + df_temp['Female_ST']
    elif df_temp['ST'] == df_temp['ST'] and df_temp['Male_ST'] == df_temp['Male_ST']:
            df_temp['Female_ST'] = df_temp['ST'] - df_temp['Male_ST']
    elif df_temp['ST'] == df_temp['ST'] and df_temp['Female_ST'] == df_temp['Female_ST']:
            df_temp['Male_ST'] = df_temp['ST'] - df_temp['Female_ST']      
            



   
    if df_temp['Workers'] != df_temp['Workers'] and df_temp['Main_Workers'] == df_temp['Main_Workers'] and df_temp['Marginal_Workers'] == df_temp['Marginal_Workers']:
        df_temp['Workers'] = df_temp['Main_Workers'] + df_temp['Marginal_Workers']
    elif df_temp['Cultivator_Workers'] == df_temp['Cultivator_Workers']and df_temp['Agricultural_Workers'] == df_temp['Agricultural_Workers']and df_temp['Household_Workers'] == df_temp['Household_Workers']and df_temp['Other_Workers'] == df_temp['Other_Workers']:
        df_temp['Workers'] = df_temp['Cultivator_Workers'] + df_temp['Agricultural_Workers']+ df_temp['Household_Workers']+ df_temp['Other_Workers']
    elif df_temp['Non_Workers'] == df_temp['Non_Workers']:
        df_temp['Workers'] = df_temp['Population'] - df_temp['Non_Workers']

    if df_temp['Main_Workers'] != df_temp['Main_Workers'] and df_temp['Marginal_Workers'] == df_temp['Marginal_Workers']and df_temp['Workers'] == df_temp['Workers']:
        df_temp['Main_Workers'] = df_temp['Workers'] - df_temp['Marginal_Workers']

    if df_temp['Marginal_Workers'] != df_temp['Marginal_Workers'] and df_temp['Main_Workers'] == df_temp['Main_Workers']and df_temp['Workers'] == df_temp['Workers']:
        df_temp['Marginal_Workers'] = df_temp['Workers'] - df_temp['Main_Workers']

    df_temp['Non_Workers'] = df_temp['Population'] - df_temp['Workers']

    df_temp['Male_Workers'] = df_temp['Workers'] - df_temp['Female_Workers']
    df_temp['Female_Workers'] = df_temp['Workers'] - df_temp['Male_Workers']

    if df_temp['Workers'] == df_temp['Workers']: 
        if df_temp['Cultivator_Workers'] != df_temp['Cultivator_Workers'] and df_temp['Agricultural_Workers'] == df_temp['Agricultural_Workers']and df_temp['Household_Workers'] == df_temp['Household_Workers']and df_temp['Other_Workers'] == df_temp['Other_Workers']:
            df_temp['Cultivator_Workers'] = df_temp['Workers']- df_temp['Agricultural_Workers'] - df_temp['Household_Workers'] - df_temp['Other_Workers']
        elif df_temp['Agricultural_Workers'] != df_temp['Agricultural_Workers'] and df_temp['Cultivator_Workers'] == df_temp['Cultivator_Workers']and df_temp['Household_Workers'] == df_temp['Household_Workers']and df_temp['Other_Workers'] == df_temp['Other_Workers']:
            df_temp['Agricultural_Workers'] = df_temp['Workers']- df_temp['Cultivator_Workers'] - df_temp['Household_Workers'] - df_temp['Other_Workers']
        elif df_temp['Household_Workers'] != df_temp['Household_Workers'] and df_temp['Agricultural_Workers'] == df_temp['Agricultural_Workers']and df_temp['Cultivator_Workers'] == df_temp['Cultivator_Workers']and df_temp['Other_Workers'] == df_temp['Other_Workers']:
            df_temp['Household_Workers'] = df_temp['Workers']- df_temp['Agricultural_Workers'] - df_temp['Cultivator_Workers'] - df_temp['Other_Workers']
        elif df_temp['Other_Workers'] != df_temp['Other_Workers'] and df_temp['Agricultural_Workers'] == df_temp['Agricultural_Workers']and df_temp['Household_Workers'] == df_temp['Household_Workers']and df_temp['Cultivator_Workers'] == df_temp['Cultivator_Workers']:
            df_temp['Other_Workers'] = df_temp['Workers']- df_temp['Agricultural_Workers'] - df_temp['Household_Workers'] - df_temp['Cultivator_Workers']

    
    if df_temp['Hindus'] == df_temp['Hindus'] and df_temp['Muslims'] == df_temp['Muslims']and df_temp['Christians'] == df_temp['Christians'] and df_temp['Sikhs'] == df_temp['Sikhs'] and df_temp['Buddhists'] == df_temp['Buddhists'] and df_temp['Jains'] == df_temp['Jains']and df_temp['Others_Religions'] == df_temp['Others_Religions']:
         df_temp['Religion_Not_Stated'] =  df_temp['Population'] -df_temp['Hindus'] - df_temp['Muslims']- df_temp['Christians'] -df_temp['Sikhs'] - df_temp['Buddhists']- df_temp['Jains'] -df_temp['Others_Religions']
    elif df_temp['Religion_Not_Stated'] == df_temp['Religion_Not_Stated']and df_temp['Muslims'] == df_temp['Muslims']and df_temp['Christians'] == df_temp['Christians'] and df_temp['Sikhs'] == df_temp['Sikhs'] and df_temp['Buddhists'] == df_temp['Buddhists'] and df_temp['Jains'] == df_temp['Jains']and df_temp['Others_Religions'] == df_temp['Others_Religions']:
         df_temp['Hindus'] =  df_temp['Population'] -df_temp['Religion_Not_Stated'] - df_temp['Muslims'] - df_temp['Christians'] -df_temp['Sikhs'] - df_temp['Buddhists']- df_temp['Jains'] -df_temp['Others_Religions']
    elif df_temp['Religion_Not_Stated'] == df_temp['Religion_Not_Stated']and df_temp['Hindus'] == df_temp['Hindus']and df_temp['Christians'] == df_temp['Christians'] and df_temp['Sikhs'] == df_temp['Sikhs'] and df_temp['Buddhists'] == df_temp['Buddhists'] and df_temp['Jains'] == df_temp['Jains']and df_temp['Others_Religions'] == df_temp['Others_Religions']:
         df_temp['Muslims'] =  df_temp['Population'] -df_temp['Religion_Not_Stated'] - df_temp['Hindus'] - df_temp['Christians'] - df_temp['Sikhs'] - df_temp['Buddhists'] - df_temp['Jains'] - df_temp['Others_Religions']
    elif df_temp['Hindus'] == df_temp['Hindus']and df_temp['Muslims'] == df_temp['Muslims']and df_temp['Religion_Not_Stated'] == df_temp['Religion_Not_Stated'] and df_temp['Sikhs'] == df_temp['Sikhs'] and df_temp['Buddhists'] == df_temp['Buddhists'] and df_temp['Jains'] == df_temp['Jains']and df_temp['Others_Religions'] == df_temp['Others_Religions']:
         df_temp['Christians'] =  df_temp['Population'] -df_temp['Hindus'] - df_temp['Muslims'] - df_temp['Religion_Not_Stated'] - df_temp['Sikhs'] - df_temp['Buddhists'] - df_temp['Jains'] - df_temp['Others_Religions']
    elif df_temp['Hindus'] == df_temp['Hindus']and df_temp['Muslims'] == df_temp['Muslims']and df_temp['Christians'] == df_temp['Christians'] and df_temp['Religion_Not_Stated'] == df_temp['Religion_Not_Stated'] and df_temp['Buddhists'] == df_temp['Buddhists'] and df_temp['Jains'] == df_temp['Jains']and df_temp['Others_Religions'] == df_temp['Others_Religions']:
         df_temp['Sikhs'] =  df_temp['Population'] -df_temp['Religion_Not_Stated'] - df_temp['Muslims'] - df_temp['Christians'] - df_temp['Hindus'] - df_temp['Buddhists'] - df_temp['Jains'] - df_temp['Others_Religions']
    elif df_temp['Hindus'] == df_temp['Hindus']and df_temp['Muslims'] == df_temp['Muslims']and df_temp['Christians'] == df_temp['Christians'] and df_temp['Sikhs'] == df_temp['Sikhs'] and df_temp['Religion_Not_Stated'] == df_temp['Religion_Not_Stated'] and df_temp['Jains'] == df_temp['Jains']and df_temp['Others_Religions'] == df_temp['Others_Religions']:
         df_temp['Buddhists'] =  df_temp['Population'] -df_temp['Religion_Not_Stated'] - df_temp['Muslims'] - df_temp['Christians'] - df_temp['Sikhs'] - df_temp['Hindus'] - df_temp['Jains'] - df_temp['Others_Religions']
    elif df_temp['Hindus'] == df_temp['Hindus']and df_temp['Muslims'] == df_temp['Muslims']and df_temp['Christians'] == df_temp['Christians'] and df_temp['Sikhs'] == df_temp['Sikhs'] and df_temp['Buddhists'] == df_temp['Buddhists'] and df_temp['Religion_Not_Stated'] == df_temp['Religion_Not_Stated']and df_temp['Others_Religions'] == df_temp['Others_Religions']:
         df_temp['Jains'] =  df_temp['Population'] -df_temp['Religion_Not_Stated'] - df_temp['Muslims'] - df_temp['Christians'] - df_temp['Sikhs'] - df_temp['Buddhists'] - df_temp['Hindus'] - df_temp['Others_Religions']
    elif df_temp['Hindus'] == df_temp['Hindus']and df_temp['Muslims'] == df_temp['Muslims']and df_temp['Christians'] == df_temp['Christians'] and df_temp['Sikhs'] == df_temp['Sikhs'] and df_temp['Buddhists'] == df_temp['Buddhists'] and df_temp['Jains'] == df_temp['Jains']and df_temp['Religion_Not_Stated'] == df_temp['Religion_Not_Stated']:
         df_temp['Others_Religions'] =  df_temp['Population'] -df_temp['Hindus'] - df_temp['Muslims'] - df_temp['Christians'] - df_temp['Sikhs'] - df_temp['Buddhists'] - df_temp['Jains'] - df_temp['Religion_Not_Stated']

    if df_temp['Households_with_Telephone_Mobile_Phone'] != df_temp['Households_with_Telephone_Mobile_Phone'] :
        if df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] == df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] and df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] == df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] and df_temp['Households_with_Telephone_Mobile_Phone_Both'] == df_temp['Households_with_Telephone_Mobile_Phone_Both']:
            df_temp['Households_with_Telephone_Mobile_Phone'] = df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] + df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] + df_temp['Households_with_Telephone_Mobile_Phone_Both']
    
    if df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] != df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] :
         if df_temp['Households_with_Telephone_Mobile_Phone'] == df_temp['Households_with_Telephone_Mobile_Phone'] and df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] == df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] and df_temp['Households_with_Telephone_Mobile_Phone_Both'] == df_temp['Households_with_Telephone_Mobile_Phone_Both']:
            df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] = df_temp['Households_with_Telephone_Mobile_Phone'] - df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] -df_temp['Households_with_Telephone_Mobile_Phone_Both']
    elif df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] != df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] :
         if df_temp['Households_with_Telephone_Mobile_Phone'] == df_temp['Households_with_Telephone_Mobile_Phone'] and df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] == df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] and df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] == df_temp['Households_with_Telephone_Mobile_Phone_Landline_only']:
            df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] = df_temp['Households_with_Telephone_Mobile_Phone'] - df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] -df_temp['Households_with_Telephone_Mobile_Phone_Both']
    elif df_temp['Households_with_Telephone_Mobile_Phone_Both'] != df_temp['Households_with_Telephone_Mobile_Phone_Both'] :
         if df_temp['Households_with_Telephone_Mobile_Phone'] == df_temp['Households_with_Telephone_Mobile_Phone'] and df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] == df_temp['Households_with_Telephone_Mobile_Phone_Mobile_only'] and df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] == df_temp['Households_with_Telephone_Mobile_Phone_Landline_only']:
            df_temp['Households_with_Telephone_Mobile_Phone_Both'] = df_temp['Households_with_Telephone_Mobile_Phone'] - df_temp['Households_with_Telephone_Mobile_Phone_Landline_only'] -df_temp['Households_with_Telephone_Mobile_Phone_Landline_only']
    
    if df_temp['Total_Education'] != df_temp['Total_Education'] and df_temp['Illiterate_Education'] == df_temp['Illiterate_Education']and df_temp['Literate_Education'] == df_temp['Literate_Education']:
        df_temp['Total_Education'] = df_temp['Literate_Education'] + df_temp['Illiterate_Education']
    elif df_temp['Illiterate_Education'] != df_temp['Illiterate_Education'] and df_temp['Total_Education'] == df_temp['Total_Education']and df_temp['Literate_Education'] == df_temp['Literate_Education']:
        df_temp['Illiterate_Education'] = df_temp['Total_Education'] - df_temp['Literate_Education'] 
    elif df_temp['Literate_Education'] != df_temp['Literate_Education'] and df_temp['Total_Education'] == df_temp['Total_Education']and df_temp['Illiterate_Education'] == df_temp['Illiterate_Education']:
            df_temp['Literate_Education'] = df_temp['Total_Education'] - df_temp['Illiterate_Education'] 


    return df_temp


df_temp = df_temp.apply(fill_missing_values, axis=1)
print(df_temp.isnull().sum(axis=0))
#df_temp.to_csv("new.csv")