#  import libraries
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient

# create variables for your resource key, custom endpoint, sourceUrl, targetUrl, and targetLanguage
key = '<key>'
endpoint = 'https://<your_doc_translation_resource>.cognitiveservices.azure.com/'
sourceUri = '<azure_input_storage_blob>'
targetUri = '<azure_output_storage_blob>'
targetLanguage = 'en'
sourceLanguage = 'kn'


# initialize a new instance of the DocumentTranslationClient object to interact with the asynchronous Document Translation feature
client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))

# include source and target locations and target language code for the begin translation operation
poller = client.begin_translation(sourceUri, targetUri, targetLanguage, sourceLanguage)
result = poller.result()

print('Status: {}'.format(poller.status()))
print('Created on: {}'.format(poller.details.created_on))
print('Last updated on: {}'.format(poller.details.last_updated_on))
print(
    'Total number of translations on documents: {}'.format(
        poller.details.documents_total_count
    )
)

print('\nOf total documents...')
print('{} failed'.format(poller.details.documents_failed_count))
print('{} succeeded'.format(poller.details.documents_succeeded_count))

for document in result:
    print('Document ID: {}'.format(document.id))
    print('Document status: {}'.format(document.status))
    if document.status == 'Succeeded':
        print('Source document location: {}'.format(document.source_document_url))
        print(
            'Translated document location: {}'.format(document.translated_document_url)
        )
        print('Translated to language: {}\n'.format(document.translated_to))
    else:
        print(
            'Error Code: {}, Message: {}\n'.format(
                document.error.code, document.error.message
            )
        )