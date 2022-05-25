import os
from dotenv import load_dotenv
from tabulate import tabulate

from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

data = []

def main():

    try:

        # Get configuration settings
        load_dotenv()
        form_endpoint = os.getenv('FORM_ENDPOINT')
        form_key = os.getenv('FORM_KEY')

        # Create client using endpoint and key
        form_recognizer_client = FormRecognizerClient(form_endpoint, AzureKeyCredential(form_key))

        # Model ID from when you trained your model.
        model_id = os.getenv('MODEL_ID')
        model_id = "build-demo"

        # Test trained model with a new form
        with open('test1.jpg', "rb") as f:
            poller = form_recognizer_client.begin_recognize_custom_forms(
                model_id=model_id, form=f)

        result = poller.result()

        for recognized_form in result:
            print("Form type: {}".format(recognized_form.form_type))
            for name, field in recognized_form.fields.items():
                data.append([field.label_data.text if field.label_data else name, field.value, field.confidence])

        data.sort()
        print(tabulate(data, headers=['Label', 'Value', 'Confidence'], tablefmt='fancy_grid'))

    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()