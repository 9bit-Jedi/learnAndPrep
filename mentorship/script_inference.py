import pandas as pd
import numpy as np
import random
import pickle
import os
from itertools import product

from django.conf import settings

used_ids = set()

def generate_unique_id(used_ids, id_range=(1000, 9999)):
    while True:
        unique_id = random.randint(*id_range)
        if unique_id not in used_ids:
            used_ids.add(unique_id)
            return unique_id

def gender_code(gender):
    if gender.lower() == 'female':
        return 0
    elif gender.lower() == 'male':
        return 1
    else:
        return None

def load_model():
    with open(os.path.join(settings.BASE_DIR, 'mentorship/models/model_saved.pkl'), 'rb') as f:
        model = pickle.load(f)
    with open(os.path.join(settings.BASE_DIR, 'mentorship/models/mentor_encoder.pkl'), 'rb') as f:
        mentor_encoder = pickle.load(f)
    return model, mentor_encoder

def prepare_new_student_data(new_student):
    new_student_df = pd.DataFrame(new_student, index=[0])
    new_student_df['student_name'] = new_student_df['student_name'].apply(lambda x: x.lower())
    new_student_df['student_dropper'] = new_student_df['student_dropper'].apply(lambda x: x.lower())
    new_student_df['student_medium'] = new_student_df['student_medium'].apply(lambda x: x.lower())
    new_student_df['student_medium_change'] = new_student_df['student_medium_change'].apply(lambda x: x.lower())
    new_student_df['student_state'] = new_student_df['student_state'].apply(lambda x: x.lower())
    new_student_df['student_gender'] = new_student_df['student_gender'].apply(lambda x: x.lower())
    new_student_df['student_gender'] = new_student_df['student_gender'].apply(gender_code)
    # new_student_df['student_id'] = generate_unique_id(used_ids)
    new_student_df['student_id'] = new_student_df['student_id']
    return new_student_df

def prepare_mentor_data(mentors):
    mentors_df = mentors.copy()
    mentors_df['mentor_name'] = mentors_df['mentor_name'].apply(lambda x: x.lower())
    mentors_df['mentor_dropper'] = mentors_df['mentor_dropper'].apply(lambda x: x.lower())
    mentors_df['mentor_medium'] = mentors_df['mentor_medium'].apply(lambda x: x.lower())
    mentors_df['mentor_medium_change'] = mentors_df['mentor_medium_change'].apply(lambda x: x.lower())
    mentors_df['mentor_state'] = mentors_df['mentor_state'].apply(lambda x: x.lower())
    mentors_df['mentor_gender'] = mentors_df['mentor_gender'].apply(lambda x: x.lower())
    mentors_df['mentor_iit'] = mentors_df['mentor_iit'].apply(lambda x: x.replace(" ", "").lower())
    mentors_df['mentor_gender'] = mentors_df['mentor_gender'].apply(gender_code)
    # mentors_df['mentor_id'] = [generate_unique_id(used_ids) for _ in mentors_df['mentor_name']]
    mentors_df['mentor_id'] = mentors_df['mentor_id']
    return mentors_df

def combine_student_mentor_data(student_df, mentors_df):
    rows_mentors = mentors_df.to_dict('records')
    rows_students = student_df.to_dict('records')
    all_pairs = list(product(rows_mentors, rows_students))
    combined_features = pd.DataFrame([{**x, **y} for x, y in all_pairs])
    combined_features['strongest_subject_match'] = (combined_features["student_maths_rank"] == combined_features["mentor_maths_rank"]).astype(int)
    combined_features['weak_subject_match'] = (combined_features["student_physics_rank"] == combined_features["mentor_physics_rank"]).astype(int)
    combined_features['medium_match'] = (combined_features["student_medium"] == combined_features["mentor_medium"]).astype(int)
    combined_features['dropper_match'] = (combined_features["mentor_dropper"] == combined_features["student_dropper"]).astype(int)
    combined_features['state_match'] = (combined_features["mentor_state"] == combined_features["student_state"]).astype(int)
    combined_features['medium_change_match'] = (combined_features["student_medium_change"] == combined_features["mentor_medium_change"]).astype(int)
    return combined_features

