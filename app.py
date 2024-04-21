import streamlit as st
from langchain.prompts import PromptTemplate
# from langchain.llms import CTransformers,OpenAI
from langchain_openai import OpenAI
from langchain.chains import LLMChain
import re
import os



os.environ['OPENAI_API_KEY'] = 'sk-proj-Koako9tin5Gmzii44hBRT3BlbkFJBIDrBC2y1o5Uwt8QhCbS'

st.title("Personalized Diet and Workout Recommender:coffee:")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('Your Best Food and Exercise Advisor:spoon:')
st.markdown('<style>h3{color: pink;  text-align: center;}</style>', unsafe_allow_html=True)

#llm = CTransformers(model="llama-2-13b-chat.Q4_K_M.gguf", config={'max_new_tokens': 512, "temperature": 0.3})
llm = OpenAI(temperature=0.9)


prompt_template = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 5 breakfast names, 5 lunch names, 5 dinner names, and 5 workout names, "
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight in kg: {weight}\n"
             "Person height in cm: {height}\n"
             "Person Veg_or_Nonveg: {veg_or_nonveg} and in veg don't include egg related or omelette \n"
             "Person generic disease: {disease}\n"
             "and everytime give breakfast names with Breakfast, "
             "lunch names with Lunch, "
             "dinner names with Dinner, "
             "workout names with Workouts, "
             
)

age = st.number_input("Age", min_value=0)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
weight = st.number_input("Weight (Kg)", min_value=0)
height = st.number_input("Height (cm)", min_value=0)
veg_or_nonveg = st.selectbox("Veg or Non-Veg", ["Veg", "Non-Veg"])
disease = st.text_input("Disease")

if st.button("Get Recommendations"):
    chain = LLMChain(llm=llm, prompt=prompt_template)
    input_data = {
        'age': age,
        'gender': gender,
        'weight': weight,
        'height': height,
        'veg_or_nonveg': veg_or_nonveg,
        'disease': disease
    }
    results = chain.run(input_data)
    print ("-------------------results", results)

    # Initialize recommendation lists
    restaurant_names = []
    breakfast_names = []
    lunch_names = []
    dinner_names = []
    workout_names = []

    # Extracting the different recommendations using regular expressions
    # restaurant_matches = re.findall(r'Restaurants:(.*?)Breakfast:', results, re.DOTALL)
    # if restaurant_matches:
    #     restaurant_names = [name.strip() for name in restaurant_matches[0].strip().split('\n') if name.strip()]
 
    breakfast_matches = re.findall(r'Breakfast:(.*?)Lunch:', results, re.DOTALL)
    if breakfast_matches:
        breakfast_names = [name.strip() for name in breakfast_matches[0].strip().split('\n') if name.strip()]

    lunch_matches = re.findall(r'Lunch:(.*?)Dinner:', results, re.DOTALL)
    if lunch_matches:
        lunch_names = [name.strip() for name in lunch_matches[0].strip().split('\n') if name.strip()]

    dinner_matches = re.findall(r'Dinner:(.*?)Workout[s]?:', results, re.DOTALL)
    if dinner_matches:
        dinner_names = [name.strip() for name in dinner_matches[0].strip().split('\n') if name.strip()]

    workout_matches = re.findall(r'Workout[s]?:(.*?)$', results, re.DOTALL)
    if workout_matches:
        workout_names = [name.strip() for name in workout_matches[0].strip().split('\n') if name.strip()]

    st.subheader("Recommendations")
    # st.markdown("#### Restaurants")
    # if restaurant_names:
    #     for restaurant in restaurant_names:
    #         st.write(restaurant)
    # else:
    #     st.write("No restaurant recommendations available.")

    st.markdown("#### Breakfast")
    if breakfast_names:
        for breakfast in breakfast_names:
            st.write(breakfast)
    else:
        st.write("No breakfast recommendations available.")

    st.markdown("#### Lunch")
    if lunch_names:
        for lunch in lunch_names:
            st.write(lunch)
    else:
        st.write("No Lunch recommendations available.")


    st.markdown("#### Dinner")
    if dinner_names:
        for dinner in dinner_names:
            st.write(dinner)
    else:
        st.write("No dinner recommendations available.")

    st.markdown("#### Workouts")
    if workout_names:
        for workout in workout_names:
            st.write(workout)
    else:
        st.write("No workout recommendations available.")
