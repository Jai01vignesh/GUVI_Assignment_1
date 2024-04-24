# importing dependencies
import pandas as pd
import docx2txt
from pymongo import MongoClient
from sqlalchemy import create_engine
import streamlit as st
import plotly.express as px

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


df_temp = pd.read_excel("census_2011.xlsx")
#print(df_temp.head())


#Task 1: Rename the Column names - using rename function
renamed_col_dict ={
                   'District code':'District_code',
                   'State name': 'State/UT',
                   'District name': 'District',
                   'Male_Literate': 'Literate_Male',
                   'Female_Literate': 'Literate_Female',
                   'Rural_Households': 'Households_Rural',
                   'Urban_Households': 'Households_Urban',
                   'Age_Group_0_29': 'Young_and_Adult',
                   'Age_Group_30_49': 'Middle_Aged',
                   'Age_Group_50': 'Senior_Citizen',
                   'Age not stated': 'Age_Not_Stated',
                   'Married_couples_5__Households':'Married_couples_5_Households'
                   }
df_temp.rename(columns =renamed_col_dict,inplace=True)



#Task 2: Task 2: Rename State/UT Names
def rename_col(name):
    name_lst = name.split()
    cnvrtd_name_lst = []
    for nme in name_lst:
        if nme  == "AND":
            cnvrtd_name_lst.append(nme.lower())
        else:
            cnvrtd_name_lst.append(nme.capitalize())
    return(" ".join(cnvrtd_name_lst))


df_temp["State/UT"] = df_temp["State/UT"].apply(rename_col)
df_temp["District"] = df_temp["District"].apply(rename_col)


#Task 3: New State/UT formation

my_text = docx2txt.process("Telangana.docx")

lst =df_temp["District name"][df_temp["District name"].duplicated() == True].to_list()

def rename_state(df_temp):
    for nme in my_text.split():
        df_temp.loc[df_temp['District'] == nme, 'State/UT'] ="Telangana"
    df_temp.loc[df_temp['District'].isin (['Leh(Ladakh)','Kargil']), 'State/UT'] ="Ladakh"

def rename_duplicated_districts(df_temp):
    for nme in lst:
        df_temp.loc[df_temp['District name'] == nme, 'District name'] = nme + " ("+ df_temp.loc[df_temp['District name'] == nme]['State name']  +")"

rename_state(df_temp)
rename_duplicated_districts(df_temp)


