''' 
******************************************************************
MY AI - Author: Rob Braxman
(c) Copyright Braxmobile 20204
License GPL 3.0
******************************************************************

'''
import ollama
import os
import textwrap
import time

#Update this list your favorite models
#this is the official ollama spellings
model_list = [
   'llama3',
   'gemma2',
   'llava',
   'qwen2',
   'phi3:medium',
   'codellama',
   'dolphin-llama',
             ]
#specify which model is to be used as the multimodal
#(image processing) model
multimodal_model = "llava"


global icontext
global isystem
global imodel
global isystemname
global basepath 
global itemp
global FirstLoad
global ContextCount
from datetime import datetime

# Ansi color codes
BOLD = '\033[1m'
COLORFUL = '\033[92m'  # bluegreen
BACK_TO_NORMAL = '\033[0m'

global PromptCount 

#Change this to your desired folders
basepath = "/home/worker/Documents/vscode-test/"

pathimage = basepath+"images/"
pathlog = basepath+"logs/"
pathtext = basepath+"text/"
pathcontext = basepath+"context/"


def make_dirs():
    try:
      os.mkdir(pathimage)
    except Exception as e:
      None

    try:
      os.mkdir(pathlog)
    except Exception as e:
      None

    try:
      os.mkdir(pathtext)
    except Exception as e:
      None


    try:
      os.mkdir(pathcontext)
    except Exception as e:
      None





def select_action():
    global imodel
    os.system("cls||clear")

    print(BOLD+COLORFUL+" WELCOME TO MyAI\n"+BACK_TO_NORMAL+COLORFUL)
    i1 = 0
    for model in model_list:
        i1+=1
        print(" "+str(i1)+". Load "+model)
    
    print("")
    print(" T. Fine Tune (Session Only)")
    print(" X. Exit\n")
    iselect = input( COLORFUL+" Enter Action ==> "+BACK_TO_NORMAL)

    if(iselect.lower()=='t'):
      imodel = "T"
    elif(iselect.lower()=='x' or iselect==''):
      imodel = "X"
    elif(int(iselect)>0 and int(iselect)<6 ):
      imodel = model_list[int(iselect)-1]
    else:
      imodel = ''
    return imodel





def ask_image(input_string):
    # Convert the input string to lower case for case-insensitive search
    input_string_lower = input_string.lower()

    # Check if '/image' is found in the input string (case-insensitive)
    if '/image' in input_string_lower:
        # If found, return True and remove '/image' from the original string
        return True    
    else:
        # If not found, return False and keep the original string unchanged
        return False
    




def ask_context(input_string):
    # Convert the input string to lower case for case-insensitive search
    input_string_lower = input_string.lower()

    # Check if '/image' is found in the input string (case-insensitive)
    if '/c' in input_string_lower:
        # If found, return True and remove '/text' from the original string
        return True    
    else:
        # If not found, return False and keep the original string unchanged
        return False




def ask_help():
      
      global FirstLoad 
      
      helpinfo =  COLORFUL+BOLD+"\n MULTI-LINE ENTRY\n"+BACK_TO_NORMAL+COLORFUL 
      helpinfo += COLORFUL+"\n 'Ask "+isystemname+ " a question?'\n"
      helpinfo +=  "\n The above prompt allows entry of multiple lines of text."
      helpinfo += "\n The data will be sent when a blank line is entered."
      helpinfo += "\n This means you have to hit Enter twice at the end.\n"
      helpinfo +=  BOLD+"\n ADDITIONAL COMMANDS\n"+BACK_TO_NORMAL+COLORFUL 
      helpinfo += "\n Additional Commands: /i Image, /c Context, /x Erase Context\n"
      helpinfo += "\n "+BOLD+"/i Image, /c Context"+BACK_TO_NORMAL+COLORFUL
      helpinfo += "\n Depending on the model you can tell the AI that you"
      helpinfo += "\n will be uploading an image (/i) or add context "
      helpinfo += "\n (/c) by uploading a text file.\n"

      helpinfo += "\n "+BOLD+"/x Erase context"+BACK_TO_NORMAL+COLORFUL
      helpinfo += "\n /x clear clear screen and clear context cache\n"+BACK_TO_NORMAL
      helpinfo += "\n "+COLORFUL+BOLD+"/r Redo entry"+BACK_TO_NORMAL+COLORFUL
      helpinfo += "\n /r Clear the current entry and start again\n"+BACK_TO_NORMAL

      FirstLoad = True
   
      print(helpinfo)
      input(COLORFUL+"\n Press Enter to continue."+BACK_TO_NORMAL)
      return ""






