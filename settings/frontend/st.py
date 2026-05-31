import streamlit as st
import requests

st.sidebar.title('Task Choice')

task = st.sidebar.radio(
    label='Model Type',
    options=['Computer Vision', 'Speech Recognition', 'Natural Language Processing']
)

if task == 'Computer Vision':
    cv_model = st.sidebar.radio(
        label='CV Models',
        options=['CIFAR-10', 'CIFAR-100', 'Smartphones']
    )


    if cv_model == 'CIFAR-10':
        api = 'http://api:8000/cifar_10/'

        st.title(f'Model {cv_model}')
        st.write('Upload the file and model will try to recognize it')

        uploaded_file = st.file_uploader(label='Choose image', type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            st.image(uploaded_file, caption='Uploaded image', width=200)

            if st.button('Predict'):
                try:
                    request = requests.post(api, files={'image': uploaded_file}, timeout=10)

                    if request.status_code == 200:
                        result = request.json()
                        st.success(f'Label: {result["Prediction"]}')
                    else:
                        st.error(f'Error {request.status_code}')
                except Exception as e:
                    st.error('Cannot connect to the api')


    if cv_model == 'CIFAR-100':
        api = 'http://api:8000/cifar_100/'

        st.title(f'Model {cv_model}')
        st.write('Upload the file and model will try to recognize it')

        uploaded_file = st.file_uploader(label='Choose image', type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            st.image(uploaded_file, caption='Uploaded image', width=200)

            if st.button('Predict'):
                try:
                    request = requests.post(api, files={'image': uploaded_file}, timeout=10)

                    if request.status_code == 200:
                        result = request.json()
                        st.success(f'Label: {result["Prediction"]}')
                    else:
                        st.error(f'Error {request.status_code}')
                except Exception as e:
                    st.error('Cannot connect to the api')


    if cv_model == 'Smartphones':
        api = 'http://api:8000/phones/'

        st.title(f'Model {cv_model}')
        st.write('Upload the file and model will try to recognize it')

        uploaded_file = st.file_uploader(label='Choose image', type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            st.image(uploaded_file, caption='Uploaded image', width=200)

            if st.button('Predict'):
                try:
                    request = requests.post(api, files={'image': uploaded_file}, timeout=10)

                    if request.status_code == 200:
                        result = request.json()
                        st.success(f'Label: {result["Prediction"]}')
                    else:
                        st.error(f'Error {request.status_code}')
                except Exception as e:
                    st.error('Cannot connect to the api')