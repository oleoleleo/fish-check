import flaski.database
import flaski.dbmodels
import http.client, urllib.request, urllib.parse, urllib.error, base64
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

base_url ='https://fish-teacher.cognitiveservices.azure.com/'
projectID ='0e061463-50be-41f6-8250-9d19bda4dda4'
publish_iteration_name='Iteration6'
prediction_key='de548dcab28148d6bc555e48663b2bda'

threshold=5

def callAPI(uploadFile):
    predictor=CustomVisionPredictionClient(prediction_key, endpoint=base_url)

    with open(uploadFile, mode='rb') as f:
        results=predictor.classify_image(projectID, publish_iteration_name, f.read())

    result=[]
    for prediction in results.predictions:
        if len(get_fish_data(prediction.tag_name))!=0:
            if prediction.probability * 100 > threshold:
                result.append(get_fish_data(prediction.tag_name))
    return result

def get_fish_data(fishname):
    ses = flaski.database.db_session()
    fish_master = flaski.dbmodels.FishMaster
    fish_data = ses.query(fish_master).filter(fish_master.fish_name == fishname).first()

    fish_data_dict = {}

    if not fish_data is None:
        fish_data_dict['fish_name'] = fish_data.fish_name
        if fish_data.poison == 1:
            fish_data_dict['poison'] = '毒あり'
        else:
            fish_data_dict['poison'] = ''
        fish_data_dict['poison_part']=fish_data.poison_part
        fish_data_dict['wiki_url']=fish_data.wiki_url
        fish_data_dict['picture_path']=fish_data.picture_path
        fish_data_dict['copyright_owner']=fish_data.copyright_owner
        fish_data_dict['copyright_url']=fish_data.copyright_url
    return fish_data_dict
