# Sending emails to multiple recipients with attachement
import smtplib
from email.message import EmailMessage
import json
import pandas as pd

# get the name of the school and 
def get_data(): 
    # df = pd.read_csv('Schulen_2.csv',sep=';')
    df = pd.read_csv('Schulen_2.csv', sep=';')
    # Define a regular expression pattern for 'XXBXX'
    pattern = r'\d{2}G\d{2}'
    # Use the str.contains() method with regex=True to filter the DataFrame
    filtered_df = df[df['BSN'].str.contains(pattern, regex=True)]
    filtered_df = filtered_df[(filtered_df['BSN'] != '01G25') & (filtered_df['BSN'] != '04G26')]
    filtered_df_list_email = filtered_df['eMail'].to_list()
    filtered_df_list_name = filtered_df['Name'].to_list()
    return [filtered_df, filtered_df_list_email, filtered_df_list_name]

filtered_df, filtered_df_list_email, filtered_df_list_name = get_data()

# Read the JSON file
with open('config.json', 'r') as json_file:
    config = json.load(json_file)
    
# Retrieve your email credentials from the configuration
EMAIL_ADDRESS = config.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = config.get('EMAIL_PASSWORD')

smtp_server = 'smtp.gmail.com'
smtp_port = 587

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Use TLS for secure connection
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    
    for email, name in zip(filtered_df_list_email, filtered_df_list_name):
        msg = EmailMessage()
        msg['Subject'] = 'Vertretungslehrkraft Wiesemann ab Klassenstufe 3'
        msg['From'] = EMAIL_ADDRESS 
        msg['To'] = email # müssen valid sein und kein nan enthalten
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
        
        # Attach a PDF file (replace 'path/to/your.pdf' with the actual file path)
        pdf_file_path = 'cv_schule_wiesemann_stand_2023_10_18.pdf'
        with open(pdf_file_path, 'rb') as pdf:
            msg.add_attachment(pdf.read(), maintype='application', subtype='octet-stream', filename=pdf.name)

        server.send_message(msg)
        
    # Quit the SMTP server
    server.quit()
    print("Emails sent successfully.")
except Exception as e:
    print(f"An error ocurred: {str(e)}")
# msg.set_content(f'''
# <!DOCTYPE html>
# <html>
#     <body>
#         <div style="padding:20px 0px">
#             <div style="height: 500px;width:400px">
#                 <img src="https://dummyimage.com/500x300/000/fff&text=Dummy+image" style="height: 300px;"> //TODO mein Bewerbungsbild DANKE!//
#                 <div style="text-align:left;">
#                     <h3>Sehr geehrtes Team der {filtered_df_list_name}</h3>
#                     <p>hiermit möchte ich mich als Vertretungslehrkraft initiativ bewerben.<br>
#                         Zu meiner Person:<br> 
#                             - 1. + 2. Staatsexamen<br> 
#                             - 6 Jahre Berufserfahrung (GS, ISS, Gymnasium)<br> 
#                             - Fächer: Frz, Lat, Nawi, Sport, Mathe)<br> 
#                         Wunsch:<br> 
#                             - Teilzeit ab 5 Stunden am Tag, Vollzeit<br> 
#                         Mit freundlichen Grüßen<br> 
#                         Janine Wiesemann</p>
#                     <a href="#">Read more</a>
#                 </div>
#             </div>
#         </div>
#     </body>
# </html>
# ''', subtype='html'))