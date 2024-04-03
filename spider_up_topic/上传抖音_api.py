import requests






url = 'https://open.douyin.com/api/douyin/v1/video/upload_video/?open_id=ba253642-0590-40bc-9bdf-9a1334******'
headers = {
    'access-token': 'act.1d1021d2aee3d41fee2d2add43456badMFZnrhFhfWotu3Ecuiuka******'
}
files = {
    'video': open('/path/to/file', 'rb')
}

response = requests.post(url, headers=headers, files=files)

print(response.text)
