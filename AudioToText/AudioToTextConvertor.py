import os
from builtins import print
import speech_recognition as sr
from gtts import gTTS
from NLTK import LexicalAnalyzer
from Constants import Constants
from datetime import datetime
import re
from DBase import DBscript
from Utils import Conversation
from word2number import w2n

class AudioToTextConvertor:

    def __init__(self, connection):
        self.comment_flag = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.count = 1
        self.conv_count = 0
        self.text = ""
        self.previous_text = ""
        self.connection = connection
        self.keyword = "Ganesh"
        self.context_change_flag = False # True ->In the context
        self.is_query_answered = False
        self.keyword_appearance_list = list()
        self.break_flag = False
        self.role_id = 1001
        self.dbscript = DBscript.DBscript()
        self.interactor_words = ""
        self.fCchange_flag = False

    def verify_story_in_db(self,key):
        query = {"Story_name": key}
        collection = self.connection.story_collection
        if collection.find(query).count() > 0:
            return True
        return False

    def insert_conversation(self, flag, text):
        date: datetime = datetime.utcnow()
        if flag == True:
            conversation = Conversation.Conversation(text, "Agent", date)
            self.dbscript.insertConversation(conversation)
        elif flag == False:
            conversation = Conversation.Conversation(text, "Primary interactor", date)
            # self.agent_insert_count += 1
            self.dbscript.insertConversation(conversation)

    def conversation_loop(self):
        while(True == True):
            with self.microphone as source:
                print("Speak :")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                if self.conv_count < 5:
                    # self.text = self.text+" "+self.recognizer.recognize_google(audio)
                    try:
                        text = self.recognizer.recognize_google(audio)
                        print("You said : {}".format(text))
                        self.interactor_words = text
                        return text
                    except:
                        print("Sorry could not recognize what you said")
                    #text = input()
                    self.conv_count += 1
                else:
                    text = ""
                    self.conv_count = 0
                    #return text
                #return text
                #print("You said : {}".format(text))
                #self.interactor_words = text
                #self.insert_conversation(False, text)
        #print("speak: ")
        #text = input()
        #self.insert_conversation(False,text)
        #self.interactor_words = text
        #return text

    def story_number_exception(self):
        self.previous_text = self.text
        self.text = ""
        # keyword_appearance_list = list()
        sentence = "Story number couldn't be found"
        self.play_audio_agent(sentence, "snf")
        return

    def verify_story(self, story_no):
        story = self.fetch_story(story_no)
        if story['developer'] == self.role_id:
            return True
        else:
            return False

    def comment_search(self, story_id):
        query = {"Story_id": story_id}
        collection = self.connection.comment_collection
        if collection.find(query).count() > 0:
            return True
        return False

    def search_comment(self, story_no):
        date: datetime = datetime.utcnow()
        query1 = {"Story_id": story_no}
        collection = self.connection.comment_collection
        list_of_data = collection.find(query1)
        count = collection.find(query1).count()
        return list_of_data[0]

    def verify_comment(self, story_no):
        found_comment_flag = False
        flag = False
        count = 0
        story_validation = self.verify_story(story_no)
        if self.comment_search(story_no) == True:
            comment = self.search_comment(story_no)
            if comment['User_id'] == self.role_id:
                flag = story_validation
                found_comment_flag = True
        else:
            flag = story_validation
            found_comment_flag = False
        return flag, found_comment_flag

    def greeting(self):
        x = str()
        for x in Constants.greeting_words:
            x = x.casefold()
            if x in self.text.casefold():
                return True

    def get_verb_n_noun(self, analysis):
        exc_flag  = False
        flag0 = False
        data_string = ""
        flag1 = False
        for i in range(len(analysis)):
            if exc_flag == False:
                if analysis[len(analysis)-1][1] == "NN" or analysis[len(analysis)-1][1] == "NNP":
                    if len(analysis) > 2:
                        if flag0 == False and flag0 == False:
                            exc_flag = True
                            continue

                if analysis[i][1] == "VB" or analysis[i][1] == "WP" or analysis[i][1] == "WRB":
                    if analysis[i][0] in Constants.fetch_verbs :
                        flag0 = True
                elif analysis[i][1] == "NN" and analysis[i][0] in Constants.fetch_verbs:
                    flag0 = True
                elif len(analysis) > 2 and analysis[i][1] == "JJ" and analysis[i + 1][1] == "CD":
                    flag1 = True
                    if analysis[i][0] == 'story' or analysis[i][0] == 'Story':
                        analysis[i][0] = 'Story'
                    if analysis[i + 1][0] == 'six' and (analysis[i][0] == 'story' or analysis[i][0] == 'Story'):
                        analysis[i][0] = 'Story'
                        analysis[i + 1][0] = '6'
                    if analysis[i + 1][0] == 'five' and (analysis[i][0] == 'story' or analysis[i][0] == 'Story'):
                        analysis[i][0] = 'Story'
                        analysis[i + 1][0] = '5'
                    data_string = analysis[i][0] + analysis[i + 1][0]
                    return data_string
                elif ((analysis[i][1] == "NNP" and analysis[i + 1][1] == "NN") and analysis[i][1] != self.keyword) or \
                        ((analysis[i][1] == "NNP" and analysis[i + 1][1] == "NNP") and analysis[i][1] != self.keyword):
                    if flag0 == False and flag0 == False:
                        self.story_number_exception()
                    continue
                elif (analysis[i][1] == "NN" and analysis[i + 1][1] == "CD") or (analysis[i][1] == "NNP" and analysis[i + 1][1] == "CD"):
                    flag1 = True
                    if analysis[i][0] == 'story' or analysis[i][0] == 'Story':
                        analysis[i][0] = 'Story'
                    if analysis[i + 1][0] == 'six' and (analysis[i][0] == 'story' or analysis[i][0] == 'Story'):
                        analysis[i][0] = 'Story'
                        analysis[i + 1][0] = '6'
                    if analysis[i + 1][0] == 'five' and (analysis[i][0] == 'story' or analysis[i][0] == 'Story') :
                        analysis[i][0] = 'Story'
                        analysis[i + 1][0] = '5'
                    data_string = analysis[i][0] + analysis[i + 1][0]
                    return data_string
        return data_string

    def play_audio_agent(self, sentence, file_name):
        myobj = gTTS(text=sentence, lang='en', slow=False)
        file_name = file_name + ".mp3"
        myobj.save(file_name)
        os.system("mpg321 " + file_name)
        print("inserting conversation of agent")
        self.insert_conversation(True, sentence)
        print("inserting conversation of actor: " + self.interactor_words)

        self.insert_conversation(False, self.interactor_words)
        print(sentence + "\n")

    def analyse_the_respose(self, ans):
        self.text = ans
        lexical_analyzer = LexicalAnalyzer.LexicalAnalyzer()
        analysis, self.keyword_appearance_list, only_token_list = lexical_analyzer.analyze_and_search(
            text=self.text, keyword=self.keyword)
        print("lexical analysis done")
        if self.context_change_flag != True:
            print("Entered conversation")
            if len(self.keyword_appearance_list) == 0:
                print("not addressed to the user")
                return True
            else:
                self.context_change_flag = True
                if self.greeting() == True:
                    # self.play_audio("Hello", "reply")
                    print("hello")
                for i in range(0, len(analysis)):
                    if analysis[i][0] in Constants.participants and analysis[i][
                        0] != self.keyword:
                        self.context_change_flag = True
                        print("context changed!")
                        self.break_flag = True
                if self.break_flag == False:
                    self.find_story(analysis, only_token_list)
                else:
                    return True
        else:
            if self.greeting() == True:
                # self.play_audio("Hello", "reply")
                print("hello")
            for i in range(0, len(analysis)):
                if analysis[i][0] in Constants.participants and analysis[i][0] != self.keyword:
                    self.context_change_flag = False
                    print("context changed!")
                    self.break_flag = True
            if self.break_flag == False:
                self.find_story(analysis, only_token_list)
            else:
                return True
        return True

    def find_question(self, analysis, only_token_list):
        quest_flag = False
        for x in Constants.interrogative_format:
            if only_token_list.find(Constants.interrogative_format[x]) != -1:
                quest_flag = True
                break
        return quest_flag

    def fetch_story(self, key_string):
        query = {"Story_number": key_string}
        collection = self.connection.story_collection
        list_of_data = collection.find(query)
        return list_of_data[0]

    def find_story(self, analysis, only_token_list):
        quest_flag = self.find_question(analysis, only_token_list)
        if quest_flag == 1:
            self.play_audio_agent("Let me see.", "gap_filler")
            # print("gap filler")
            data_string = self.get_verb_n_noun(analysis)
            self.get_comment(data_string)
            self.is_query_answered = True
            # GET DEPENDENT STORY
            #find_dependent_stories
            self.find_dependent_stories(data_string)


    def fetch_comment(self, key_string):
        now = datetime.now()
        mongodate = now.strftime("%Y-%m-%d")
        count = 0
        query1 = {"Story_id": key_string}
        collection = self.connection.comment_collection
        collection_list = []
        list_of_data = collection.find(query1)
        for item in list_of_data:
            if str(item['Date_Time']).find(mongodate) == 0:
                collection_list.append(item)
                count += 1
                # dateStr = date.strftime("%d %B %Y that is, %A at %I:%M %p")
        # count = collection.find(query1).count()
        # count = collection.find(query1,query2).count()
        return collection_list, count

    def fetch_developer(self, id):
        query = {"developer_id": id}
        collection = self.connection.developer_collection
        list_of_data = collection.find(query)
        return list_of_data[0]

    def my_dependent_story(self, story_no):
        story = self.fetch_story(story_no)
        if story['developer'] == self.role_id:
            return True
        else:
            return False

    def get_dependent_stories(self, id, story_no):
        if self.my_dependent_story(id) == True:
            sentence = "story " + story_no + " has depndency on " + id + "." + " Do you want me to tell further?"
            self.play_audio_agent(sentence, "reply")
            self.previous_text = self.text
            ans = self.conversation_loop()
            for i in Constants.yes_words:
                if ans.casefold() in i.casefold():
                    self.get_story(story_no)
                    story = self.fetch_story(id)
                    developer_id = story["developer"]
                    sentence = ""
                    developer = self.fetch_developer(developer_id)
                    sentence += " description of story " + id + " is " + "\n" + story["Story_discription"] + "."
                    # sentence += developer["Name"] + " should provide more information on this story."
                    self.play_audio_agent(sentence, "reply")
                    return
            for i in Constants.no_words:
                if ans.casefold() in i.casefold():
                    self.play_audio_agent("ok", "reply")
                    return True
            self.analyse_the_respose(ans)
            self.text = self.previous_text
            return


    def find_dependent_stories(self, story_name):
        if self.fCchange_flag == True:
            self.fCchange_flag = False
            return False
        if story_name != "" and self.verify_story_in_db(story_name) == True:
            collection = self.connection.story_collection
            querry = {"Story_name": story_name}
            cursor = collection.find(querry)
            for item in cursor:
                dep_str = item['dependent_stories']
            dependent_list = dep_str
            for item in dependent_list:
                if item == "":
                    break
                else:
                    self.play_audio_agent("do you want to know dependent stories?", 'rply')
                    ans = self.conversation_loop()
                    for i in Constants.yes_words:
                        if ans.casefold() in i.casefold():
                            self.get_dependent_stories(item, story_name)
                            return True
                    for i in Constants.no_words:
                        if ans.casefold() in i.casefold():
                            self.play_audio_agent("ok", "reply")
                            return True
                    self.analyse_the_respose(ans)
                    return True
            else: return False

    def story_description_by_keystring(self, key_string):
        collection = self.connection.story_collection
        query = {"Story_number": key_string}
        list_of_data = collection.find(query)
        for item in list_of_data:
            desc = item['Story_discription']
            gap = "description is, "
            no_update = ' No updates for the story!'
            # self.play_audio_agent(gap + desc + '.' + no_update, "reply")
            return gap + desc + '.'

    def get_comment(self, data_string):
        if data_string != "" and self.verify_story_in_db(data_string) == True:
            key_string_list = re.split('\d+', data_string)
            key_string = key_string_list[0].upper()+"_"+data_string[len(key_string_list[0]): None]
            flag, found_comment_flag = self.verify_comment(key_string)
            if flag == True and found_comment_flag == True:
                comment_item, count = self.fetch_comment(key_string)
                if count != 0:
                    sentence = self.story_description_by_keystring(key_string) + '\n'
                    sentence += Constants.story_update_part_1 + ' by agent ' + self.keyword + ' on ' + key_string + " is, "
                    for comment in comment_item:
                        sentence += "\n" + comment['Text'] + ".\n" + "(made on "
                        date = comment['Date_Time']
                        dateStr = date.strftime("%d %B %Y that is, %A at %I:%M %p")
                        sentence += dateStr
                        sentence += ')\n'
                    self.play_audio_agent(sentence, "reply")
                # sentence = self.play_audio(comment['Date_Time'],'rply')
                # self.find_dependent_stories(comment)
                # os.system("espeak '"+sentence+"'")
                # self.previous_text = self.text
                else:
                    # self.play_audio_agent("no updates for the story!", "reply")
                    collection = self.connection.story_collection
                    query = {"Story_number": key_string}
                    list_of_data = collection.find(query)
                    for item in list_of_data:
                        desc = item['Story_discription']
                        gap = "description is, "
                        no_update = ' No updates for the story!'
                        self.play_audio_agent(gap + desc + '.' + no_update, "reply")

                    #self.play_audio_agent("no updates for the story!", "reply")

                self.text = ""

            elif flag == True and found_comment_flag != True:
                # self.play_audio_agent("no updates for the story!", "reply")
                desc = self.story_description_by_keystring(key_string)
                if desc is not None:
                    self.play_audio_agent(desc + "no updates for the story!", "reply")
                else:
                    self.play_audio_agent("Could not find the story", "reply")
                    return False

            # keyword_appearance_list = list()
            else:
                sentence = "this is not " + self.keyword + "'s Story" + " "
                self.play_audio_agent(sentence, "reply")
                self.fCchange_flag = True
                self.break_flag = True
                self.context_change_flag = False
                #print("Context changed!")
                #self.context_change_flag = True
                return False
        else:
            self.play_audio_agent("Could not find the story", "reply")
            return False

    def convert(self):
        while self.count == 1:
            # self.listener()
            self.break_flag = False
            self.text = self.conversation_loop()
            lexical_analyzer = LexicalAnalyzer.LexicalAnalyzer()
            analysis, self.keyword_appearance_list, only_token_list = lexical_analyzer.analyze_and_search(
                text=self.text, keyword=self.keyword)

            if self.context_change_flag != True:
                if len(self.keyword_appearance_list) == 0:
                    print("not addressed to the user")
                    self.context_change_flag = False
                    continue
                else:
                    self.context_change_flag = True
                    if self.greeting() == True:
                        self.play_audio_agent("Hello", "reply")
                    for i in range(0, len(analysis)):
                        if analysis[i][0] in Constants.participants and analysis[i][0] != self.keyword:
                            self.context_change_flag = True
                            print("context changed!")
                            self.break_flag = True
                    if self.break_flag == False and self.greeting() != True:
                        self.find_story(analysis, only_token_list)
                    else:
                        continue
            else:
                for i in range(0, len(analysis)):
                    if analysis[i][0] in Constants.participants and analysis[i][0] != self.keyword:
                        self.context_change_flag = False
                        print("context changed!")
                        self.break_flag = True
                if self.greeting() == True and self.break_flag != True:
                    self.play_audio_agent("Hello", "reply")
                if self.break_flag == False and self.greeting() != True:
                    self.find_story(analysis, only_token_list)
                else:
                    continue
