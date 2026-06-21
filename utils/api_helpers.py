import requests


class APIHelper:

    @staticmethod
    def initiate_taran(user_id, transaction_id):

        url = (
            f"https://sit-app.skorcard.app/"
            f"v1/taran/initiate/{user_id}/{transaction_id}/"
        )

        headers = {
            "x-app": "TARANDM",
            "Content-Type": "application/json",
            "Authorization": (
                "Basic "
                "dGFyYW5kbToyNDM4NzQyZi0xZTY3LTRmMGYtYTFiOC1kYWEzYTk5NmI0Yzk="
            )
        }

        response = requests.post(
            url=url,
            headers=headers,
            json={}
        )

        print(f"URL         : {url}")
        print(f"Status Code : {response.status_code}")
        print(f"Response    : {response.text}")

        return response