import streamlit as st
#hindi wordnet and codecs,re
from Feature_Extract import features_extraction 
import pickle


st.title('Paraphrase Detection in Hindi text')
txt1 = st.text_area("INPUT TEXT 1",placeholder="Enter hindi text")
txt2 = st.text_area("INPUT TEXT 2",placeholder="Enter hindi text")

if st.button("Check Paraphrase"):
    feat = features_extraction(txt1,txt2)
    svc_model = pickle.load(open('/app/paraphrase_hindi/App/Models/svc_model.pkl', 'rb'))
    svc_pred = svc_model.predict(feat['features'])
    print("svc: ",svc_pred)
    rfc_model = pickle.load(open('/app/paraphrase_hindi/App/Models/rfc_model.pkl', 'rb'))
    rfc_pred = rfc_model.predict(feat['features'])
    print("rfc: ",rfc_pred)

    st.title('Results')
    st.subheader('ML based')
    if svc_pred == 1:
        svc_pred = "Paraphrased"
        st.write('SVC Model Prediction: ',svc_pred)
    else:
        svc_pred = "Not Paraphrased"
        st.write('SVC Model Prediction: ',svc_pred )
    if rfc_pred == 1:
        rfc_pred = "Paraphrased"
        st.write('RFC Model Prediction: ',rfc_pred)
    else:
        rfc_pred = "Not Paraphrased"
        st.write('RFC Model Prediction: ',rfc_pred)

    st.subheader('Rule Based')
    st.write('cosine_similarity ',feat['cosine_value'])
    st.write('jaccard_similarity ',feat['jaccard_value'])
    st.write('bigram_matching ',feat['bigram_value'])
    st.write('syno_match ',feat['syno_value'])