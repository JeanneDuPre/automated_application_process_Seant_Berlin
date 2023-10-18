import smtplib
from email.message import EmailMessage
import json
import pandas as pd

# get the name of the school and 
def get_filtered_school_data():
    """
    Load school data from a CSV file, filter based on a pattern, exclude specific schools, and extract relevant information.

    Returns:
    - filtered_df: DataFrame containing filtered school data
    - email_list: List of email addresses for selected schools
    - name_list: List of names for selected schools
    """
    # Load the dataset from 'schulen.csv' with ';' as the separator
    df = pd.read_csv('schulen.csv', sep=';')
    
    # Define a regular expression pattern for 'XXGXX' in 'BSN' column
    pattern = r'\d{2}G\d{2}'
    
    # Use str.contains() with regex=True to filter the DataFrame
    filtered_df = df[df['BSN'].str.contains(pattern, regex=True)]
    
    # Define a list of 'BSN' values for schools where I have worked
    filtered_df = filtered_df[(filtered_df['BSN'] != '01G25') & (filtered_df['BSN'] != '04G26')]
    
    # Extract email addresses and names
    filtered_df_list_email = filtered_df['eMail'].to_list()
    filtered_df_list_name = filtered_df['Name'].to_list()
    
    return [filtered_df, filtered_df_list_email, filtered_df_list_name]

filtered_df, filtered_df_list_email, filtered_df_list_name = get_filtered_school_data()

# Read the JSON file
with open('config.json', 'r') as json_file:
    config = json.load(json_file)
    
# Retrieve my email credentials from the configuration
EMAIL_ADDRESS = config.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = config.get('EMAIL_PASSWORD')

# Define the SMTP server and port for Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587

try:
    # Initialize an SMTP server and start a TLS secure connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # TLS for secure connection
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # Iterate through a list of email addresses and school names
    for email, name in zip(filtered_df_list_email, filtered_df_list_name):
        # Create an EmailMessage object
        msg = EmailMessage()
        msg['Subject'] = 'Vertretungslehrkraft Wiesemann ab Klassenstufe 3'
        msg['From'] = EMAIL_ADDRESS 
        msg['To'] = email 
        
        # Compose the email content
        content= f'''
        Sehr geehrtes Team der {name},

        hiermit möchte ich mich initiativ als Vertretungslehrkraft bewerben.
        Zu meiner Person: 
            - B.Ed., M.Ed. + 2. Staatsexamen (Frz, Lat- Gymnasium)
            - 6 Jahre Berufserfahrung (GS ~ 3 Jahre, ISS ~ 3 Jahre, Gymnasium ~ 1/2 Jahr)
            - Fächer: Frz, Lat, Nawi, Sport, Mathe
        Wunsch: 
            - Teilzeit ab 5 Stunden am Tag
            - Vollzeit sehr gern
            - weitere Fächer: Informatik
        Anbei sende ich Ihnen meinen Lebenslauf.
         
        Mit freundlichen Grüßen
        Janine Wiesemann
        '''
        msg.set_content(content)
        
        # Attach a PDF file
        pdf_file_path = 'cv_schule_wiesemann_stand_2023_10_18.pdf'
        with open(pdf_file_path, 'rb') as pdf:
            msg.add_attachment(pdf.read(), maintype='application', subtype='octet-stream', filename=pdf.name)
        
        # Send the email
        server.send_message(msg)
        
    # Quit the SMTP server
    server.quit()
    print("Emails sent successfully.")
except Exception as e:
    print(f"An error ocurred: {str(e)}")
