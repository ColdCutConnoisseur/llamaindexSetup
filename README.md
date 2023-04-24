# llamaindexSetup
Example setup of llamaindex + chatgpt

1. Run ```pip install -r requirements.txt``` to install dependencies.
 <br></br>
2. Create an account on OpenAI and create an API key.
 <br></br>
3. Set the **AKEY** parameter in the *config_file.py* file to your created API key. Or alternatively you can save the key to a JSON file and link that file through the *PATH_TO_KEY* variable in the *config_file.py* file.
 <br></br>
4. Set the **PATH_TO_FOLDER_TO_INDEX** parameter to point to the folder / directory you'd like to index.  Save the config file.
 <br></br>
5. At the bottom of the *revised_sample.py* file, set the **EXAMPLE_QUERY** parameter to whatever you'd like to query.  Save the file.
 <br></br>
6. Run ```python revised_sample.py``` to execute the query on the index and print the coresponding response.



### NOTES ABOUT 'REVISED_SAMPLE' FILE
*revised_sample.py* is more robust form of sample.py.  The new file will build an index file by file within the target directory.  If an EoF PyPDF2 error is caught, the errored-out file will be appended to a bad_files list.  If no error is raised, the file was successfully added to the index.

Once the full directory has been worked through, a print out of all bad files will be outputted.  This will allow further review / the ability to add the **%%EOF** character to the errored-out pdf files.
