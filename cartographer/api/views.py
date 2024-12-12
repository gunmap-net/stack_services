import requests, os, json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

baserow_url = os.getenv('BASEROW_URL')
baserow_username = os.getenv('BASEROW_USERNAME')
baserow_password = os.getenv('BASEROW_PASSWORD')
baserow_gunmap_database_id = os.getenv('BASEROW_GUNMAP_DATABASE_ID')
baserow_images_database_id = os.getenv('BASEROW_IMAGES_DATABASE_ID')

def check_json_response(
    response, success_message, failed_message,
    fields_to_check = None,
    size_to_check = None
):
    try:
        if response.status_code != 200:
            print('STATUS CODE WAS NOT 200. CODE WAS: {}'.format(response.status_code))
            print(response)
            print(failed_message)
            json_response = response.json()
            print('RESPONSE: {}'.format(json_response))
            raise Exception(failed_message)

        json_response = response.json()

        if size_to_check:
            if len(json_response) < size_to_check:
                print('Response was smaller than required size {}'.format(size_to_check))
                print('Response was: ')
                print(json_response)
                print(failed_message)
                raise Exception(failed_message)

        if fields_to_check:
            for field_to_check in fields_to_check:
                if field_to_check not in json_response:
                    print('Field {} not in response'.format(field_to_check))
                    print('Response was: ')
                    print(json_response)
                    print(failed_message)
                    raise Exception(failed_message)

        return json_response
    except Exception as e:
        print(e)
        print(failed_message)
        raise Exception(failed_message)

def format_rows(results):
    formatted_rows = []
    for result in results:
        formatted_result = {
            'id': result['id'],
            'title': result['field_3450'],
            'created': result['field_3454'],
            'author': format_multivalue_field(result['field_3451']),
            'organization': format_multivalue_field(result['field_3452']),
            'gunmap_category': format_multivalue_field(result['field_3482']),
            'munition_type': format_multivalue_field(result['field_3483']),
            'munition_platform': format_multivalue_field(result['field_3484']),
            'munition_part': format_multivalue_field(result['field_3515']),
            'munition_caliber': format_multivalue_field(result['field_3517']),
            'fabrication_method': format_multivalue_field(result['field_3518']),
            'diy_level': format_multivalue_field(result['field_3519']),
            'entity_format': format_multivalue_field(result['field_3520']),
            'link': format_multivalue_field(result['field_3484']),
            'thumbnail_url': result['field_3525'],
            'description': result['field_3485'],
            'link': result['field_3453'],
            "images": [],
        }

        #if 'field_3495' in result:
        #    formatted_result['thumbnail_url'] = result['field_3495']

        formatted_rows.append(formatted_result)

    return formatted_rows

def add_images(initial_response, images):
    for entity in initial_response:
        if entity['id'] in images:
            entity['images'] = images[entity['id']]

    return initial_response

def format_multivalue_field(field):
    res = []
    if len(field) > 0:
        for r in field:
            res.append({
                'id': r['id'],
                'value': r['value']
            })

    return res


def ping_view(request):
    return HttpResponse("pong")

def get_most_recent_entities(request):
    size = 'all' if 'size' not in request.GET else request.GET['size']

    token_response = requests.post(
        '{}/api/user/token-auth/'.format(baserow_url),
        json = {
            'username': baserow_username,
            'password': baserow_password,
        },
        headers = {
            'Content-Type': 'application/json',
        }
    )    

    token_response = check_json_response(
        token_response, 
        'ACQUIRED BASEROW TOKEN', 
        'PROBLEM WITH ACQUIRING BASEROW TOKEN',
        fields_to_check=['token', 'refresh_token']
    )    

    token = token_response['token']

    all_links_retrieved = False
    all_rows = []
    get_all_rows_url = \
        '{}/api/database/rows/table/{}/'.format(baserow_url, baserow_gunmap_database_id, size) + \
        '?order_by=-3455' + \
        '&filter__field_3521__boolean=1' + \
        '&filter__field_3462__contains=Odysee' \
        

    if size and size != 'all':
        get_all_rows_url += '&size={}'.format(size)

    while not all_links_retrieved:

        rows_response = requests.get(
            get_all_rows_url,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'JWT ' + token,
            }
        )

        rows_response = check_json_response(
            rows_response, 
            'LISTED ROWS', 
            'PROBLEM WITH LISTING ROWS',
            fields_to_check=['results']
        )

        all_rows.extend(rows_response['results'])

        if size == 'all' and 'next' in rows_response and rows_response['next']:
            get_all_rows_url = rows_response['next']
        else:
            all_links_retrieved = True

    initial_response = format_rows(all_rows)

    images = get_all_images(token)

    full_response = add_images(initial_response, images) 
    
    return JsonResponse(full_response, safe=False)


