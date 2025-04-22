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
            # Remove the folder prefix to get just the filename
            relative_path = blob.name[len(full_prefix):] if blob.name.startswith(full_prefix) else blob.name
            # Only add it if it's not an empty string and not a folder (no trailing slash)
            if relative_path and not relative_path.endswith('/'):
                files.append(blob.name)
        
        return files, None
    except Exception as e:
        return [], f"Error: {str(e)}"

def summarize_file(file_path):
    """Placeholder function for file summarization"""
    # This is just a placeholder - you'll implement actual summarization later
    return f"The file '{file_path}' is being summarized. This is where your summarization logic will go."

# Create the Gradio interface
with gr.Blocks(title="Azure Blob Storage File Explorer") as demo:
    gr.Markdown("# Azure Blob Storage File Explorer")
    gr.Markdown("Browse and summarize files from your Azure Blob Storage container.")
    
    with gr.Row():
        with gr.Column(scale=1):
            folder_input = gr.Textbox(label="Subfolder (optional)", placeholder="Enter subfolder path or leave empty")
            list_btn = gr.Button("List Files")
            file_list = gr.Radio(label="Files", choices=[], interactive=True)
        
        with gr.Column(scale=2):
            summarize_btn = gr.Button("Summarize Selected File", interactive=False)
            summary_output = gr.Textbox(label="Summary", lines=10, interactive=False)
    
    # Connect the components with functions
    list_btn.click(
        fn=list_blobs,
        inputs=[folder_input],
        outputs=[file_list, summary_output]
    )
    
    # Enable the summarize button when a file is selected
    file_list.change(
        fn=lambda x: gr.Button.update(interactive=True if x else False),
        inputs=file_list,
        outputs=summarize_btn
    )
    
    # Summarize the selected file
    summarize_btn.click(
        fn=summarize_file,
        inputs=[file_list],
        outputs=[summary_output]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()