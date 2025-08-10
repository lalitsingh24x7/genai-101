def show(compiled_graph, image_name):
    try:
        img_bytes = compiled_graph.get_graph().draw_mermaid_png()
        with open(image_name, "wb") as f:
            f.write(img_bytes)
        print("Graph image saved as graph.png")
    except Exception as e:
        print(f"Exception: {e}")
        print("Error occurred while displaying the graph")
