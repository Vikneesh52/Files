import gradio as gr
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Replace these with your actual Azure Storage account credentials
connection_string = "YOUR_CONNECTION_STRING"
container_name = "YOUR_CONTAINER_NAME"
folder_path = "YOUR_FOLDER_PATH"  # e.g. "documents/" or empty string for root

def list_blobs(folder_prefix=""):
    """List all blobs in the specified folder"""
    try:
        # Create the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get the container client
        container_client = blob_service_client.get_container_client(container_name)
        
        # Use folder_path combined with any additional folder prefix passed to the function
        full_prefix = os.path.join(folder_path, folder_prefix).replace("\\", "/")
        
        # List blobs with the prefix
        blob_list = container_client.list_blobs(name_starts_with=full_prefix)
        
        # Extract only file names (without the full path)
        files = []
        for blob in blob_list:
            # Only add it if it's not a folder (no trailing slash)
            if not blob.name.endswith('/'):
                files.append(blob.name)
        
        return files, None
    except Exception as e:
        return [], f"Error: {str(e)}"

def summarize_file(file_path):
    """Placeholder function for file summarization"""
    # This is just a placeholder - you'll implement actual summarization later
    if not file_path:
        return "No file selected for summarization."
    return f"The file '{file_path}' is being summarized. This is where your summarization logic will go."

# Create the Gradio interface
with gr.Blocks(title="Azure Blob Storage File Explorer") as demo:
    gr.Markdown("# Azure Blob Storage File Explorer")
    gr.Markdown("Browse and summarize files from your Azure Blob Storage container.")
    
    with gr.Row():
        with gr.Column(scale=1):
            folder_input = gr.Textbox(label="Subfolder (optional)", placeholder="Enter subfolder path or leave empty")
            list_btn = gr.Button("List Files")
            
            # Using a Radio component rather than checkboxes since we need to select one file at a time
            file_radio = gr.Radio(label="Select a file", choices=[], interactive=True)
        
        with gr.Column(scale=2):
            summarize_btn = gr.Button("Summarize Selected File", interactive=False)
            summary_output = gr.Textbox(label="Summary", lines=10, interactive=False)
    
    # Connect the components with functions
    def update_file_list(folder):
        files, error = list_blobs(folder)
        if error:
            return [], error, False
        
        if not files:
            return [], "No files found in this location.", False
        
        return files, "", False
    
    list_btn.click(
        fn=update_file_list,
        inputs=[folder_input],
        outputs=[file_radio, summary_output, summarize_btn]
    )
    
    # Enable summarize button when a file is selected
    def update_button_state(selected):
        return selected is not None and selected != ""
    
    file_radio.change(
        fn=update_button_state,
        inputs=[file_radio],
        outputs=[summarize_btn]
    )
    
    # Summarize the selected file
    summarize_btn.click(
        fn=summarize_file,
        inputs=[file_radio],
        outputs=[summary_output]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()