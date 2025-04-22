import gradio as gr
from azure.storage.blob import BlobServiceClient

# Azure Blob Storage connection
AZURE_CONNECTION_STRING = "your_connection_string"
CONTAINER_NAME = "your_container_name"
FOLDER_NAME = "your/folder/path/"  # if nested, else just leave as "" for root

# Connect to Azure
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# List blobs in the specified folder
def list_blob_files():
    blob_list = container_client.list_blobs(name_starts_with=FOLDER_NAME)
    file_names = [blob.name for blob in blob_list if not blob.name.endswith("/")]
    return file_names

# Placeholder summarization function
def on_file_click(file_name):
    return f"Summarizing file: {file_name}..."

# Interface
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# 📂 Azure Blob File Summarizer")

        file_list_output = gr.Column()
        message_output = gr.Textbox(label="Summary Status", interactive=False)

        def refresh_files():
            files = list_blob_files()
            file_buttons = []
            file_list_output.children.clear()
            for file in files:
                file_button = gr.Button(file)
                file_button.click(fn=on_file_click, inputs=[], outputs=message_output, _js=None).then(
                    lambda f=file: on_file_click(f), inputs=[], outputs=message_output
                )
                file_list_output.append(file_button)

        refresh_btn = gr.Button("🔄 Refresh File List")
        refresh_btn.click(fn=refresh_files, inputs=[], outputs=[])

        refresh_files()  # initial load

    return demo

demo = create_interface()
demo.launch()
