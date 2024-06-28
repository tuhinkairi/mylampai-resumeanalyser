import requests
import json
url = "http://127.0.0.1:8000/extract_structured_data"

text = """SHUBHAM KUMAR  |  21CH10065
CHEMICAL ENGG. (B.Tech 4Y)
EDUCATION
Year Degree/Exam Institute CGPA/Marks
2025 B.TECH IIT Kharagpur 8.67 / 10
2021 Intermediate Eamination Bihar School Examination Board 84.8%
2019 Matriculation Examination Central Board of Secondary Education 94.2%
PROJECTS
Multi-Account Todo | Self Project                                                                                                                            May'23-Jun'23
• Enhanced To-Do List to a full-stack web application for multiple users with a secure login system using the MERN stack.
• Utilized React framework to build an interactive and responsive frontend interface, enhancing the user's overall experience.
• Used Node.js as runtime and Express framework in the backend, providing a robust and scalable server-side architecture.
• Leveraged MongoDB Atlas for storing and retrieving user data, ensuring scalable and continuous availability of the database.
Link-Generator | Self Project                                                                                                                                                 May'23
• Devised a full-stack web application for file sharing using the MERN stack, which generates a share link for the uploaded file.
• Implemented the frontend using React framework, providing a user-friendly interface for uploading files and link generation.
• Leveraged MongoDB Atlas for the storage of the uploaded files, ensuring uninterrupted availability and a scalable database.
My Weather App | Self Project                                                                                                                                              May'23
• Developed a weather application that utilizes API calls to provide the current weather and weekly forecast for any location.
• Designed a responsive interface using React that seamlessly adapts to API response, enhancing the user's overall experience.
• Integrated RAPID API's GeoDB API and OpenWeather API for fetching location and weather information of the specified place.
Flip Card Game | Self Project                                                                                                                                                March'23
• Created a card-flipping game using React framework which counts the number of flips the user makes to match all the cards.
• Utilized CSS to create a responsive frontend interface and implement animations, enhancing the overall user experience.
• Successfully deployed the project on Netlify, safely encoding the API Keys in environment variables for enhanced security.
Arduino-based Sensitive Metal Detector | Course Project | IIT Kharagpur                                                      March'22-June'22
Prof. Soumyadip Chaoudhary | Rubber Technology, IIT Kharagpur
• Collaborated with a team for a metal detector project, achieving high sensitivity to detect metal within a range of 1 meter.
• Showcased the prototype's capability to detect a range of metals, encompassing both ferrous and non-ferrous elements.
• Designed the digital circuit using EasyCAD software, prepared the presentation, and delivered it in front of the whole batch.
SKILLS AND EXPERTISE
Programming : C | C++ | JavaScript | HTML | CSS | Python | Node.js | MongoDB | Express.js*
Libraries : C++ STL | React JS | Bootstrap | Mongoose | Tailwind CSS* | NumPy* | Pandas* | Matplotlib* | Seaborn*
Software : VS Code | Git & GitHub | MongoDB Atlas | MongoDB Compass | TinkerCAD | FreeCAD | Arduino | Jupyter
Notebook | Google Colaboratory | MATLAB*                                                                        (* denotes intermediate level knowledge)
COMPETITION/CONFERENCE
• Currently among the top 1.8% of Programmers on the CodeChef platform, with the highest rating of 1858 (4 stars).
• Secured a rank of 90 in CodeChef Starters 97 Division 2 among more than 1500 Division 2 rated candidates.
COURSEWORK INFORMATION
Computer Science: Programming and Data Structures Theory | Programming and Data Structures Laboratory 
Mathematics:           Advanced Calculus | Linear Algebra, Numerical and Complex Analysis | Transform Calculus
Core:                    Instrumentation and Process Control | Reaction Engineering | Chemical Process Calculations
Others:                     Electrical Technology | DIY Project | Basic Engineering Mechanics | Physics of Waves | Physics Laboratory
CERTIFICATIONS
Guided Path | Coding Ninjas                                                                                                                                               June'23
• Successfully completed the Object Oriented Programming Course in C++, offered by Coding Ninjas with Codestudio.
Machine Learning Specialization | Stanford University (Coursera)                                                                     April'23-July'23
• Successfully completed the Supervised Machine Learning and Unsupervised Learning Courses offered through Coursera.
AWARDS AND ACHIEVEMENTS
• Ranked in the top 6.7% among 1,40,000+ shortlisted candidates in the Joint Entrance Examination Advanced 2021.
• Ranked in the top 1.5% among 1 million+ candidates who registered for the Joint Entrance Examination Mains 2021.
EXTRA CURRICULAR ACTIVITIES
• Volunteered for NSS, attended a 7-day camp, and facilitated Medical Camp, and a talk on Stem Cell Donation in Shola Dahar.
• Member of the Silver Winning team of Pandit Madan Mohan Malviya Hall of Residence in the Illumination for the year 2022.
• Served as Associate Member at Institute Wellness Group for the year 2022, and organised events like Khatt, Halloween Night.
!Self declared by the student, CDC could not verify the relevant documents"""
data = {"cv_text":text}
headers = {"Content-Type": "application/json"}
response_extract = requests.post(url, data=json.dumps(data),headers=headers)

# Check the response
if response_extract.status_code == 200:
    extract_result = response_extract.json()
    description = extract_result.get("Description", "")

    # Prepare the data for the quantification endpoint
    text_to_check = {"points_to_check": description}
    url_quantification = "http://127.0.0.1:8000/quantification"
    
    # Send the data to the quantification endpoint
    response_quantification = requests.post(url_quantification, json=json.dumps(text_to_check),headers=headers)
    
    # Check the response and print it
    if response_quantification.status_code == 200:
        print(response_quantification.json())
    else:
        print("Error in quantification request:", response_quantification.status_code, response_quantification.text)
else:
    print("Error in extract_structured_data request:", response_extract.status_code, response_extract.text)