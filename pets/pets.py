import streamlit as st
from pets import foodAndSupplyRecommendation, petHealthMonitoringAndAlerts, vetLocator, chatbot

def show_pets_navigation():
    st.title("Pets Information and Features")

    # Create right-side navigation for Pets' features
    feature_selection = st.radio("Select a Feature", ["Food and Supply Recommendations", "Pet Health Monitoring", "Vet Locator", "Chatbot"])

    if feature_selection == "Food and Supply Recommendations":
        foodAndSupplyRecommendation.show_feature()

    elif feature_selection == "Pet Health Monitoring":
        petHealthMonitoringAndAlerts.show_feature()

    elif feature_selection == "Vet Locator":
        vetLocator.show_feature()

    elif feature_selection == "Chatbot":
        chatbot.show_feature()