def ask_ai(client ):
    global icontext
    global isystem
    global imodel
    global itemp
    global FirstLoad
    global ContextCount

    if(FirstLoad):
       #ask_help()
       #input(COLORFUL+" Press Enter to Continue..."+BACK_TO_NORMAL)
       os.system("cls||clear")
  
    imagefile = ''
    icontext_purpose = ''

    #PROMPT ===========================================================================================
    print(COLORFUL+" Ask "+isystemname+ " a question? (/? Help) "+BACK_TO_NORMAL)

    if(FirstLoad == True):
      print(COLORFUL+"\n -- TIPS:")
      print(COLORFUL+" -- /c upload a context "+BACK_TO_NORMAL)

      if(imodel == multimodal_model):
        print(COLORFUL+" -- /i upload an image "+BACK_TO_NORMAL)

      print(COLORFUL+" -- /x erase the context "+BACK_TO_NORMAL)
      print(COLORFUL+" -- /r redo entry"+BACK_TO_NORMAL)
      print(COLORFUL+" -- /bye to exit "+BACK_TO_NORMAL)
      print(COLORFUL+" -- Multiline entry. Hit "+BOLD+"Enter 2X"+BACK_TO_NORMAL+COLORFUL+" to send "+BACK_TO_NORMAL)
       
    FirstLoad = False

    
    try:
      lines = []
      while True:
          
          line = input(" ")
          if line:  # Check if the line is not blank
              lines.append(line)
          else:
              break
          
          line = line.lower()
          if(line == '/?'):
             break;
          if(line == '/bye'):
             break;
          if(line == '/x'):
             break;
             break;
          if(line == '/c'):
             break;
          if(line == ''):
             break;
          if(line == '/r'):
             return(" ....")
             break;
    
          
    except Exception as e:
      print(' Error '+e)
      #exit()
      
    iprompt = ' '.join(lines).lstrip()
    #if('/bye' == iprompt.lower() ):
    #  return("")
    
    if '/?' == iprompt.lower():
       ask_help()
       return " ..."   

    if '' == iprompt:
       if(is_yn(COLORFUL+"\n Exit? (y/n) ==> "+BACK_TO_NORMAL)=='y'):
          return ""
       #os.system('cls||clear')
       return " "   

    is_checkpoint = False
    if(iprompt.lower()=="/bye"):
      if(PromptCount > 1 and is_yn(COLORFUL+"\n Save current context? (y/n) ==> "+BACK_TO_NORMAL)=='y' ):
        iprompt = "Create a conversation summary in JSONL format. Only include words that are the minimum required to restore context. This will be used to restore the conversation at a later time. Do not add any other commentary. "
        is_checkpoint = True
      else: 
        return " " 

    if(iprompt.lower()=="/x"):
      #os.system("cls||clear")
      if(PromptCount > 1):
        icontext=""
        iprompt = "Clear the current context. Respond only with: Context Cleared"


    
    is_image = ask_image(iprompt)
    if(is_image):
       iprompt = iprompt.replace('/i', '')

    is_text = ask_context(iprompt)
    if(is_text):
       iprompt = iprompt.replace('/c', '')



    # MULTIMODAL ====================================================================
    # MULTIMODAL ====================================================================
    # MULTIMODAL ====================================================================
    if(is_image and imodel==multimodal_model):
      input_prompt  = COLORFUL+"\n UPLOAD AN IMAGE"
      input_prompt += "\n -- Reading from "+pathimage+"\n -- /x to cancel upload.\n -- Enter Filename ==> "+BACK_TO_NORMAL

      imagefile = get_file_name(input_prompt, pathimage, 1)

    if(is_image and imodel!=multimodal_model):
      print(' Model '+imodel+' is not multimodal. Select a different model. ')
      iprompt = " Please ask again..."
      return iprompt
    
    if(imagefile!=''):
      imagefile = pathimage + imagefile
      neuralhash = imagefile + ".neural.txt"



    # RAG/CONTEXT ====================================================================
    # RAG/CONTEXT ====================================================================
    # RAG/CONTEXT ====================================================================
    icontext_text = ''
    if(is_text):
      input_prompt  = COLORFUL+"\n UPLOAD A CONTEXT TEXT FILE"
      input_prompt += "\n -- Reading from "+pathcontext
      input_prompt += "\n -- Must be a text file."
      input_prompt += "\n -- /x to cancel upload."
      input_prompt += "\n -- /l to load last context."
      input_prompt += "\n -- Enter Filename  ==> "+BACK_TO_NORMAL


      icontextfile = get_file_name(input_prompt, pathcontext, 2)
      if(icontextfile == ''):
        print('\n')
        return(" ")
      with open(pathcontext+icontextfile,'r') as f:
        icontext_text = f.read()

      #context instructions  
      if(icontext_text.lstrip()!=''):
        if(ContextCount == 0):
           icontext_purpose = "The following text is the initial context. "
        else:
           icontext_purpose = "Append the following text to the current context. "
        ContextCount +=1
  

    current_datetime = datetime.now()
    idate = f"For context, if relevant, current date and time is {current_datetime.date()} {current_datetime.time()}. "

    itemp_text = ""
    #if(itemp!=0.5):
    #  itemp_text = "Set the temperature to "+str(itemp)+". "
    
    try:

      promptmodified  = "Context: ''' "
      promptmodified += icontext_purpose
      promptmodified += " "+icontext_text+" "
      promptmodified += idate+itemp_text+"  ''' "

      if(iprompt =='' and icontext_text!=''):
         promptmodified += " Do not acknowledge. Actual Prompt will follow later. Prompt: None "

      if(iprompt!=''):
        promptmodified += "Prompt: "
        promptmodified += iprompt

    except Exception as e:
      print(" -- Context File is not in a valid format.")
      return ""

    #print('\n Context: '+icontext_text+' '+idate+'\n')

    print("\n "+COLORFUL+"-- Other commands:  /h help /c context /x clear-context /r redo-entry /bye"+BACK_TO_NORMAL)
    print(" "+COLORFUL+"Thinking...Please wait.\n"+BACK_TO_NORMAL)


    #GENERATE ===================================================================
    try:
      if( imagefile!=''):
        response = client.generate(model=imodel, prompt=promptmodified,context=icontext,system=isystem,images=[imagefile])
      else:
        response = client.generate(model=imodel, prompt=promptmodified,context=icontext,system=isystem)

      #RESPONSE HANDLING ===================================================================
      icontext = response['context']
      #reset to normal and drive it via context
      isystem = ''
    
      #DO NOT Print response if context only
      if(iprompt.lstrip()!=''):
        formatted_text = BOLD+format_output(response['response'])+BACK_TO_NORMAL
      else:
        formatted_text = BOLD+"Context Accepted"+BACK_TO_NORMAL

      print('\n')
      print(formatted_text)
      print(COLORFUL+'\n Context Token Count: '+str(len(icontext))+BACK_TO_NORMAL)

      #Save Results to File
      #-------------------------------------------------------------------------------
      if(imodel == multimodal_model and is_image):
          neuralhashtext = textwrap.fill(response['response'], width=40)
          f = open(neuralhash, "w")
          f.write(neuralhashtext)
          f.close()

      if(is_checkpoint == True):    
          save_context(response['response'])
          #ext after
          return("")
      if(is_checkpoint == False):
          save_query(response['response'], icontext_text, iprompt, imagefile )       
      #-------------------------------------------------------------------------------


    except ollama.ResponseError as e:
      #generate ERROR =================================================
      print(' Error:', e.error)
    
      if e.status_code == 404:
        exit()
    return("\n ***")



