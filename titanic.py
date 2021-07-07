import requests
from requests.structures import CaseInsensitiveDict

import streamlit as st
from PIL import Image
import streamlit_analytics

##################################################################################################

icon = Image.open("images/titanic.png")

st.set_page_config(
                page_title = "Titanic Prediction",
                page_icon = icon,
                layout = "centered",
                initial_sidebar_state = "auto",
                )

##################################################################################################

st.markdown("## Find out who did or did not survive on the Titanic.")
st.sidebar.write('Answer these questions to give details of the passenger in question.')

##################################################################################################

image = Image.open("images/titanic-r.png")
st.image(image)

##################################################################################################
# FUNCTIONS
##################################################################################################
def get_passenger_details(sex, embark, title, alone, age, fare):
    data_dict = {
        "Sex" : sex,
        "EmbarkStatus" : embark,
        "Title" : title,
        "IsAlone" : alone,
        "AgeBand" : age,
        "FareBand" : fare
    }

    return data_dict

def dict_to_string():
    data_dict = get_passenger_details(sex, embark, title, alone, age, fare)
    keys = list(data_dict.keys())
    values = list(data_dict.values())

    joined_data = []

    keys_range = range(len(keys))
    for i in keys_range:
        ki = str(keys[i])
        vi = str(values[i])
        if i == 0:
            temp_data = ''.join(['[{','"',ki,'":',vi,','])
        elif keys_range.index(i) != len(keys) - 1:
            temp_data = ''.join(['"',ki,'":',vi,','])
        else: 
            temp_data = ''.join(['"',ki,'":',vi,'}]'])
        joined_data.append(temp_data)
    return ' '.join(joined_data)

def survival_prediction():
    url = "https://a1b2a7aa-333d-4c41-a40a-bd50d4096e53.inferences.beta.layer.co/invocations"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json; format=pandas-records"

    data = dict_to_string()

    resp = requests.post(url, headers=headers, data=data)

    return int(list(resp.text)[1])

def make_prediction():
    click_button = st.button("Click to run simulation")
    if click_button:
        if survival_prediction() == 1:
            st.markdown("### Yes! This fortunate passenger survived!")
            st.balloons()
        else:
            st.markdown("### Alas! This poor passenger did not make it.")

p_sex = st.sidebar.radio('What was the gender of the passenger?', ['Male', 'Female'])
if p_sex == 'Male':
    sex = 0
else:
    sex = 1

if sex == 0:
    p_title = st.sidebar.radio('What was the passenger\'s title?', ['Mr.', 'Master', 'Other'])
    if p_title == 'Mr.':
        title = 1
    elif p_title == 'Master':
        title = 4
    elif p_title == 'Other':
        title = 5

if sex == 1:
    p_title = st.sidebar.radio('What was the passenger\'s title?', ['Miss', 'Mrs.', 'Other'])
    if p_title == 'Miss':
        title = 2
    elif p_title == 'Mrs.':
        title = 3
    elif p_title == 'Other':
        title = 5

p_embark = st.sidebar.radio('At which port did the passenger embark?', ['Southampton', 'Cherbourg', 'Queenstown'])
if p_embark == 'Southampton':
    embark = 0
elif p_embark == 'Cherbourg':
    embark = 1
else:
    embark = 2

p_alone = st.sidebar.radio('Was the passenger travelling alone?', ['No', 'Yes'])
if p_alone == 'No':
    alone = 0
else:
    alone = 1

p_age = st.sidebar.radio('What was the passenger\'s age range?',
    ['Younger than 16 years',
     'Between 16 and 32 years',
     'Between 32 and 48 years',
     'Between 48 and 64 years',
     'Older than 64 years'])
if p_age == 'Younger than 16 years':
    age = 0
elif p_age == 'Between 16 and 32 years':
    age = 1
elif p_age == 'Between 32 and 48 years':
    age = 2
elif p_age == 'Between 48 and 64 years':
    age = 3
else:
    age = 4

p_fare = st.sidebar.radio('What was the passenger\'s fare category?',
    ['Less than 7.91',
     'Between 7.91 and 14.454',
     'Between 14.454 and 31',
     'More than 31'])
if p_fare == 'Less than 7.91':
    fare = 0
elif p_fare == 'Between 7.91 and 14.454':
    fare = 1
elif p_fare == 'Between 14.454 and 31':
    fare = 2
else:
    fare = 3

##################################################################################################

with streamlit_analytics.track():
    if __name__ == "__main__":
        make_prediction()
