import gradio as gr

countries_cities_dict = {
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Canada": ["Toronto", "Montreal", "Vancouver"],
    "Pakistan": ["Karachi", "Lahore", "Islamabad"],
}




with gr.Blocks() as demo:
    country = gr.Dropdown(list(countries_cities_dict.keys()), label="Country")
    cities = gr.Dropdown([], label="Cities")
        
    @country.change(inputs=country, outputs=cities)
    def update_cities(country):
        cities = list(countries_cities_dict[country])
        return gr.Dropdown(choices=cities, value=cities[0])



if __name__ == "__main__":
    demo.launch(server_port=8888, share=True)