def save_query(response,icontext_text,iprompt,imagefile ):
      global PromptCount
      if(iprompt==''):
         return

      querylog = pathlog + "query-"+str(int(time.time())) + '.log'
      querylog_text = format_log(imodel, icontext_text,iprompt,response,imagefile)
      f = open(querylog, "w")
      f.write(querylog_text)
      f.close()
      PromptCount += 1



def save_context(response):
    #save context upon exit
    querylog = ''
    if(response == ''):
       return
    while('.txt' not in querylog):
        querylog = input(COLORFUL+" Enter a filename (.txt) for the context summary ==> "+BACK_TO_NORMAL)
        if('.txt' not in querylog):
            querylog += ".txt"
        querylog = pathcontext + querylog.replace(" ","-").lower()
    #querylog_text = format_log(imodel, icontext_text,iprompt,response['response'],imagefile)
    f = open(querylog, "w")
    f.write(response)
    f.close()

    lastlog = pathcontext +"_last"
    f = open(lastlog, "w")
    f.write(response)
    f.close()
    os.system("cls||clear")

    return



def format_log(model, context, prompt, response, imagefile):
   
   context_clean = context.replace("  ","").lstrip()
   prompt_clean = prompt.replace("  ","").lstrip()

   output = "Model "+imodel
   output = output + "\nPrompt: "+prompt_clean

   if(context_clean!=''):
      output = output + "\nContext: "+context_clean

   output = output + "\n\nResponse: "+response

   if(imagefile.lstrip()!=''):
      output = output + "\n\nImage: "+imagefile
   return output



