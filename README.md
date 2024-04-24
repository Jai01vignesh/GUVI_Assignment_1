# GUVI_Assignment_1
Census Data Standardization and Analysis Pipeline: From Cleaning to Visualization

Important files:
Python file with entire process along with streamlit code - Data_pipeline_cleaning.py
Presentation file - Census 2011.pptx



Dependencies installed: - pip install -r requirements.txt
pandas
doc2txt
openpyxl
pymongo
sqlalchemy
streamlit
plotly
psycopg2

Task 1: Rename the Column names
Below given columns were renamed:
⮚ State name to State/UT
⮚ District name to District
⮚ Male_Literate to Literate_Male
⮚ Female_Literate to Literate_Female
⮚ Rural_Households to Households_Rural
⮚ Urban_ Households to Households_Urban
⮚ Age_Group_0_29 to Young_and_Adult
⮚ Age_Group_30_49 to Middle_Aged
⮚ Age_Group_50 to Senior_Citizen
⮚ Age not stated to Age_Not_Stated

Task 2: Rename State/UT Names
All the state names are converted to camel case and "AND" is converted to small letter

Task 3: New State/UT formation
Distircts given in the Telanagana.docx were assigned to a new state Telangana.
Leh and kargil were assigned to a new UT Ladakh

Task 4: Find and process Missing Data
Majority of the missing Data in each column was filled based on the dependant columns and the remaining data which were not  interdependant were imputed to 0

Task 5: Save Data to MongoDB
Cleaned Data was Stored to MongoDB with collection name census. Used Pymongo dependency and connected to the Mongoclient

Task 6: Database connection and data upload
Relational Database used: POSTGRESQL
Columns which were of pandas object type were converted into Varchar(50) and int types were converted to Intgerr type.
Primary key was created for the column District_code
Connection to Postgresql Database was made using sqlalchemy which required pyscopy2 dependency.


Task 7: Run Query on the database and show output on streamlit
Each of the below 20 qns were answered using streamlit and plotly
1. What is the total population of each district?
2. How many literate males and females are there in each district?
3. What is the percentage of workers (both male and female) in each district?
4. How many households have access to LPG or PNG as a cooking fuel in each
district?
5. What is the religious composition (Hindus, Muslims, Christians, etc.) of each
district?
6. How many households have internet access in each district?
7. What is the educational attainment distribution (below primary, primary,
middle, secondary, etc.) in each district?
8. How many households have access to various modes of transportation
(bicycle, car, radio, television, etc.) in each district?
9. What is the condition of occupied census houses (dilapidated, with separate
kitchen, with bathing facility, with latrine facility, etc.) in each district?
10.How is the household size distributed (1 person, 2 persons, 3-5 persons, etc.)
in each district?
11. What is the total number of households in each state?
12.How many households have a latrine facility within the premises in each
state?
13.What is the average household size in each state?
14.How many households are owned versus rented in each state?
15.What is the distribution of different types of latrine facilities (pit latrine, flush
latrine, etc.) in each state?
16.How many households have access to drinking water sources near the
premises in each state?
17.What is the average household income distribution in each state based on the
power parity categories?
18.What is the percentage of married couples with different household sizes in
each state?
19.How many households fall below the poverty line in each state based on the
power parity categories?
20.What is the overall literacy rate (percentage of literate population) in each
state?