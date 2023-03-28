import openai


def generate_response(message):
    # openai.api_key = "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"
    # prompt = "User: {}\nBot:".format(message)
    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=prompt,
    #     temperature=0.7,
    #     max_tokens=100
    #     # model="text-davinci-003",
    #     # prompt=prompt,
    #     # temperature=0.6,
    # )
    # return response.choices[0].text.strip()
    return '''
ChatGPT is an advanced language model developed by OpenAI that uses deep learning algorithms to generate human-like responses to natural language queries. While there are other language models available, some of the closest alternatives to ChatGPT include:

GPT-3: This is another language model developed by OpenAI that is larger and more advanced than ChatGPT. It has a much larger parameter space and can generate more complex and nuanced responses.

T5: This is a language model developed by Google that is capable of performing a wide range of natural language tasks, including translation, summarization, and question-answering. It is similar to ChatGPT in that it is based on a transformer architecture.

BERT: This is a language model developed by Google that is specifically designed for natural language processing tasks, such as sentiment analysis and named entity recognition. It is known for its high accuracy and has been widely adopted in the natural language processing community.

XLNet: This is a language model developed by Carnegie Mellon University and Google that is based on an autoregressive language modeling approach. It is similar to ChatGPT in that it is based on a transformer architecture and can generate coherent and contextually appropriate responses.

These language models can be used for a wide range of natural language processing tasks, including chatbot development, question-answering, and text summarization. However, each model has its own strengths and weaknesses, and the choice of model will depend on the specific task at hand.
'''
