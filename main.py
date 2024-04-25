import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from src import PlotGPT

# Function to plot using matplotlib or seaborn based on provided code
def plot_from_code(plot_code):
    exec(plot_code)

# Main function to create the Streamlit dashboard
def main():
    st.title("Interactive Data Visualization Dashboard")

    # Create a sidebar
    st.sidebar.title("Input Options")

    # Option to type in a prompt in the sidebar
    prompt = st.sidebar.text_input("Type in a Prompt:", "")

    # Option to upload a CSV file in the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

    global df

    # If CSV file is uploaded, read it into a DataFrame
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.write("Uploaded DataFrame:")
        st.sidebar.write(df.head())

    # If prompt is not empty and a CSV file is uploaded, proceed with plotting
    if prompt and uploaded_file is not None:
        # Pass the DataFrame to PlotGPT for inspection
        ai = PlotGPT()
        ai.inspect(df)  # Ensure that df is defined before calling inspect()

        # Get plot code from PlotGPT class based on user input prompt
        plot_code = ai.get_code(prompt)

        # Option to plot using generated code
        if st.sidebar.button("Plot"):
            st.title("Plot")
            fig, ax = plt.subplots()
            plot_from_code(plot_code)
            st.pyplot(fig)
    else:
        # Display a sample image in the main frame
        st.image(Image.open(r"src\assets\sample2.webp"), caption="Sample Image", use_column_width=True)

if __name__ == "__main__":
    main()
