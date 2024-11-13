def verify_graph_structure(init_graph):
    # Required fields for nodes and valid keys for obj_transform
    required_node_fields = ['id', 'class_name', 'category', 'obj_transform']
    valid_obj_transform_keys = ['position', 'rotation', 'scale']

    print("Verifying nodes...")
    for node in init_graph['nodes']:
        # Check if all required fields are present
        missing_fields = [field for field in required_node_fields if field not in node]
        if missing_fields:
            print(f"Node ID {node.get('id', 'Unknown')} is missing fields: {missing_fields}")
            continue  # Skip further checks if fields are missing
        
        # Check obj_transform structure
        obj_transform = node['obj_transform']
        if not isinstance(obj_transform, dict):
            print(f"Node ID {node['id']} has invalid obj_transform data: {obj_transform}")
        else:
            # Ensure obj_transform contains valid keys
            missing_transform_keys = [key for key in valid_obj_transform_keys if key not in obj_transform]
            if missing_transform_keys:
                print(f"Node ID {node['id']} has an incomplete obj_transform: missing {missing_transform_keys}")

            # Validate position, rotation, and scale data
            for key in valid_obj_transform_keys:
                if key in obj_transform:
                    if key == 'rotation' and len(obj_transform[key]) != 4:  # Rotation should have 4 elements (quaternion)
                        print(f"Node ID {node['id']} has invalid {key}: {obj_transform[key]}")
                    elif key != 'rotation' and len(obj_transform[key]) != 3:  # Position and scale should have 3 elements
                        print(f"Node ID {node['id']} has invalid {key}: {obj_transform[key]}")

    # Check edges
    print("Verifying edges...")
    node_ids = {node['id'] for node in init_graph['nodes']}
    for edge in init_graph['edges']:
        if edge['from_id'] not in node_ids:
            print(f"Edge 'from_id' {edge['from_id']} references an invalid node ID.")
        if edge['to_id'] not in node_ids:
            print(f"Edge 'to_id' {edge['to_id']} references an invalid node ID.")
        if 'relation_type' not in edge:
            print(f"Edge from {edge['from_id']} to {edge['to_id']} is missing 'relation_type'.")

    print("Verification complete.")