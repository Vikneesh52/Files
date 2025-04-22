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
        
        # Return formatted list of files
        return files
    except Exception as e:
        return [f"Error: {str(e)}"]

def summarize_file(file_path):
    """Placeholder function for file summarization"""
    # This is just a placeholder - you'll implement actual summarization later
    return f"The file '{file_path}' is being summarized. This is where your summarization logic will go."

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Azure Blob Storage File Explorer")
    gr.Markdown("Browse and summarize files from your Azure Blob Storage container.")
    
    # First get the list of files
    with gr.Row():
        folder_input = gr.Textbox(label="Subfolder (optional)", placeholder="Enter subfolder path or leave empty")
        list_btn = gr.Button("List Files")
    
    # Display the files in a simple list
    file_display = gr.Textbox(label="Available Files", lines=10, interactive=False)
    
    # File selection
    selected_file = gr.Textbox(label="Enter the file name to summarize", placeholder="Copy and paste a filename from above")
    
    # Summarization
    with gr.Row():
        summarize_btn = gr.Button("Summarize Selected File")
        clear_btn = gr.Button("Clear")
    
    summary_output = gr.Textbox(label="Summary", lines=10, interactive=False)
    
    # Connect the components
    def display_files(folder):
        files = list_blobs(folder)
        if not files:
            return "No files found."
        return "\n".join(files)
    
    list_btn.click(
        fn=display_files,
        inputs=[folder_input],
        outputs=[file_display]
    )
    
    # Clear function
    def clear_outputs():
        return "", ""
    
    clear_btn.click(
        fn=clear_outputs,
        inputs=[],
        outputs=[selected_file, summary_output]
    )
    
    # Summarize button
    summarize_btn.click(
        fn=summarize_file,
        inputs=[selected_file],
        outputs=[summary_output]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()