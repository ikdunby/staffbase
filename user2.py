import requests
import pandas as pd
import json

# this script uploads users present in specified csv file to staffbase
#  it is assumed that the csv  contain data mapped to this format : email;firstName;lastName;avatar
# insert the authorisation token for api with Admin access below

AuthorizationHeader = "Basic insert_api_token_here"


def post(url, item):
    headers = {
        "Content-Type": "application/json",
        "Authorization": AuthorizationHeader
    }

    print("post url : %s " % (url))
    # converting dict to json
    staffbase_request = requests.post(
        url, data=json.dumps(item), headers=headers)
    print(staffbase_request.status_code)


if __name__ == "__main__":
    url = "https://backend.staffbase.com/api/users"
    df = pd.read_csv("email.csv", sep=";")

    items = df.to_dict(orient="records")
    for item in items:
        post(url, item)
