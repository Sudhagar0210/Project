Phonepe Pulse Data Visualization and Exploration


Table of Contents

* Overview
* Project Setup
* Project Structure
* Features
* Usage
* Visualizations
* Data Source
* Contributing
* License
* Contact

1. Overview
This project aims to visualize PhonePe Pulse data, providing insights into transactions and user activities across different states in India from 2018 to 2024. 
It leverages Streamlit for the web interface, Plotly for data visualization, and SQL databases for data storage and retrieval.

2. Project Setup
    * Clone the Repository:      
     git clone <repository-url>
     cd <repository-directory>

    * Database Configuration:
      Update the conn variable in app.py with your SQL Server details:
      conn = pyodbc.connect('DRIVER={SQL Server};SERVER=YourServer;DATABASE=YourDatabase;UID=YourUsername;PWD=YourPassword')

    * Run the Application:
      streamlit run app.py

3. Project Structure
   * app.py: The main Streamlit application file containing all the code for data visualization and interaction.
   * requirements.txt: A file listing all the required Python libraries.
  
4. Features
   * Transaction Analysis:-
   
    * Transaction Year Selection: Allows users to select the year for transaction data visualization.
    * Transaction Quarter Selection: Allows users to select the quarter for transaction data visualization.
    * Transaction Type Selection: Allows users to select the type of transaction.
    * Geographical Visualization: Visualizes transaction amounts across different states using a choropleth map.
      
   * Bar Chart Analysis:-
     * Visualizes transaction amounts across different states using bar charts.
       
   * User Analysis:-  
   * User Year Selection: Allows users to select the year for user data visualization.
   * User Quarter Selection: Allows users to select the quarter for user data visualization.
   * Geographical Visualization: Visualizes user counts across different states using a choropleth map.
   * Bar Chart Analysis: Visualizes user counts across different states using bar charts.

     
   * Insights:-  
   * Transaction Insights: Provides detailed insights into transaction counts, amounts, and types.
   * User Insights: Provides detailed insights into user counts and transaction percentages.
  
5. Usage:-
   * Select the Analysis Type: Choose between "Payment" and "Insights" using the radio buttons.
   * Select the Year and Quarter: Use the dropdown menus to select the desired year and quarter.
   * Visualize the Data: View the visualizations and insights on the selected data.

6. Visualizations:-
   
Geographical Visualization:-
   Uses Plotly's px.choropleth for mapping transaction and user data.

Bar Chart Analysis:-
   Uses Plotly's px.bar for visualizing transaction and user data.

7. Data Source:-
   The data used in this project is sourced from PhonePe Pulse, which provides detailed transaction and
   user data across various states in India.

8. Contributing:-
   Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

9.Contact
For any queries or support, please contact:
Your Name :- Sudhagar Chandar
Email: your.sudhakarchandar0210@example.com





