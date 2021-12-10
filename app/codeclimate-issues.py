import httpx
import asyncio
import pandas as pd
import os
import argparse


async def main(repo_id: str, codeclimate_token: str, file_name: str):
    async with httpx.AsyncClient() as client:
        latest_snapshot = await get_latest_snapshot(
            repo_id=repo_id, codeclimate_token=codeclimate_token, client=client
        )

        dataframe = pd.DataFrame()
        page = 1
        while True:
            request = await client.get(
                f"https://api.codeclimate.com/v1/repos/{repo_id}/snapshots/{latest_snapshot}/issues?page[size]=100&page[number]={page}",
                headers=dict(
                    Accept="application/vnd.api+json",
                    Authorization=f"Token token={codeclimate_token}",
                ),
            )
            data = request.json()["data"]
            if len(data) <= 0:
                break

            for row in data:
                dataframe = dataframe.append(row["attributes"], ignore_index=True)
            page += 1

        dataframe.to_csv(file_name)


async def get_latest_snapshot(
    repo_id: str, codeclimate_token: str, client: httpx.AsyncClient
) -> str:
    request = await client.get(
        f"https://api.codeclimate.com/v1/repos/{repo_id}",
        headers=dict(
            Accept="application/vnd.api+json",
            Authorization=f"Token token={codeclimate_token}",
        ),
    )
    return request.json()["data"]["relationships"]["latest_default_branch_snapshot"][
        "data"
    ]["id"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Filename to export csv")
    parser.add_argument("-t", "--token", help="Codeclimate Token")
    parser.add_argument("-r", "--repo", help="Repository ID")

    output = parser.parse_args().output
    token = parser.parse_args().token
    repo = parser.parse_args().repo

    if os.name == "nt":  # windows fix = https://stackoverflow.com/a/66772242
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(repo_id=repo, codeclimate_token=token, file_name=output))
