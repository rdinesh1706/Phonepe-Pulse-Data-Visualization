Welcome to my Github phonepe data visualization repository here I done a project in streamlit application to visualize the phonepe data

The concept of this project is to visualize the data using different types graphs by using phonepe data

Project Title:Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly

Skills Used: Github Cloning, Python, Pandas, MySQL query browser, mysql-connector-python, Streamlit, and Plotly.

Project Process Explaination:

1) Download the github folder using git clone in terminal to the required location.

2) Importing all the required libraries.

***The Folder has some files in a structure for different module***

3) By selecting the path we are fetching data from the followings:
			a) Aggregated - Transaction, User, Insurance
			b) Map - Transaction, User, Insurance
			c) Top - Transaction, User, Insurance

4) All the data are converted into a dataframe. 

5) By using Mysql connector the fetched data are stored in Mysql in individual table.

6) Inserting the all the dataframe(data) in the table.

7) With the help of mysql connector we are fetching all the tables and converting into dataframe for the future use.

8) Importing and installing the streamlit application

9) With the help of if-else we are fetching and converting the dataframe into map graph, bar chart, and pie chart.

10) Those if-else has to conditions to satisfies:
		a) type of data
		b) year

11) Below every graphs there will be a tabs section were we can change the tabs to display the data in Quarter wise

12) By using show_agg() function we are visualizing some graphs and charts by using Aggregation data.

13) By using mapLL() function we are visualizing some graphs and charts by using Map data.

14) By using Top() function we are visualizing some graphs and charts by using Top data.

15) By using map_thirdd() function we are visualizing some 3d graphs(out of syllabus).

16) To access these functions there will be a radio button in side bar of the streamlit application.

17) All the graphs and charts are displayed in streamlit application.















