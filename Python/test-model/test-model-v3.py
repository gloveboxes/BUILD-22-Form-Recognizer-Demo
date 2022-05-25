# Sample updated to Python SDK https://pypi.org/project/azure-ai-formrecognizer/3.2.0b4/
# pip install azure-ai-formrecognizer==3.2.0b4
# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/formrecognizer/azure-ai-formrecognizer/MIGRATION_GUIDE.md

import os
from dotenv import load_dotenv
from tabulate import tabulate

from azure.core.exceptions import ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient, DocumentModelAdministrationClient

data = []


def main():
    try:
        # Get configuration settings
        load_dotenv()
        form_endpoint = os.getenv('FORM_ENDPOINT')
        form_key = os.getenv('FORM_KEY')

        model_id = "BUILD22-Demo"

        document_analysis_client = DocumentAnalysisClient(
            endpoint=form_endpoint, credential=AzureKeyCredential(form_key))

        with open('test1.jpg', "rb") as f:
            poller = document_analysis_client.begin_analyze_document(
                model=model_id, document=f)

        result = poller.result()

        # Display key value pairs
        for idx, document in enumerate(result.documents):
            print()
            print("--------Analyzing document #{}--------".format(idx + 1))
            print("Document has type {}".format(document.doc_type))
            print("Document has document type confidence {}".format(
                document.confidence))
            print("Document was analyzed with model with ID {}".format(
                result.model_id))
            print()
            for name, field in document.fields.items():
                field_value = field.value if field.value else field.content
                if field.value_type != 'list':
                    data.append([name, field.value, field.confidence])

        data.sort()
        print(tabulate(data, headers=[
              'Label', 'Value', 'Confidence'], tablefmt='fancy_grid'))

        # Display table data
        for i, table in enumerate(result.tables):

            row_index = 1
            hdr = []
            rows = []
            row = []

            print("\nTable {} can be found on page:".format(i + 1))
            # for region in table.bounding_regions:
            #     print("...{}".format(i + 1, region.page_number))

            for cell in table.cells:
                if cell.row_index == 0:
                    hdr.append(cell.content)
                else:
                    if row_index != cell.row_index:
                        rows.append(row)
                        row_index = cell.row_index
                        row = []

                    row.append(cell.content)

            rows.append(row)
            print(tabulate(rows, headers=hdr, tablefmt='fancy_grid'))

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