def get_most_recent_ten_dev(request):
    result = """
        [
           {
              "id":10,
              "order":"4214.00000000000000000000",
              "field_3450":"ECM Process for Making Barrels - Guide",
              "field_3451":[
                 {
                    "id":1,
                    "value":"JeffRod",
                    "color":"blue"
                 } ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@Chaos_Customs#1/Reloading-308win(1)#3",
              "field_3454":"2021-06-01",
              "field_3455":"2023-09-20T00:12:34.179736Z",
              "field_3456":"https://mega.nz/file/MGMjDIhZ#DBm-zofDxo4K8_LE5rUzWpK4m93QWEs3PggoMU4CACo",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":1,
                 "value":"Odysee",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"3fbd07c25edf188ede5b72a371abe975a37679f3",
              "field_3465":false,
              "field_3482":[
                 {
                    "id":2,
                    "value":"Documents",
                    "color":"light-gray"
                 }
              ],
              "field_3483":[
                 {
                    "id":1,
                    "value":"Pistol",
                    "color":"light-gray"
                 }
              ],
              "field_3484":[
              ],
              "field_3485":"The full process for creating ECM barrels, pioneered by Jeffrod.",
              "field_3495": "https://player.odycdn.com/v6/streams/53bdef0a790021cc6f44be58f2d63f0bd763584b/b18371.mp4"
           },
           {
              "id":9,
              "order":"4213.00000000000000000000",
              "field_3450":"DMB Glock Magazine",
              "field_3451":[
                 {
                    "id":2,
                    "value":"DannyMeatball",
                    "color":"blue"
                 }
              ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@Chaos_Customs#1/AK-FRT#f",
              "field_3454":"2022-01-01",
              "field_3455":"2023-09-20T00:12:25.439293Z",
              "field_3456":"https://mega.nz/file/gKcBGRBD#PsGQe7dyk-YOpp8h7kxOLz_TZI_IFaCWvlCogaxOyCU",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":1,
                 "value":"Odysee",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"f14c8a4fb3c42d977a5407032964d64a56b46d56",
              "field_3465":false,
              "field_3482":[
                 {
                    "id":3,
                    "value":"Magazines",
                    "color":"light-gray"
                 }
              ],
              "field_3483":[
                 {
                    "id":1,
                    "value":"Pistol",
                    "color":"light-gray"
                 }
                 
              ],
              "field_3484":[
                 {
                    "id":1,
                    "value":"Glock 17",
                    "color":"light-gray"
                 },
                 {
                    "id":2,
                    "value":"Glock 19",
                    "color":"light-gray"
                 }
              ],
              "field_3485":"A superior printable Glock magazine.",
              "field_3495":""
           },
           {
              "id":8,
              "order":"4212.00000000000000000000",
              "field_3450":"Gunpowder Formula",
              "field_3451":[
                 {
                    "id":3,
                    "value":"HoffmanTactical",
                    "color":"blue"
                 }
              ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@Chaos_Customs#1/Reloading-9mm(1)#2",
              "field_3454":"1994-01-01",
              "field_3455":"2023-09-20T00:12:21.007997Z",
              "field_3456":"https://mega.nz/file/oaVTWYLS#i9ZL4YkRfaASnBfridJKX3Tg1k_jhOOv098tcDtenj8",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":1,
                 "value":"Odysee",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"2a2674cfb541ee710823806b5cf5261c3be08d4c",
              "field_3465":false,
              "field_3482":[
                 {
                    "id":2,
                    "value":"Documents",
                    "color":"light-gray"
                 },
                 {
                    "id":4,
                    "value":"Explosives",
                    "color":"light-gray"
                 }
              ],
              "field_3483":[
                 {
                    "id":5,
                    "value":"Propellant",
                    "color":"light-gray"
                 }
              ],
              "field_3484":[
              ],
              "field_3485":"An easy DIY formula for making your own black powder."
           },
           {
              "id":7,
              "order":"4211.00000000000000000000",
              "field_3450":"Luger Reference Model",
              "field_3451":[
                 {
                    "id":4,
                    "value":"ReferenceModelsRUs",
                    "color":"blue"
                 }
              ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@Chaos_Customs#1/Mauser-bolt-actions#0",
              "field_3454":"1908-01-01",
              "field_3455":"2023-09-20T00:12:17.531285Z",
              "field_3456":"https://mega.nz/file/tPsR2azJ#sZ007g2jppPjqMSHjsZu6c1TX19JsOZLJU1OlHa1EnU",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":1,
                 "value":"Odysee",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"03935734ec3d94d23a0d1c0cc001168147aefdd1",
              "field_3465":false,
              "field_3482":[
                 {
                    "id":5,
                    "value":"Reference Models",
                    "color":"light-gray"
                 }
              ],
              "field_3483":[
                 {
                    "id":1,
                    "value":"Pistol",
                    "color":"light-gray"
                 }
                 
              ],
              "field_3484":[
                 {
                    "id":3,
                    "value":"Luger",
                    "color":"light-gray"
                 }
                 
              ],
              "field_3485":"A complete reference model for the P08 Luger",
              "field_3495": "https://player.odycdn.com/v6/streams/53bdef0a790021cc6f44be58f2d63f0bd763584b/b18371.mp4"
           },
           {
              "id":6,
              "order":"4210.00000000000000000000",
              "field_3450":"Practical Scrap Metal Arms #1: Building the Luty",
              "field_3451":[
                 {
                    "id":5,
                    "value":"Professor Parabellum",
                    "color":"blue"
                 }
              ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@Chaos_Customs#1/Luty-22cal#c",
              "field_3454":"2016-01-01",
              "field_3455":"2023-09-20T00:11:33.940046Z",
              "field_3456":"https://mega.nz/file/BWV2hCJa#ZimIpK5xRJS46dIfSVhFixah8bvNKIc3Rd_7pWxJUmk",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":2,
                 "value":"DEFCAD",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"c347ccbaf272265fddf347f4a7cbfeb5e6107dac",
              "field_3465":false,
              "field_3482":[{
                    "id":2,
                    "value":"Documents",
                    "color":"blue"
              }],
              "field_3483":[{
                    "id":2,
                    "value":"Submachine Gun",
                    "color":"blue"
              }],
              "field_3484":[{
                    "id":4,
                    "value":"Luty",
                    "color":"blue"
              }],
              "field_3485":"Prof. Parabellum's first released guide, for building the famous Luty submachine gun.",
              "field_3495": "https://player.odycdn.com/v6/streams/53bdef0a790021cc6f44be58f2d63f0bd763584b/b18371.mp4"
           },
           {
              "id":5,
              "order":"4209.00000000000000000000",
              "field_3450":"G0 Cutcode",
              "field_3451":[
                 {
                    "id":6,
                    "value":"Ghost Gunner",
                    "color":"blue"
                 }
              ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@Funky_Fetus_Fabrications#0/Crushed-17L-Family-Pack#5",
              "field_3454":"2023-05-27",
              "field_3455":"2023-09-19T17:12:57.725667Z",
              "field_3456":"https://mega.nz/file/4OcESB4Z#PrhtuQyapzcXYvD0TuA5dkf3NXEL-wPPKwSbKkdx3dE",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":2,
                 "value":"DEFCAD",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"58b0a4ed6e688598acc717931c85d939fcdb94f9",
              "field_3465":false,
              "field_3482":[{
                 "id":20,
                 "value":"Machinable Firearms",
                 "color":"blue"
              }],
              "field_3483":[{
                 "id":1,
                 "value":"Pistol",
                 "color":"blue"
              }],
              "field_3484":[{
                 "id":2,
                 "value":"Glock 19",
                 "color":"Blue"
              }],
              "field_3485":"The cutcode to mill the G0 chassis.",
              "field_3495": "https://player.odycdn.com/v6/streams/53bdef0a790021cc6f44be58f2d63f0bd763584b/b18371.mp4"
           },
           {
              "id":4,
              "order":"4208.00000000000000000000",
              "field_3450":"M1911 Blueprint",
              "field_3451":[
                 {
                    "id":7,
                    "value":"US Army",
                    "color":"blue"
                 }
              ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@Funky_Fetus_Fabrications#0/Skippy-17#8",
              "field_3454":"1911-01-01",
              "field_3455":"2023-09-17T04:21:40.423383Z",
              "field_3456":"https://mega.nz/file/cSkXwKiS#qED1yjj2xjoD8Ss4rDh2dgNC6_zkM9-qEp6kqkWAN5Q",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":1,
                 "value":"Odysee",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"8b99cf8801cf1e3b59c8978dd6d26606753734a1",
              "field_3465":false,
              "field_3482":[
                 {
                    "id":10,
                    "value":"Blueprints",
                    "color":"gray"
                 }
              ],
              "field_3483":[
                 {
                    "id":1,
                    "value":"Pistol",
                    "color":"green"
                 }
              ],
              "field_3484":[
                 {
                    "id":5,
                    "value":"M1911",
                    "color":"dark-blue"
                 }
              ],
              "field_3485":"Original blueprints for the M1911 pistol",
              "field_3495": "https://player.odycdn.com/v6/streams/53bdef0a790021cc6f44be58f2d63f0bd763584b/b18371.mp4"
           },
           {
              "id":3,
              "order":"4207.00000000000000000000",
              "field_3450":"DD17.2 Printable Glock",
              "field_3451":[
                 {
                    "id":8,
                    "value":"FreeMenDontAsk",
                    "color":"blue"
                 }
              ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@TheGatalogPrintableFramesAndReceivers#0/DD17-2#1",
              "field_3454":"2021-05-15",
              "field_3455":"2023-09-16T00:00:28.193805Z",
              "field_3456":"https://mega.nz/file/xXFwSJzB#VjoqwZr64ytXd-FKaVyJagieXi0txnVyR3BfcI_QQMo",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":1,
                 "value":"Odysee",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"1b20a74efc8c9a6ac3aa5e77fccd6eafeed73fa7",
              "field_3465":false,
              "field_3482":[
                 {
                    "id":1,
                    "value":"Printable Firearms",
                    "color":"gray"
                 }
              ],
              "field_3483":[
                 {
                    "id":1,
                    "value":"Pistol",
                    "color":"green"
                 }
              ],
              "field_3484":[
                 {
                    "id":1,
                    "value":"Glock 17",
                    "color":"orange"
                 }
              ],
              "field_3485":"A 3D-printable Glock 17 frame, paired with DIY front and rear rails.",
              "field_3495": "https://player.odycdn.com/v6/streams/53bdef0a790021cc6f44be58f2d63f0bd763584b/b18371.mp4"
           },
           {
              "id": 2,
              "order":"4206.00000000000000000000",
              "field_3450":"King Cobra 9",
              "field_3451":[
                 {
                    "id":9,
                    "value":"Derwood",
                    "color":"blue"
                 }
              ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@Derwood/KC9",
              "field_3454":"2022-01-12",
              "field_3455":"2023-09-15T00:00:33.523530Z",
              "field_3456":"https://mega.nz/file/weEUlLbJ#3bAQfFt7G3N1olC-VvetToKgs19rLTddsl1Yp9m0j4w",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":2,
                 "value":"DEFCAD",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"5cf0b5aa325c1ca8bf330600ac5afa931983a32f",
              "field_3465":false,
              "field_3482":[
                 {
                    "id":1,
                    "value":"Printable Firearms",
                    "color":"gray"
                 }
              ],
              "field_3483":[
                 {
                    "id":3,
                    "value":"Pistol-Caliber Carbine",
                    "color":"green"
                 }
              ],
              "field_3484":[
                 {
                    "id":10,
                    "value":"KC9",
                    "color":"orange"
                 }
              ],
              "field_3485":"The latest 3D printed gun from Derwood, featuring magnet delay and a custom bolt with extractor!",
              "field_3495": "https://player.odycdn.com/v6/streams/53bdef0a790021cc6f44be58f2d63f0bd763584b/b18371.mp4"
           },
           {
              "id": 1,
              "order":"4205.00000000000000000000",
              "field_3450":"Liberator",
              "field_3451":[
                 {
                    "id":10,
                    "value":"Defense Distributed",
                    "color":"blue"
                 }
              ],
              "field_3452":[
                 
              ],
              "field_3453":"https://odysee.com/@Funky_Fetus_Fabrications#0/DarkSouls-19#4",
              "field_3454":"2013-05-27",
              "field_3455":"2023-09-15T00:00:30.188472Z",
              "field_3456":"https://mega.nz/file/pOMkWIiR#ho6igaRRJIzFF9xgKfEE2yEy9iAlIR_7rVdVE8UKQG8",
              "field_3457":"",
              "field_3458":[
                 
              ],
              "field_3459":[
                 
              ],
              "field_3460":false,
              "field_3461":false,
              "field_3462":{
                 "id":2,
                 "value":"DEFCAD",
                 "color":"light-gray"
              },
              "field_3463":"{}",
              "field_3464":"4315ebaffc9b5e65a90d21d81991e70a0af6a80f",
              "field_3465":false,
              "field_3482":[
                 {
                    "id":1,
                    "value":"Printable Firearms",
                    "color":"gray"
                 }
              ],
              "field_3483":[
                 {
                    "id":1,
                    "value":"Pistol",
                    "color":"green"
                 }
              ],
              "field_3484":[
                 {
                    "id":20,
                    "value":"Liberator",
                    "color":"orange"
                 }
              ],
              "field_3485":"The Liberator is the world's first fully 3D-printed gun released to the public",
              "field_3495": "https://player.odycdn.com/v6/streams/53bdef0a790021cc6f44be58f2d63f0bd763584b/b18371.mp4"
           }
        ]
    """;

    initial_response = format_rows(json.loads(result))

    images = {
        1: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
        2: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
        3: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
        4: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
        5: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
        6: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
        7: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
        8: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
        9: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
        10: [
            "https://thumbs.odycdn.com/17df591bbe967a8be08408dccd6a5c3e.webp",
        ],
    }

    full_response = add_images(initial_response, images) 

    return JsonResponse(full_response, safe=False)


def get_all_images(token):
    get_all_rows_url = '{}/api/database/rows/table/{}/'.format(baserow_url, baserow_images_database_id)

    rows_response = requests.get(
        get_all_rows_url,
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + token,
        }
    )

    rows_response = check_json_response(
        rows_response, 
        'LISTED ROWS', 
        'PROBLEM WITH LISTING ROWS',
        fields_to_check=['results']
    )

    image_map = {}

    for result in rows_response['results']:
        if 'field_3499' in result:
            entity_id = result['field_3499'][0]['id']
            image_url = result['field_3496']

            if entity_id not in image_map:
                image_map[entity_id] = []
            image_map[entity_id].append(image_url)

    return image_map
