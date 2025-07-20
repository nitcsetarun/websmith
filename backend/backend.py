import gradio as gr
from websmith import Websmith


async def setup():
    websmith = Websmith()
    await websmith.setup()
    return websmith

async def process_message(websmith, message, success_criteria, history):
    results = await websmith.run_superstep(message, success_criteria, history)
    return results, websmith
    
async def reset():
    new_websmith = Websmith()
    await new_websmith.setup()
    return "", "", None, new_websmith

def free_resources(websmith):
    print("Cleaning up")
    try:
        if websmith:
            websmith.free_resources()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="Websmith", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Websmith Personal Co-Worker")
    websmith = gr.State(delete_callback=free_resources)
    
    with gr.Row():
        chatbot = gr.Chatbot(label="Websmith", height=300, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Websmith")
        with gr.Row():
            success_criteria = gr.Textbox(show_label=False, placeholder="What are your success critiera?")
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")
        
    ui.load(setup, [], [websmith])
    message.submit(process_message, [websmith, message, success_criteria, chatbot], [chatbot, websmith])
    success_criteria.submit(process_message, [websmith, message, success_criteria, chatbot], [chatbot, websmith])
    go_button.click(process_message, [websmith, message, success_criteria, chatbot], [chatbot, websmith])
    reset_button.click(reset, [], [message, success_criteria, chatbot, websmith])

    
ui.launch(inbrowser=True)