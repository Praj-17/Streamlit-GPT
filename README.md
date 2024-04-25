# Streamlit GPT

Introducing Streamlit GPT, Which creates Streamlit Dasboards for a Given csv File and user input in Natural Language. To create an intuitive dashboard.

## Setup and Installation


Step:1 clone the Repository

```
git clone  https://github.com/Praj-17/Streamlit-GPT.git
```

If you do not have git, you can download the code in a zip file by clicking on the above green button.

Step:2 Install Python `3.10.0`

If you are not able to download this specific version you can try with otehr version between `3.8` and `3.12` Or simpli use `conda` to get the desired version

Step:3 Install Necessary Libraries

Run the following command to install all the libraries

```
pip install -r requirements.txt
```

Step: 4 Setup the `.env` file

Checkout the `example.env` file. Replace the necessary parameters such as `OPENAI_API_KEY` to your own key

Step:4 Run the streamlit Dashboard

```
streamlit run main.py
```

## Folder Structure Explaination

### 📂src
The `src` folder contains all the necessary codes

### 📂modules
The `modules` folder has the important file called `plotgpt.py` which actually implements the plotgpt class from the following repository 

```
https://github.com/stphnma/plotgpt
```