def is_yn(prompt):
      while True:
          status = input(prompt)
          if(status.lower()=='y' or status.lower()=='n'):
             break
      return status.lower()


def get_file_name(prompt,path, style):
      while True:
          filename = input(prompt)
          if(filename== '/x'):
             return ""
          elif(filename == '/l'):
             return("_last")
          elif(filename == ''):
             None
          elif os.path.exists(path+filename):
              return filename
          else:
              print(" File not found in "+path+". Please try again.")




def format_output(text):
    lines = text.splitlines()
    wrapped_lines = [textwrap.fill(line,width=80) for line in lines]
    formatted_text = '\n'.join([' ' * 2 + line for line in wrapped_lines])
    return formatted_text




def set_aisystem():
    global isystem
    global isystemname
    global itemp


    irole = input(COLORFUL+'\n Who will the AI be (Role)? Blank for Default Assistant? ==> '+BACK_TO_NORMAL)

    if(irole !=''):
      isystem = "You are "+irole+". "
      isystemname = irole.title()

    iroleplus = input(COLORFUL+' Additional Role Instructions (blank for none) ==> '+BACK_TO_NORMAL)
    #itemp = input(' Creative Temperature (between 0 - 2, blank for default .5) ==> ')

    isystem = isystem + " " + iroleplus
    #if(itemp =='' or float(itemp)<0 or float(itemp)>2):
    #   itemp = 0.5

    imodel = ''






#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

os.system('cls||clear')

#Make Dirs if NotExist
make_dirs()

#Initialize Model
imodel = ''
icontext = ''
isystemname = 'AI Assistant'
isystem = 'you are'+isystemname
FirstLoad = True
PromptCount = 0
ContextCount = 0
#itemp = 0.5

while(imodel == ""):

  imodel = select_action()

  if(imodel == 'T' or imodel=='t'):
    set_aisystem()
    imodel = '' #loop back

  if(imodel == 'X'):
    print(" Bye for now.")
    exit()  

os.system("cls||clear")
print(" Starting "+imodel+ " as "+isystemname+"\n")
#print(" Model Parameters: "+isystem)

from ollama import Client
client = Client(host='http://localhost:11434')

status = 'start';
while (status!=""):

  try:
    status = ask_ai(client)
  except Exception as e:
     print("Error AskAi "+e)

  if(status!="" and status!=" "):
    print(status)
  
os.system("cls||clear")
print(' Bye for now. --'+isystemname+"\n\n\n\n")
exit()

'''
Dependency Summary
sudo apt install python3-pip
pip install ollama
pip install textwrap
pip install time

To match the models here download the models as follows
ollama pull llama3
ollama pull llava
ollama pull phi3:medium
ollama pull codellama
ollama pull dolphin-llama3
'''