def predict_compatibility(model, mentor_encoder, combined_features):
    combined_features['mentor_iit'] = mentor_encoder.transform(combined_features['mentor_iit'])
    
    # Ensure all features match those used during training
    
    # expected_features = ['mentor_iit', 'mentor_gender', 'student_gender', 
    expected_features = ['student_id', 'mentor_id', 'mentor_iit', 'mentor_gender', 'student_gender', 
                         'strongest_subject_match', 'weak_subject_match', 'medium_match', 'dropper_match', 
                         'medium_change_match', 'state_match']
    
    # Adding missing columns with default value 0
    for feature in expected_features:
        if feature not in combined_features.columns:
            combined_features[feature] = 0

    # Dropping any extra columns
    X_new = combined_features[expected_features]

    predictions = model.predict(X_new)
    combined_features['compatibility_score'] = predictions
    return combined_features

def inference(new_student, mentors):
    model, mentor_encoder = load_model()
    student_df = prepare_new_student_data(new_student)
    mentors_df = prepare_mentor_data(mentors)
    combined_features = combine_student_mentor_data(student_df, mentors_df)
    predictions = predict_compatibility(model, mentor_encoder, combined_features)
    return predictions

def main(new_student, mentors):
    # new_student = {
    #   'student_id': '1666',
    #   'student_name': 'Utsah',
    #   'student_dropper': 'no',
    #   'student_maths_rank': 2,
    #   'student_physics_rank': 5,
    #   'student_chemistry_rank': 4,
    #   'student_medium': 'english',
    #   'student_medium_change': 'no',
    #   'student_state': 'delhi',
    #   'student_gender': 'male'
    # }
    # new_student = new_student.rename(columns = {'id':'student_id','Name':'student_name','dropper_status':'student_dropper','maths_rank':'student_maths_rank','physics_rank':'student_physics_rank','chemistry_rank':'student_chemistry_rank','medium':'student_medium','did_you_change ':'student_medium_change', 'state':'student_state'})

    # mentors = pd.read_csv("mentors_final.csv")  ### mentors data dataframe
    mentors = mentors[['id','Name', 'IIT', 'state', 'dropper_status', 'physics_rank', 'chemistry_rank', 'maths_rank', 'medium', 'did_you_change', 'mentor_gender']]

    mentors = mentors.rename(columns = {'id':'mentor_id','Name':'mentor_name','dropper_status':'mentor_dropper','maths_rank':'mentor_maths_rank','physics_rank':'mentor_physics_rank','chemistry_rank':'mentor_chemistry_rank','medium':'mentor_medium','did_you_change':'mentor_medium_change', 'state':'mentor_state','IIT':'mentor_iit'})
    
    predictions = inference(new_student, mentors).sort_values(by='compatibility_score', ascending=False)
    # predictions.to_csv('results.csv') 
    
    
    #### 
    
    get_my_mentor = predictions[['mentor_id','mentor_name','mentor_iit', 'compatibility_score','mentor_gender','student_gender']].sort_values(by='compatibility_score', ascending=False).head(3)

    my_mentor = get_my_mentor[['mentor_id','mentor_name','mentor_iit', 'compatibility_score','mentor_gender']]
    my_student = get_my_mentor[['student_gender']]
    
    # print(get_my_mentor)
    
    def allocate_mentor(my_mentor, my_student):
        # Filter mentors based on student's gender
        student_gender_value = my_student['student_gender'].iloc[0]
        filtered_mentors = [mentor for mentor in my_mentor if mentor['mentor_gender'] == student_gender_value]

        if filtered_mentors:
            # If there are mentors of the same gender, randomly select one
            allocated_mentor = random.choice(filtered_mentors)
        else:
            # If no mentor of the same gender, randomly select from all mentors
            allocated_mentor = random.choice(my_mentor)

        return allocated_mentor

    # Sample mentors data (assuming each mentor has a 'name' and 'gender' field)

    allocated_mentor = allocate_mentor(my_mentor.to_dict('records'),my_student)
    alloted_mentor = {
        'mentor_id': [allocated_mentor['mentor_id']],
        'mentor_name': [allocated_mentor['mentor_name']],
        'mentor_iit': [allocated_mentor['mentor_iit']],
        'compatibility_score': [allocated_mentor['compatibility_score']]
    }
    
    # print(predictions.head(10))
    
    predictions.to_csv(os.path.join(settings.BASE_DIR, 'mentorship/csv/results.csv'))
    alloted_mentor = pd.DataFrame(alloted_mentor)
    return [allocated_mentor, get_my_mentor]
