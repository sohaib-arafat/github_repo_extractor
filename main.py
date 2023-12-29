import requests

def retrieve_github_repo_contents(owner, repo_name, path="", access_token=None):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{path}"
    headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file':
                yield item
                print(f"Processing file: {item['path']}")
            elif item['type'] == 'dir':
                yield from retrieve_github_repo_contents(owner, repo_name, item['path'], access_token)
    else:
        print(f"Failed to retrieve contents. Status code: {response.status_code}")
        try:
            error_message = response.json()['message']
            print(f"Error message: {error_message}")
        except Exception as e:
            print(f"Error parsing response: {e}")
        return None

def save_to_txt_file(contents, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for item in contents:
            file_url = item['download_url']
            file_content = requests.get(file_url).text
            file.write(f"File: {item['path']}\n")
            file.write(file_content)
            file.write("\n\n")

owner = "YOUR_OWNER"
repo_name = "YOUR_REPO_NAME"
access_token = "TOKEN"

contents = retrieve_github_repo_contents(owner, repo_name, access_token=access_token)

if contents:
    save_to_txt_file(contents, "github_repo_contents.txt")
    print("Repository contents saved to github_repo_contents.txt")
else:
    print("Failed to retrieve repository contents")