#Task 4: Find and process Missing Data
print(df_temp.isnull().sum(axis=0).sum())

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

    
    if df_temp['Households'] != df_temp['Households'] :
        if df_temp['Households_Rural'] == df_temp['Households_Rural'] and df_temp['Households_Urban'] == df_temp['Households_Urban'] :
            df_temp['Households'] = df_temp['Households_Rural'] + df_temp['Households_Urban'] 
    elif df_temp['Households_Rural'] != df_temp['Households_Rural'] and df_temp['Households_Urban'] == df_temp['Households_Urban'] and df_temp['Households'] == df_temp['Households'] :
            df_temp['Households_Rural'] = df_temp['Households'] - df_temp['Households_Urban']
    elif df_temp['Households_Urban'] != df_temp['Households_Urban'] and df_temp['Households_Rural'] == df_temp['Households_Rural'] and df_temp['Households'] == df_temp['Households'] :
            df_temp['Households_Urban'] = df_temp['Households'] - df_temp['Households_Rural']
    
    
    
    if df_temp['Total_Education'] != df_temp['Total_Education'] and df_temp['Illiterate_Education'] == df_temp['Illiterate_Education']and df_temp['Literate_Education'] == df_temp['Literate_Education']:
        df_temp['Total_Education'] = df_temp['Literate_Education'] + df_temp['Illiterate_Education']
    elif df_temp['Illiterate_Education'] != df_temp['Illiterate_Education'] and df_temp['Total_Education'] == df_temp['Total_Education']and df_temp['Literate_Education'] == df_temp['Literate_Education']:
        df_temp['Illiterate_Education'] = df_temp['Total_Education'] - df_temp['Literate_Education'] 
    elif df_temp['Literate_Education'] != df_temp['Literate_Education'] and df_temp['Total_Education'] == df_temp['Total_Education']and df_temp['Illiterate_Education'] == df_temp['Illiterate_Education']:
            df_temp['Literate_Education'] = df_temp['Total_Education'] - df_temp['Illiterate_Education'] 


    if df_temp['Young_and_Adult'] != df_temp['Young_and_Adult'] and  df_temp['Population'] == df_temp['Population'] and df_temp['Middle_Aged'] == df_temp['Middle_Aged'] and df_temp['Senior_Citizen'] == df_temp['Senior_Citizen']and df_temp['Age_Not_Stated'] == df_temp['Age_Not_Stated']:
        df_temp['Young_and_Adult'] = df_temp['Population'] - df_temp['Middle_Aged']- df_temp['Senior_Citizen']- df_temp['Age_Not_Stated']
    elif df_temp['Senior_Citizen'] != df_temp['Senior_Citizen'] and  df_temp['Population'] == df_temp['Population'] and df_temp['Middle_Aged'] == df_temp['Middle_Aged'] and df_temp['Young_and_Adult'] == df_temp['Young_and_Adult']and df_temp['Age_Not_Stated'] == df_temp['Age_Not_Stated']:
         df_temp['Senior_Citizen'] = df_temp['Population'] - df_temp['Middle_Aged']- df_temp['Young_and_Adult']- df_temp['Age_Not_Stated']
    elif df_temp['Middle_Aged'] != df_temp['Middle_Aged'] and  df_temp['Population'] == df_temp['Population'] and df_temp['Young_and_Adult'] == df_temp['Young_and_Adult'] and df_temp['Senior_Citizen'] == df_temp['Senior_Citizen']and df_temp['Age_Not_Stated'] == df_temp['Age_Not_Stated']:
             df_temp['Middle_Aged'] = df_temp['Population'] - df_temp['Young_and_Adult']- df_temp['Senior_Citizen']- df_temp['Age_Not_Stated']
    elif df_temp['Age_Not_Stated'] != df_temp['Age_Not_Stated'] and  df_temp['Population'] == df_temp['Population'] and df_temp['Young_and_Adult'] == df_temp['Young_and_Adult'] and df_temp['Senior_Citizen'] == df_temp['Senior_Citizen']and df_temp['Middle_Aged'] == df_temp['Middle_Aged']:
             df_temp['Age_Not_Stated'] = df_temp['Population'] - df_temp['Young_and_Adult']- df_temp['Senior_Citizen']- df_temp['Middle_Aged']


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
    

    if df_temp['Household_size_1_to_2_persons'] != df_temp['Household_size_1_to_2_persons'] and df_temp['Household_size_2_persons_Households'] == df_temp['Household_size_2_persons_Households'] and df_temp['Household_size_1_person_Households'] == df_temp['Household_size_1_person_Households'] :
            df_temp['Household_size_1_to_2_persons'] = df_temp['Household_size_1_person_Households'] + df_temp['Household_size_2_persons_Households']
    elif df_temp['Household_size_1_person_Households'] != df_temp['Household_size_1_person_Households'] and df_temp['Household_size_2_persons_Households'] == df_temp['Household_size_2_persons_Households'] :
            df_temp['Household_size_1_person_Households'] = df_temp['Household_size_1_to_2_persons'] - df_temp['Household_size_2_persons_Households']
    elif df_temp['Household_size_2_persons_Households'] != df_temp['Household_size_2_persons_Households'] and df_temp['Household_size_1_person_Households'] == df_temp['Household_size_1_person_Households'] :
            df_temp['Household_size_2_persons_Households'] = df_temp['Household_size_1_to_2_persons'] - df_temp['Household_size_1_person_Households']

    if df_temp['Household_size_3_to_5_persons_Households'] != df_temp['Household_size_3_to_5_persons_Households'] :
           df_temp['Household_size_3_to_5_persons_Households'] = df_temp['Household_size_3_persons_Households'] + df_temp['Household_size_4_persons_Households'] + df_temp['Household_size_5_persons_Households']
    elif df_temp['Household_size_3_persons_Households'] != df_temp['Household_size_3_persons_Households'] and df_temp['Household_size_3_to_5_persons_Households'] == df_temp['Household_size_3_to_5_persons_Households'] and df_temp['Household_size_4_persons_Households'] == df_temp['Household_size_4_persons_Households'] and df_temp['Household_size_5_persons_Households'] == df_temp['Household_size_5_persons_Households']:
            df_temp['Household_size_3_persons_Households'] = df_temp['Household_size_3_to_5_persons_Households'] - df_temp['Household_size_4_persons_Households'] - df_temp['Household_size_5_persons_Households']
    elif df_temp['Household_size_4_persons_Households'] != df_temp['Household_size_4_persons_Households'] and df_temp['Household_size_3_to_5_persons_Households'] == df_temp['Household_size_3_to_5_persons_Households'] and df_temp['Household_size_3_persons_Households'] == df_temp['Household_size_3_persons_Households'] and df_temp['Household_size_5_persons_Households'] == df_temp['Household_size_5_persons_Households'] :
            df_temp['Household_size_4_persons_Households'] = df_temp['Household_size_3_to_5_persons_Households'] - df_temp['Household_size_3_persons_Households'] - df_temp['Household_size_5_persons_Households']
    elif df_temp['Household_size_5_persons_Households'] != df_temp['Household_size_5_persons_Households'] and df_temp['Household_size_3_to_5_persons_Households'] == df_temp['Household_size_3_to_5_persons_Households'] and df_temp['Household_size_3_persons_Households'] == df_temp['Household_size_3_persons_Households'] and df_temp['Household_size_4_persons_Households'] == df_temp['Household_size_4_persons_Households'] :
            df_temp['Household_size_5_persons_Households'] = df_temp['Household_size_3_to_5_persons_Households'] - df_temp['Household_size_3_persons_Households'] - df_temp['Household_size_4_persons_Households']
    

    if df_temp['Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households'] != df_temp['Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households']and df_temp['Main_source_of_drinking_water_Spring_Households'] == df_temp['Main_source_of_drinking_water_Spring_Households'] and df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] == df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] and df_temp['Main_source_of_drinking_water_River_Canal_Households'] == df_temp['Main_source_of_drinking_water_River_Canal_Households'] and df_temp['Main_source_of_drinking_water_Other_sources_Households'] == df_temp['Main_source_of_drinking_water_Other_sources_Households']:
        df_temp['Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households'] = df_temp['Main_source_of_drinking_water_Other_sources_Households'] + df_temp['Main_source_of_drinking_water_Spring_Households'] + df_temp['Main_source_of_drinking_water_River_Canal_Households'] + df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households']
    elif df_temp['Main_source_of_drinking_water_Spring_Households'] != df_temp['Main_source_of_drinking_water_Spring_Households'] and df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] == df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] and df_temp['Main_source_of_drinking_water_River_Canal_Households'] == df_temp['Main_source_of_drinking_water_River_Canal_Households'] and df_temp['Main_source_of_drinking_water_Other_sources_Households'] == df_temp['Main_source_of_drinking_water_Other_sources_Households']:
        df_temp['Main_source_of_drinking_water_Spring_Households'] = df_temp['Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households'] - df_temp['Main_source_of_drinking_water_Other_sources_Households'] - df_temp['Main_source_of_drinking_water_River_Canal_Households'] - df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households']
    elif df_temp['Main_source_of_drinking_water_River_Canal_Households'] != df_temp['Main_source_of_drinking_water_River_Canal_Households'] and df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] == df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] and df_temp['Main_source_of_drinking_water_Spring_Households'] == df_temp['Main_source_of_drinking_water_Spring_Households'] and df_temp['Main_source_of_drinking_water_Other_sources_Households'] == df_temp['Main_source_of_drinking_water_Other_sources_Households']:
        df_temp['Main_source_of_drinking_water_River_Canal_Households'] = df_temp['Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households'] - df_temp['Main_source_of_drinking_water_Other_sources_Households'] - df_temp['Main_source_of_drinking_water_Spring_Households'] - df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households']
    elif df_temp['Main_source_of_drinking_water_Other_sources_Households'] != df_temp['Main_source_of_drinking_water_Other_sources_Households'] and df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] == df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] and df_temp['Main_source_of_drinking_water_River_Canal_Households'] == df_temp['Main_source_of_drinking_water_River_Canal_Households'] and df_temp['Main_source_of_drinking_water_Spring_Households'] == df_temp['Main_source_of_drinking_water_Spring_Households']:
        df_temp['Main_source_of_drinking_water_Other_sources_Households'] = df_temp['Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households'] - df_temp['Main_source_of_drinking_water_Spring_Households'] - df_temp['Main_source_of_drinking_water_River_Canal_Households'] - df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households']
    elif df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] != df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] and df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] == df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] and df_temp['Main_source_of_drinking_water_Other_sources_Households'] == df_temp['Main_source_of_drinking_water_Other_sources_Households'] and df_temp['Main_source_of_drinking_water_Spring_Households'] == df_temp['Main_source_of_drinking_water_Spring_Households']:
        df_temp['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] = df_temp['Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households'] - df_temp['Main_source_of_drinking_water_Spring_Households'] - df_temp['Main_source_of_drinking_water_River_Canal_Households'] - df_temp['Main_source_of_drinking_water_Other_sources_Households']




    if df_temp['Married_couples_3_or_more_Households'] != df_temp['Married_couples_3_or_more_Households'] :
        df_temp['Married_couples_3_or_more_Households'] = df_temp['Married_couples_3_Households'] + df_temp['Married_couples_4_Households'] + df_temp['Married_couples_5_Households']
    elif df_temp['Married_couples_3_Households'] != df_temp['Married_couples_3_Households'] and df_temp['Married_couples_4_Households'] == df_temp['Married_couples_4_Households'] and df_temp['Married_couples_5_Households'] == df_temp['Married_couples_5_Households']:
        df_temp['Married_couples_3_Households'] = df_temp['Married_couples_3_or_more_Households'] - df_temp['Married_couples_4_Households'] - df_temp['Married_couples_5_Households']
    elif df_temp['Married_couples_4_Households'] != df_temp['Married_couples_3_Households'] and df_temp['Married_couples_3_Households'] == df_temp['Married_couples_3_Households'] and df_temp['Married_couples_5_Households'] == df_temp['Married_couples_5_Households']:
        df_temp['Married_couples_4_Households'] = df_temp['Married_couples_3_or_more_Households'] - df_temp['Married_couples_3_Households'] - df_temp['Married_couples_5_Households']
    elif df_temp['Married_couples_5_Households'] != df_temp['Married_couples_3_Households'] and df_temp['Married_couples_3_Households'] == df_temp['Married_couples_3_Households'] and df_temp['Married_couples_4_Households'] == df_temp['Married_couples_4_Households']:
        df_temp['Married_couples_5_Households'] = df_temp['Married_couples_3_or_more_Households'] - df_temp['Married_couples_3_Households'] - df_temp['Married_couples_4_Households']
    

    return df_temp

print(df_temp.isnull().sum(axis=0).sum()) 
df_temp = df_temp.apply(fill_missing_values, axis=1) #imputing empty values  with 0
df_temp.fillna(0, inplace =True)

#Task-5 Save Data to MongoDB
df_dict =df_temp.to_dict('records')

#Mongo db connection
Connection_string = MongoClient("mongodb+srv://jaivigneshpris:x1!zh5>Qhc4NXd{t@census2011.uu8axpz.mongodb.net/?retryWrites=true&w=majority&appName=census2011")

try:
    Connection_string.admin.command('ping')
    db = Connection_string.guvi_census_data
    clctn = db.census
    clctn.insert_many(df_dict) #pushing dictionary data into the census  collection
except Exception as e:
    print(e)


#Task 6: Database connection and data upload

#Getting records from mongo db and parsing them to postgresql engine by appending in a list
lst =[]
for i in clctn.find((),{"_id":0}):
     lst.append(i)

df_mongo = pd.DataFrame(lst) #converting the appended list to a dataframe

connection = create_engine("postgresql://postgres:qweaszx@localhost:5432/guvi_practice") #Postgresql connection - dbname://userid:password@hostname:portnumber/databasename
df_mongo.to_sql("census", con = connection, if_exists='replace',
                index = False,dtype={'District_code': 'INTEGER PRIMARY KEY'}) # pushing data from mongo dataframe to postgree table census , rows will be replaced if the table already exists
 

#Task 7: Run Query on the database and show output on streamlit
st.set_page_config(page_title="Census-2011 Dashboard", page_icon="Active",layout = "wide" ) #setting the pagetitle and layout to be wide

#Getting State names and District names for filtering data for some metrics
State_filter = st.sidebar.selectbox("Select the State/UT",
                                    pd.read_sql('select distinct "State/UT" from census order by "State/UT";'
                                                ,connection))
District_filter = st.sidebar.selectbox("Select the District",
                                       pd.read_sql('select distinct "District" from census where "State/UT" = %(name)s order by "District"'
                                                   ,connection,params={'name' :State_filter }))

def plot(SQL_Query,Sub_header,X,Y):
    st.subheader(Sub_header)
    fig = px.bar(SQL_Query, x = X, y = Y, text = ['{:,.2f}'.format(x) for x in SQL_Query[Y]],
                template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

def plot_scatter(SQL_Query,Sub_header,X,Y,X_name,Y_name):
    st.subheader(Sub_header)
    fig = px.scatter(SQL_Query, x = X, y = Y,
      template = "seaborn",labels={"value": X_name, "variable": Y_name})
    st.plotly_chart(fig,use_container_width=True, height = 200)

def select_box(Y_axis,col):
    if Y_axis == "All":
         y_ax = col
    else:
        y_ax = Y_axis
    return  y_ax

def area_box (SQL_Query,Sub_header,X,Y):
    st.subheader(Sub_header)
    fig = px.area(SQL_Query, x=X, y=Y, color="State/UT")
    st.plotly_chart(fig,use_container_width=True, height = 200)

def plot1(SQL_Query,Sub_header,X,Y):
    st.subheader(Sub_header)
    fig = px.bar(SQL_Query, x=X, y=Y, title="Long-Form Input")
    st.plotly_chart(fig,use_container_width=True, height = 200)

def chart(SQL_Query,Sub_header,X,Y):
    st.subheader(Sub_header)
    fig = px.pie(SQL_Query, values=X, names=Y, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig,use_container_width=True, height = 200)


col1,col2,col3,col4,col5,col6 = st.columns(6)  #Splitting columns into 6 to display multiple metric values like Population , Male, Female etc

#What is the total population of each district?
SQL_Query1 = pd.read_sql('select sum("Population") as "Population"  from census where "State/UT" = %(name)s group by "State/UT" ', 
                         connection,params={'name' :State_filter })

#How many literate males and females are there in each district?
SQL_Query2 = pd.read_sql('select "Population"  from census where "District" = %(name)s and "State/UT" = %(state_name)s', 
                         connection, params = {'name' :District_filter , 'state_name': State_filter })

SQL_Query3 = pd.read_sql('select "Literate_Male"  from census where "District" = %(name)s and "State/UT" = %(state_name)s', 
                         connection, params = {'name' :District_filter , 'state_name': State_filter })

SQL_Query4 = pd.read_sql('select "Literate_Female"  from census where "District" = %(name)s and "State/UT" = %(state_name)s', 
                         connection, params = {'name' :District_filter , 'state_name': State_filter })

SQL_Query_male_percent = pd.read_sql('select ("Male_Workers"/"Workers")*100 as "Male Worker"   from census where "District" = %(name)s and "State/UT" = %(state_name)s', 
                                     connection, params = {'name' :District_filter , 'state_name': State_filter })

SQL_Query_female_percent = pd.read_sql('select ("Female_Workers"/"Workers")*100 as "Female Worker"  from census where "District" = %(name)s and "State/UT" = %(state_name)s', 
                                       connection, params = {'name' :District_filter , 'state_name': State_filter })

SQL_Query5 = pd.read_sql('select "District","Literate_Male"  from census order by "Literate_Male" desc', 
                         connection)
SQL_Query6 = pd.read_sql('select "District","Literate_Female"  from census order by "Literate_Female" desc', 
                         connection)


#What is the percentage of workers (both male and female) in each district?
SQL_Query7 = pd.read_sql('select "District",("Male_Workers"/"Workers")*100 as "Male Worker",("Female_Workers"/"Workers")*100 as "Female Worker" from census order by "District";', 
                         connection)

#How many households have access to LPG or PNG as a cooking fuel in each district?
SQL_Query8 = pd.read_sql('select "District","LPG_or_PNG_Households" from census order by "LPG_or_PNG_Households" desc;', 
                         connection)

#What is the religious composition (Hindus, Muslims, Christians, etc.) of each district?
SQL_Query9 = pd.read_sql('select "District", "Hindus","Muslims","Christians","Sikhs","Buddhists","Jains","Others_Religions","Religion_Not_Stated" from census', 
                         connection)

#How many households have internet access in each district?
SQL_Query10 = pd.read_sql('select "District","Households_with_Internet" from census order by "Households_with_Internet" desc;', 
                          connection)

#What is the educational attainment distribution (below primary, primary,middle, secondary, etc.) in each district?
SQL_Query11 = pd.read_sql('select "District","Below_Primary_Education","Primary_Education","Middle_Education","Secondary_Education","Higher_Education","Graduate_Education","Other_Education" from census;', 
                          connection)

#How is the household size distributed (1 person, 2 persons, 3-5 persons, etc.) in each district?
SQL_Query12 = pd.read_sql('select "District", ("Household_size_1_person_Households") as "1-Person", ("Household_size_2_persons_Households") as "2-Persons", ("Household_size_3_persons_Households") as "3-Persons", ("Household_size_4_persons_Households") as "4-Persons", ("Household_size_5_persons_Households") as "5-Persons", ("Household_size_6_8_persons_Households") as "6to8-Persons", ("Household_size_9_persons_and_above_Households") as "9 and more Persons" from census;', 
                          connection)

#What is the total number of households in each state?
SQL_Query13 = pd.read_sql('select "State/UT", sum("Households")as "Total Households" from census group by "State/UT" order by "Total Households" desc;', 
                          connection)

#How many households have a latrine facility within the premises in each state?
SQL_Query14 = pd.read_sql('select "State/UT", sum("Having_latrine_facility_within_the_premises_Total_Households") as "On Premisis Laterine" from census group by "State/UT" order by "On Premisis Laterine" desc;', 
                          connection)

#What is the average household size in each state?
SQL_Query15 = pd.read_sql('select "State/UT", Avg("Household_size_1_person_Households") as "1-Person", Avg("Household_size_2_persons_Households") as "2-Persons", Avg("Household_size_3_persons_Households") as "3-Persons", Avg("Household_size_4_persons_Households") as "4-Persons", Avg("Household_size_5_persons_Households") as "5-Persons", Avg("Household_size_6_8_persons_Households") as "6to8-Persons", Avg("Household_size_9_persons_and_above_Households") as "9 and more Persons" from census group by "State/UT";', 
                          connection)

#How many households are owned versus rented in each state?
SQL_Query16 = pd.read_sql('select "State/UT", sum("Ownership_Owned_Households"/("Ownership_Owned_Households"+"Ownership_Rented_Households")) as "Owned",sum("Ownership_Rented_Households"/("Ownership_Owned_Households"+"Ownership_Rented_Households")) as "Rented" from census group by "State/UT";', 
                          connection)

#What is the distribution of different types of latrine facilities (pit latrine, flush latrine, etc.) in each state?
SQL_Query17 = pd.read_sql('select "State/UT", sum("Type_of_latrine_facility_Pit_latrine_Households") as "Pit Laterine",sum("Type_of_latrine_facility_Other_latrine_Households") as "Other Laterine",sum("Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Ho") as "Night Soil",sum("Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_")as"Flush" from census group by "State/UT";', 
                          connection)

#How many households have access to drinking water sources near the premises in each state?
SQL_Query18 = pd.read_sql('select "State/UT", sum("Location_of_drinking_water_source_Near_the_premises_Households") as "Households" from census group by "State/UT" order by "Households" desc;', 
                          connection)

#What is the average household income distribution in each state based on the power parity categories?
SQL_Query19 = pd.read_sql('select "State/UT", avg("Power_Parity_Less_than_Rs_45000") as "income < 45000", avg("Power_Parity_Rs_45000_150000") as "income between 45000 to 150000", avg("Power_Parity_Rs_150000_330000") as "income between 150000 to 330000", avg("Power_Parity_Rs_330000_545000") as "income between 330000 to 545000", avg("Power_Parity_Above_Rs_545000") as "income > 545000" from census group by "State/UT";', 
                          connection)

#What is the percentage of married couples with different household sizes in each state?
SQL_Query20 = pd.read_sql('select "State/UT", (sum("Married_couples_1_Households")/sum("Married_couples_None_Households" +"Married_couples_1_Households"+"Married_couples_2_Households"+"Married_couples_3_or_more_Households"))*100 as "1"  ,(sum("Married_couples_2_Households")/sum("Married_couples_None_Households" +"Married_couples_1_Households"+"Married_couples_2_Households"+"Married_couples_3_or_more_Households"))*100 as"2" ,(sum("Married_couples_3_or_more_Households")/sum("Married_couples_None_Households" +"Married_couples_1_Households"+"Married_couples_2_Households"+"Married_couples_3_or_more_Households"))*100 as "3" from census group by "State/UT";', 
                          connection)

#How many households fall below the poverty line in each state based on the power parity categories?
SQL_Query21 = pd.read_sql('select "State/UT",sum("Power_Parity_Less_than_Rs_45000") as "Households"  from census group by("State/UT") order by "Households";', 
                          connection)

#What is the overall literacy rate (percentage of literate population) in each state?
SQL_Query22 = pd.read_sql('select "State/UT",sum("Literate")/sum("Population") as "Literacy Rate"  from census group by "State/UT" order by "Literacy Rate";', 
                          connection)

#How many households have access to various modes of transportation (bicycle, car, radio, television, etc.) in each district?
SQL_Query23 = pd.read_sql('select "District","Households_with_Bicycle","Households_with_Car_Jeep_Van","Households_with_Scooter_Motorcycle_Moped" from census;',
                          connection)

#What is the condition of occupied census houses (dilapidated, with separate kitchen, with bathing facility, with latrine facility, etc.) in each district?
SQL_Query24 = pd.read_sql('select "District","Condition_of_occupied_census_houses_Dilapidated_Households" as "Dilapidated","Households_with_separate_kitchen_Cooking_inside_house" as "Seperate Kitchen","Having_bathing_facility_Total_Households" as "Bathing Facility","Having_latrine_facility_within_the_premises_Total_Households" as "Laterine_within_premisis","Not_having_latrine_facility_within_the_premises_Alternative_sou"as "Laterine_outside_premisis_Alternate_sources" from census;',
                          connection)


with col1:
    st.metric(label = "Population", value = SQL_Query1.values)

with col2:
    st.metric(label= "District-wise Population", value = SQL_Query2.values)

with col3:
    st.metric(label = "Literate Male", value = SQL_Query3.values)
st.subheader("Literate Male per District")
fig = px.bar(SQL_Query5, x = "District", y = "Literate_Male", 
             text = ['{:,.2f}'.format(x) for x in SQL_Query5["Literate_Male"]],
             template = "seaborn")
st.plotly_chart(fig,use_container_width=True, height = 200)

with col4:
    st.metric(label= "Literate Female", value = SQL_Query4.values)
st.subheader("Literate Female per District")
fig = px.bar(SQL_Query6, x = "District", y = "Literate_Female", 
             text = ['{:,.2f}'.format(x) for x in SQL_Query6["Literate_Female"]],
             template = "seaborn")
st.plotly_chart(fig,use_container_width=True, height = 200)


with col5:
    st.metric(label= "Male Workers %", value = SQL_Query_male_percent.values)


with col6:
    #st.metric(label= "Female Workers %", value = SQL_Query_female_percent.values)
    st.metric(label= "Female Workers %", value = ['{:,.2f}'.format(x) for x in SQL_Query_female_percent.values])


#Function call to plot Bar, Scatter plots etc
 #plot - Query, Sub Header, X column, Y column
 #plot_scatter -  Query, Sub Header, X column, Y column list, Y column heading, Legend name
 #selectbox - Select box values, Y axis columns
 #chart - Query, Sub header, X column, Y column


plot(SQL_Query7,"Male Workers per District","District","Male Worker")   
plot(SQL_Query7,"Female Workers per District","District","Female Worker") 
plot(SQL_Query8,"LPG/PNG as Cooking Fuel","District","LPG_or_PNG_Households")
Y_axis=st.selectbox("Religion",["All","Hindus","Muslims","Christians","Sikhs","Buddhists","Jains","Others_Religions","Religion_Not_Stated"],
                    index = 0)
y_ax = select_box(Y_axis, ["Hindus","Muslims","Christians","Sikhs","Buddhists","Jains","Others_Religions","Religion_Not_Stated"])
plot_scatter(SQL_Query9,"District wise Religion spread","District",y_ax,"Religion",
             "Religion")
plot(SQL_Query10,"Households with Internet","District","Households_with_Internet")
Y_axis=st.selectbox("Education",["All","Below_Primary_Education","Primary_Education","Middle_Education","Secondary_Education","Higher_Education","Graduate_Education","Other_Education"],index = 0)
y_ax1 = select_box(Y_axis, ["Below_Primary_Education","Primary_Education","Middle_Education","Secondary_Education","Higher_Education","Graduate_Education","Other_Education"])
plot_scatter(SQL_Query11,"District wise Education spread","District",y_ax1,
             "Education","Education")
Y_axis1=st.selectbox("Household-Size",["All","1-Person","2-Persons","3-Persons","4-Persons","5-Persons","6to8-Persons","9 and more Persons"],
                     index = 0)
y_ax2 = select_box(Y_axis1, ["1-Person","2-Persons","3-Persons","4-Persons","5-Persons","6to8-Persons","9 and more Persons"])
plot_scatter(SQL_Query12,"District wise Household size spread","District",y_ax2,
             "Households","Households")
plot(SQL_Query13,"No. Of Households in each State/UT","State/UT","Total Households")
plot(SQL_Query14,"No. Of On Premisis Laterine Facility in each State/UT","State/UT","On Premisis Laterine")
Y_axis2=st.selectbox("Average Household Size",["All","1-Person","2-Persons","3-Persons","4-Persons","5-Persons","6to8-Persons","9 and more Persons"],
                     index = 0)
y_ax3 = select_box(Y_axis2, ["1-Person","2-Persons","3-Persons","4-Persons","5-Persons","6to8-Persons","9 and more Persons"])
plot_scatter(SQL_Query15,"Average Household Size in each State/UT","State/UT",y_ax3,
             "Household size","Household size")
#area_box(SQL_Query16,"State-wise Owned Houses vs Rented Houses","Owned","Rented")
plot1(SQL_Query16,"State-wise Owned Houses vs Rented Houses","State/UT",["Owned","Rented"])
Y_axis3=st.selectbox("Different Type of Laterines",["All","Pit Laterine","Other Laterine","Night Soil","Flush"],
                     index = 0)
y_ax4 = select_box(Y_axis3, ["Pit Laterine","Other Laterine","Night Soil","Flush"])
plot_scatter(SQL_Query17,"Different Type of Laterines in each State/UT","State/UT",y_ax4,
             "Laterine Types","Laterine Types")
plot(SQL_Query18,"No. Of On households have access to drinking water sources near the premises in each State/UT","State/UT","Households")
Y_axis4=st.selectbox("Different Type of Laterines",["All","income < 45000","income between 45000 to 150000","income between 150000 to 330000","income between 330000 to 545000","income > 545000"],index = 0)
y_ax5 = select_box(Y_axis4, ["income < 45000","income between 45000 to 150000","income between 150000 to 330000","income between 330000 to 545000","income > 545000"])
plot_scatter(SQL_Query19,"Different Type of Laterines in each State/UT","State/UT",y_ax5,
             "Income Range","Income Range")
Y_axis5 =st.selectbox("'%' of Married couplese Households in each State/UT",["All","1","2","3"],
                      index = 0)
y_ax6 = select_box(Y_axis5, ["1","2","3"])
plot_scatter(SQL_Query20,"'%' of Married couplese Households in each State/UT","State/UT",y_ax6,"Households size of Maried coluples","Households size of Maried coluples")
plot(SQL_Query21,"No. Of Households in poverty line in each State/UT","State/UT","Households")
chart(SQL_Query22,"State/UT-wise Literacy rate %","Literacy Rate","State/UT")
Y_axis6 =st.selectbox("Transport distribution District-wise",["All","Households_with_Bicycle","Households_with_Car_Jeep_Van","Households_with_Scooter_Motorcycle_Moped"],
                      index = 0)
y_ax7 = select_box(Y_axis6, ["Households_with_Bicycle","Households_with_Car_Jeep_Van","Households_with_Scooter_Motorcycle_Moped"])
plot_scatter(SQL_Query23,"Transport distribution District-wise","District",y_ax7,
             "Transports","Transports")
Y_axis7 =st.selectbox("Condition of occupied census houses District-wise",["All","Dilapidated", "Seperate Kitchen","Bathing Facility", "Laterine_within_premisis","Laterine_outside_premisis_Alternate_sources"],
                      index = 0)
y_ax8 = select_box(Y_axis7, ["Dilapidated", "Seperate Kitchen","Bathing Facility","Laterine_within_premisis", "Laterine_outside_premisis_Alternate_sources"])
plot_scatter(SQL_Query24,"Transport distribution District-wisee","District",y_ax8,
             "Types of houses","Types of houses")