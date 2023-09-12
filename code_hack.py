import streamlit as st
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel                       
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2


PAT = st.secrets['pat']
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)


with st.sidebar:
    types = st.radio('Select from below', ['Imitation👅', 'Genre Translator📜', 'Story Mimic📝'])

    models = {'GPT-4' : ['openai', 'chat-completion', 'ad16eda6ac054796bf9f348ab6733c72'], 
              'llama2-70b-chat' : ['meta', 'Llama-2', '6c27e86364ba461d98de95cddc559cb3'],
              'text-bison' : ['gcp', 'generate', '575fc5e15d53487e99d5de038d178171'],
              'falcon-40b-instruct' : ['tiiuae', 'falcon', '1f704e8d43d949348fbf5f9b8cecfca8'], 
              'GPT-3_5-turbo' : ['openai', 'chat-completion', '8ea3880d08a74dc0b39500b99dfaa376']}


    model_id = st.selectbox('Select Your Model', ['GPT-4', 'llama2-70b-chat', 'text-bison', 'falcon-40b-instruct', 'GPT-3_5-turbo'])
    user_id = models[model_id][0]
    app_id = models[model_id][1]
    model_ver_id = models[model_id][2]

    st.markdown("<hr>", unsafe_allow_html=True)

    user_pat = st.text_input('Enter Your PAT ID', placeholder="Optional untill hackathon ends")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.write("Don't have get one make sure you create an account first https://clarifai.com/settings/security")


st.markdown("<h1 style='text-align: centre; color: red;'>ImitAIte</h1>",
                unsafe_allow_html=True)


def get_imitation_response():
    if "messages" not in st.session_state.keys(): 
        st.session_state.messages = [
            {"role": "assistant", "content": "Example : You are ertugrul ghazi and you are standing with your tribe at the gates of crusader's castle what will you say?"}
        ]

    if prompt := st.chat_input("Describe scenario"): 
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages: 
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if not prompt:
        return ''

    RAW_TEXT2 = '''You are expert in Imitating, Assume all queries to be in context of providing imitation of a celebrity or a human''' + '''\nIf given query is not about imitation a person except for greeting reject it and say I'm sorry I can't assist with something differnt from Imitating \n''' +"You could also be given a scenario saying you're this particular person and a situation will be given how will you respond\n" +  '\nQUERY : \n\n' + prompt

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Mimicking..."):
    
                userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

                post_model_outputs_response = stub.PostModelOutputs(
                service_pb2.PostModelOutputsRequest(
                    user_app_id=userDataObject, 
                    model_id=model_id,
                    version_id=model_ver_id, 
                    inputs=[
                        resources_pb2.Input(
                            data=resources_pb2.Data(
                                text=resources_pb2.Text(
                                    raw=RAW_TEXT2
                                    )
                                )
                            )
                        ]
                    ),
                    metadata=metadata
                )

                if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
                    st.error(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

                output = post_model_outputs_response.outputs[0]

                lines = output.data.text.raw

                message = {"role": "assistant", "content": lines}
                st.session_state.messages.append(message)

                return lines


def genre_changer():
    if "session_state" not in st.session_state.keys():
        st.session_state.session_state = [
            {"role": "assistant", "content": "Example : 'My frustration boiled over, and I couldn't help but snap at them' change this sentence to joyful expression"}
        ]

    session_state = st.session_state.session_state

    if prompt := st.chat_input("Your question"):
        session_state.append({"role": "user", "content": prompt})

    for message in session_state:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if not prompt:
        return ''

    RAW_TEXT2 = '''You are expert in Genre Traslator, Assume all queries to be in context of providing Translation of a genre sentence into another''' + '''\nIf given query is not about genre translator reject it except for greeting and say I'm sorry I can't assist with something different from Genre translator \n''' + '\nQUERY : \n\n' + prompt

    if session_state[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Changing..."):
    
                userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

                post_model_outputs_response = stub.PostModelOutputs(
                    service_pb2.PostModelOutputsRequest(
                        user_app_id=userDataObject, 
                        model_id=model_id,
                        version_id=model_ver_id, 
                        inputs=[
                            resources_pb2.Input(
                                data=resources_pb2.Data(
                                    text=resources_pb2.Text(
                                        raw=RAW_TEXT2
                                    )
                                )
                            )
                        ]
                    ),
                    metadata=metadata
                )

                if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
                    st.error(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

                output = post_model_outputs_response.outputs[0]

                lines = output.data.text.raw

                message = {"role": "assistant", "content": lines}
                session_state.append(message)

                return lines


def story_mimic():
    if "story" not in st.session_state.keys():
        st.session_state.story = [
            {"role": "assistant", "content": "Example(After uploading a horror content) : 'How would the story change if Mr.Bean had written it 🤣"}
        ]

    session_state = st.session_state.story

    file = st.file_uploader("Upload a text document consisting of script")

    if not file:
        return ''
    
    f_type = file.name.split('.')[1]
    if f_type != 'txt':
        st.error('Upload only text documents')
        return ''

    
    file_bytes = file.read()

    
    if prompt := st.chat_input("Your Prompt"):
        session_state.append({"role": "user", "content": prompt})


    for message in session_state:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if not prompt:
        return ''


    file_bytes = str(file_bytes)
    RAW_TEXT2 = '''As an expert in altering the semantics of a scene or story while keeping the core narrative intact, your task is to transform the tone of a given story or scene to match that of a celebrity or a provided human persona go sarcastic if possible at any moment. Please note that I will only accept queries related to altering the semantics of a story or scene to align with a celebrity or human persona. For all other inquiries, except for greetings, I will respond by saying, 'I'm sorry, I can't assist with something different from Story Mimicking.\n\n''' +'generate answer as if that particular personality has written it\n'+  'STORY : \n' + file_bytes + '\n\nQUERY : \n' + prompt + '\nalso return the dialogues of celebrity or human peersona'

    if session_state[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Translating..."):
    
                userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)

                post_model_outputs_response = stub.PostModelOutputs(
                    service_pb2.PostModelOutputsRequest(
                        user_app_id=userDataObject, 
                        model_id=model_id,
                        version_id=model_ver_id, 
                        inputs=[
                            resources_pb2.Input(
                                data=resources_pb2.Data(
                                    text=resources_pb2.Text(
                                        raw=RAW_TEXT2
                                    )
                                )
                            )
                        ]
                    ),
                    metadata=metadata
                )

                if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
                    st.error(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

                output = post_model_outputs_response.outputs[0]

                lines = output.data.text.raw

                message = {"role": "assistant", "content": lines}
                session_state.append(message)

                return lines


    

if types == 'Imitation👅':
    imitate = get_imitation_response()
    st.write(imitate)

elif types == 'Genre Translator📜':
    genre = genre_changer()
    st.write(genre)

elif types == 'Story Mimic📝':
    story = story_mimic()
    st.write(story)


