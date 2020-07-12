from clarifai.rest import ClarifaiApp

def get_tags_suggestions(image_url):
#     api_key = "12159ce9c0bc42389ce3baafd60dbd74"
#     url='https://api.clarifai.com/v2/models/bd367be194cf45149e75f01d59f77ba7/outputs'
#     headers = {'Authorization': 'Key '+str(api_key) , 'Content-Type': 'application/json' }

#     data={"inputs": [{"data": {"image": {"url": image_url}}}]}

#     response = requests.post(url, headers=headers, json=data)
#     tags = list(response.json()['outputs'][0]['data']['concepts'])
#     tagsob = []
#     for tag in tags:
#         tagsob.append(tag['name'])
#     return tagsob

    app = ClarifaiApp(api_key='12159ce9c0bc42389ce3baafd60dbd74')
    # model = app.public_models.general_model
    model=app.models.get('food-items-v1.0')
    response = model.predict_by_filename(image_url)
    tags = list(response['outputs'][0]['data']['concepts'])
    tagsob = []
    for tag in tags:
        tagsob.append(tag['name'])
    return tagsob

# a=get_tags_suggestions("/home/udaram/Desktop/DBMS/hi/upload/upload.jpeg")
# print(a)