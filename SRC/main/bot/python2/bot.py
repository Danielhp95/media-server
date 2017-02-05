from luis_sdk import LUISClient


########## KEYS #############################
''' change these when you create a new bot '''
SUBSCRIPTION_KEY = 'f6c474f92e814ead826f2c6c0d6730f8'
APP_ID = '0849980a-9dc3-4765-ade4-a315be963325'



########## BOT MAGIC FUNCTIONS ##############
'''
Initialize the bot with the appropriate key and ID
'''
def build_bot(subscription_key, app_id):
    client = LUISClient(app_id, subscription_key, True)
    return client


'''
Depending on the confidence value, return an appropritate lexical construct 
'''
def process_confidence(con):
    response = ""
    if   con > 0.9: response = "I am very confident that "
    elif con > 0.6: response = "It is most likely that "
    elif con > 0.3: response = "It is possible that "
    else:           response = "I'm not too confident that "
    return response


'''
Perform action
'''
def process_action(intent_type, media_type, entities):
    # TODO: call functions from the downloader or the manager
    result = "CAPTAIN: Aye! Captain will now proceed to " + intent_type + " this " + media_type + " for you. You requested " + entities[0].get_name().title() + "."
    
    return result


'''
Process the LUISResponse object and depending on that perform an action
The LUISResponse contains the classification of intent and entities in the
text input by the user
'''
def process_media(res, silent):
    # get the information included in the response
    entities = res.get_entities() 

    media_type = ""

    # process the entities to figure out of which media type query refers to
    books  = sum([entity.get_score() for entity in entities if 'Book'  in entity.get_type() or 'Writer'   in entity.get_type()])
    films  = sum([entity.get_score() for entity in entities if 'Film'  in entity.get_type() or 'Director' in entity.get_type()])
    songs  = sum([entity.get_score() for entity in entities if 'Song'  in entity.get_type() or 'Musician' in entity.get_type()])
    albums = sum([entity.get_score() for entity in entities if 'Album' in entity.get_type() or 'Musician' in entity.get_type()])
    maximum = max(books, films, songs, albums)

    if maximum < 0.2:
        if not silent:
            print("CAPTAIN: Arrrr! I don't understand what media you want. Is it a film, a song, or a book?")
        status = -1
        return
    elif maximum == books: media_type = 'book'
    elif maximum == films: media_type = 'film'
    elif maximum == songs: media_type = 'song'
    else:                  media_type = 'album'    

    return media_type 


def process_intent(res, silent):
    # get the information included in the response
    intent   = res.get_top_intent()
    media_type = process_media(res, silent=True)

    intent_type = ""

    # process the intent whether it is of type get or find, or ask for clarification if none
    if 'Find'  in intent.get_name() and intent.get_score() > 0.4 :
        intent_type = 'find'
    elif 'Get' in intent.get_name() and intent.get_score() > 0.4 :
        intent_type = 'get'
    else:
        if not silent:
            print("CAPTAIN: Arrrr! I don't understand. Should I search for or download this " + media_type + "?")
        status = -2
        return

    return intent_type




################ MAIN SCRIPT ##################
welcome_msg = u'CAPTAIN: Welcome to the Media Server! I`m the Captain. You can ask me to download media for you, either by name or by artist, or we can talk about something that interests you, be it books, films, or songs.\n'

status = 0
media_type = ""
intent_type = ""
entities = []


try:
    CAPTAIN = build_bot(SUBSCRIPTION_KEY, APP_ID)

    print(welcome_msg)

    while(True):     
        print('ME: ')
        user_input = raw_input()
        
        res = CAPTAIN.predict(user_input)
        dialog = res.get_dialog()
        entities = res.get_entities()
        
        if len(entities) != 0:
            # if the query appears to be complete, i.e. no missing params, pursue it
            media_type = process_media(res, silent=False)
            if status == -1:
                 media_type = raw_input().lower()
     
            intent_type = process_intent(res, silent=False)
            if status == -2:
                 intent_type = raw_input().lower()
            
            # now process query: search or download and display results 
            print(process_action(intent_type, media_type, entities))


        # otherwise, loop until all data is completed
        while len(entities) == 0 and dialog is not None and not dialog.is_finished():
            print(u'CAPTAIN: %s\nME:'% res.get_dialog().get_prompt())
            missing_param = raw_input()

            if missing_param.lower() == 'nevermind':
                print(u'CAPTAIN: Ok\n')
                break
            
            res_new = CAPTAIN.reply(missing_param, res)
            if res_new != res:
                res = res_new
                break

except Exception, exc:
    print(exc)
