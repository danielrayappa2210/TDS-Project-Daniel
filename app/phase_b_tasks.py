import json
import requests
import pandas as pd
from PIL import Image
import os
import markdown
from git import Repo # type: ignore
from llm_utils import *

def fetch_and_save_data(api_url, output_file_path):
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    try:
        response = requests.get(api_url, verify=False)
        data = response.json()  # Parse the JSON response

        with open(output_file_path, "w") as f:
            json.dump(data, f, indent=4)  # Save the data to a JSON file with indentation

        print(f"Data successfully fetched and saved to {output_file_path}")
        return True
    except:
        return False

def clone_and_commit(repo_url, clone_to_path, commit_message, file_to_modify=None, modification_content=None):
    if clone_to_path.startswith('/'):
        clone_to_path = clone_to_path.strip('/')
    try:
        if os.path.exists(clone_to_path) and os.path.isdir(os.path.join(clone_to_path, ".git")):
            print(f"Repository already exists at {clone_to_path}. Making changes and committing...")
            try:
                repo = Repo(clone_to_path)

                if file_to_modify and modification_content:
                    file_path = os.path.join(clone_to_path, file_to_modify)
                    try:
                        with open(file_path, "w") as f:  # Overwrite or create the file
                            f.write(modification_content)
                        print(f"Modified file: {file_to_modify}")
                    except Exception as e:
                        print(f"Error modifying file: {e}")
                        return False  # Return False if file modification fails

                repo.git.add('.')  # Add all changes, including new files

                if repo.is_dirty(index=True, working_tree=True):  # Check if there are changes to commit
                    repo.git.commit('-m', commit_message)
                    print(f"Committed changes with message: {commit_message}")
                else:
                    print("No changes to commit.")
                return True

            except Exception as e:
                print(f"Error during commit process: {e}")
                return False

        else:
            print(f"Cloning repository to {clone_to_path} and then committing...")
            try:
                repo = Repo.clone_from(repo_url, clone_to_path)

                if file_to_modify and modification_content:
                    file_path = os.path.join(clone_to_path, file_to_modify)
                    try:
                        with open(file_path, "w") as f:
                            f.write(modification_content)
                        print(f"Modified file: {file_to_modify}")
                    except Exception as e:
                        print(f"Error modifying file: {e}")
                        return False

                repo.git.add('.')

                if repo.is_dirty(index=True, working_tree=True):  # Check if there are changes to commit
                    repo.git.commit('-m', commit_message)
                    print(f"Committed changes with message: {commit_message}")
                else:
                    print("No changes to commit.")

                return True

            except Exception as e:
                print(f"Error during clone and commit process: {e}")
                return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    
def extract_web_data(url: str, table_index: int = 1, output_file_path: str = "output.csv"):
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    try:
        tables = pd.read_html(url)
        if table_index < len(tables):
            table = tables[table_index]
            table.to_csv(output_file_path, index=False)
            print(f"Table successfully written to {output_file_path}")
            return True
        else:
            print(f"Table index {table_index} is out of range. Only {len(tables)} tables found.")
            return False
    except Exception as e:
        print(f"An error occurred while extracting web data: {e}")
        return False

def compress_image(input_path: str, output_path: str, quality: int = 85):
    if input_path.startswith('/'):
        input_path = input_path.strip('/')
    if output_path.startswith('/'):
        output_path = output_path.strip('/')
    try:
        with Image.open(input_path) as img:
            img.save(output_path, optimize=True, quality=quality)
        print(f"Image successfully compressed and saved to {output_path}")
        return True
    except:
        return False

def markdown_to_html(markdown_file_path, output_file_path):
    if markdown_file_path.startswith('/'):
        markdown_file_path = markdown_file_path.strip('/')
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    try:
        with open(markdown_file_path, "r") as f:
            markdown_text = f.read()
        
        html = markdown.markdown(markdown_text)
        
        with open(output_file_path, "w") as f:
            f.write(html)
        
        print(f"HTML successfully written to {output_file_path}")
        return True
    except:
        return False
    
def mp3_to_text(mp3_file_path, output_file_path):
    try:
        if mp3_file_path.startswith('/'):
            mp3_file_path = mp3_file_path.strip('/')
        if output_file_path.startswith('/'):
            output_file_path = output_file_path.strip('/')
        
        audio_file = open(mp3_file_path, "rb")
        output_text = mp3_transcription_model_response(audio_file)

        with open(output_file_path, "w") as file:
            file.write(output_text)
        return True
    except:
        return False