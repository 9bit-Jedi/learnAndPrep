from django.test import TestCase
from django.test import Client
# from accounts.models import *
# from .models import *
# from .views import *
# from script_inference import *
# Create your tests here.
import pandas as pd
import numpy as np
import pickle
import os
from itertools import product


# class MentorModelTest(TestCase):

  # def test_create_mentor(self):
  #   mentor = Mentor.objects.create(
  #     id="test_id",
  #     Name="Test Mentor",
  #     email="test@example.com",
  #     mobile_no="1234567890",
  #     mentor_gender="male",
  #     IIT="IIT Delhi",
  #     state="Delhi",
  #     dropper_status="Dropper",
  #     medium="English",
  #     did_you_change="No",
  #     physics_rank=100,
  #     chemistry_rank=150,
  #     maths_rank=50,
  #   )


def gender_code(gender):
    if gender.lower() == 'female':
        return 0
    elif gender.lower() == 'male':
        return 1
    else:
        return None


def load_model():
    with open('./models/model_saved_mediumchange_priority.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('./models/mentor_encoder_mediumchange_priority.pkl', 'rb') as f:
        mentor_encoder = pickle.load(f)
    return model, mentor_encoder



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


def main():
    
    mentors = pd.read_csv("csv/Mentors_Database (corrected).csv")  ### mentors data dataframe
    mentors = mentors[['id','Name', 'IIT', 'state', 'dropper_status', 'physics_rank', 'chemistry_rank', 'maths_rank', 'medium', 'did_you_change', 'mentor_gender', 'bandwidth']]
    mentors = mentors.rename(columns = {'id':'mentor_id','Name':'mentor_name','dropper_status':'mentor_dropper','maths_rank':'mentor_maths_rank','physics_rank':'mentor_physics_rank','chemistry_rank':'mentor_chemistry_rank','medium':'mentor_medium','did_you_change':'mentor_medium_change', 'state':'mentor_state','IIT':'mentor_iit'})

    df = pd.read_csv("csv/students_real.csv")
    df = df.rename(columns = {'id':'student_id','Name':'student_name','dropper_status':'student_dropper','maths':'student_maths_rank','physics':'student_physics_rank','chemistry':'student_chemistry_rank','medium':'student_medium','did_you_change ':'student_medium_change', 'state':'student_state'})
    for i, row in df.iterrows():
        new_student = pd.DataFrame([row])
        new_student._append(row)
        #   print(new_student)
        #   print(type(new_student['student_name'].iloc[0]))


        new_student = {
            'student_id': row['student_id'],
            'student_name': row['student_name'],
            'student_dropper': row['student_dropper'],
            'student_maths_rank': row['student_maths_rank'],
            'student_physics_rank': row['student_physics_rank'],
            'student_chemistry_rank': row['student_chemistry_rank'],
            'student_medium': row['student_medium'],
            'student_medium_change': row['student_medium_change'],
            'student_state': row['student_state'],
            'student_gender': row['student_gender']
        }
        print(new_student)
        predictions = inference(new_student, mentors).sort_values(by='compatibility_score', ascending=False)
        # predictions.to_csv('results.csv') 
                
        get_my_mentor = predictions[['mentor_id','mentor_name','mentor_iit', 'compatibility_score','mentor_gender','student_gender']].sort_values(by='compatibility_score', ascending=False).head(3)
        #   print(get_my_mentor)

        my_mentor = get_my_mentor[['mentor_id','mentor_name','mentor_iit', 'compatibility_score','mentor_gender']]
        my_student = get_my_mentor[['student_gender']]
        
        print(get_my_mentor)
        
        def allocate_mentor(my_mentor, my_student):
            # Filter mentors based on student's gender
            # student_gender_value = my_student['student_gender'].iloc[0]
            # filtered_mentors = [mentor for mentor in my_mentor if mentor['mentor_gender'] == student_gender_value]
            filtered_mentors = [mentor for mentor in my_mentor if mentor['compatibility_score'] == max(my_mentor, key=lambda x: x['compatibility_score'])['compatibility_score']]

            if filtered_mentors:
                # If there are mentors of the same gender, randomly select one
                # allocated_mentor = max(filtered_mentors, key=lambda x: x['compatibility_score'])
                allocated_mentor = None
                for i in range(0, len(filtered_mentors)):
                    if filtered_mentors[i]['mentor_gender'] == my_student['student_gender'].iloc[0]:
                        allocated_mentor = filtered_mentors[i]
                        print('helloosoosososossssss', allocated_mentor['mentor_gender'], my_student['student_gender'].iloc[0])
                        break
                if allocated_mentor == None:
                    allocated_mentor = filtered_mentors[0]
                    print('helloosoosososossssss', allocated_mentor['mentor_gender'], my_student['student_gender'].iloc[0])
            else:
                # If no mentor of the same gender, randomly select from all mentors
                allocated_mentor = max(my_mentor, key=lambda x: x['compatibility_score'])

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
        
        predictions.head(3).to_csv(f"./csv/results/results_{row['student_name']}.csv")
        predictions.head(1).to_csv(f"./csv/results/results_{row['student_name']}.csv")
        alloted_mentor = pd.DataFrame(alloted_mentor)
        id = alloted_mentor['mentor_id'].iloc[0]
        mentor_row = mentors[mentors['mentor_id'] == id]
        # mentor_row['bandwidth'] = mentor_row['bandwidth'] + 1
        mentors['bandwidth'] = np.where(mentors['mentor_id'] == id, mentors['bandwidth'] + 1, mentors['bandwidth'])

        print(mentor_row)
        print(alloted_mentor['compatibility_score'])
        # return [allocated_mentor, get_my_mentor]

if __name__ == "__main__":
    main()