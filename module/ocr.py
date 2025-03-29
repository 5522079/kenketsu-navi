import os
import re
import csv
import pickle # テスト用
import datetime

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest


load_dotenv()

endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
model_id = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID')

target_file_path = "../data/sample03.pdf"
output_file_path = "../data/BloodDonation.csv"

def ocr():
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(target_file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            model_id=model_id, 
            body=f
        )
        result = poller.result()
    return result

###### テスト用 ######
def save_test_result(result):
    with open("../output/test_result.pkl", "wb") as result_file:
        pickle.dump(result, result_file)
        print("resultをtest_result.pklに保存しました")

def load_test_result(file_path="../output/test_result.pkl"):
    with open(file_path, "rb") as result_file:
        return pickle.load(result_file)
###### テスト用 ######

def write_to_csv(documents, output_file=output_file_path):
    now = datetime.datetime.today()
    year, month = str(now.year), str(now.month-1)
    rows = []

    for document in documents:
        for prefecture_id, field in document.fields.items():
            tmp = str(field.content).replace('"', '').replace(',', '').replace('\n', ',').replace(' ', ',')
            tmp = re.sub(r'[^0-9,]', '', tmp)
            donor = [int(value) for value in tmp.split(',') if value.strip()]
            donor = donor[:7] + [0] * (7 - len(donor[:7]))  # 欠損値の処理
            rows.append([year, month, prefecture_id] + donor)

    rows.sort(key=lambda x: int(x[2])) # x[2] = prefecture_id

    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)

if __name__ == "__main__":
    result = ocr()
    ###### テスト用 ######
    #save_test_result(result)
    #result = load_test_result()
    ###### テスト用 ######
    write_to_csv(result.documents)