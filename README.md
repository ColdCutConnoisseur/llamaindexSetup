# llamaindexSetup
Example setup of llamaindex + chatgpt

1.) Run ```pip install -r requirements.txt``` to install dependencies.
2.) Create an account on OpenAI and create an API key.
3.) Set the **AKEY** parameter in the *config_file.py* file to your created API key.
4.) Set the **PATH_TO_FOLDER_TO_INDEX** parameter to point to the folder / directory you'd like to index.  Save the config file.
5.) At the bottom of the *sample.py* file, set the **EXAMPLE_QUERY** parameter to whatever you'd like to query.  Save the file.
6.) Run ```python sample.py``` to execute the query on the index and print the coresponding response.
