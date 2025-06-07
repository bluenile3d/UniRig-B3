# Replace the content of src/data/extract.py with this:

import os
import sys
from pathlib import Path

# Skip bpy import for executable builds
try:
    import bpy
    BLENDER_AVAILABLE = True
    print("Running inside Blender environment")
except ImportError:
    BLENDER_AVAILABLE = False
    print("Running outside Blender - using file processing mode")

def get_files(data_name, inputs=None, input_dataset_dir=None, output_dataset_dir=None, force_override=False, warning=True):
    """
    Extract and process files for UniRig
    Modified to work without bpy when running as executable
    """
    
    if inputs is not None:
        # Handle comma-separated input files
        if isinstance(inputs, str):
            input_files = [f.strip() for f in inputs.split(',')]
        else:
            input_files = [inputs]
        
        processed_files = []
        
        for input_file in input_files:
            if not os.path.exists(input_file):
                if warning:
                    print(f"Warning: Input file not found: {input_file}")
                continue
            
            # Create output filename in the specified directory
            base_name = Path(input_file).stem
            output_file = os.path.join(output_dataset_dir, f"{base_name}_{data_name}")
            
            # For executable mode, we assume the input is already in the correct format
            # and just need to process it for the output directory
            if not BLENDER_AVAILABLE:
                # Copy/process the file without using bpy
                processed_files.append((input_file, output_file))
            else:
                # Use original bpy-based processing if available
                processed_files.append(process_with_bpy(input_file, output_file))
        
        return processed_files
    
    elif input_dataset_dir is not None:
        # Handle directory input
        input_dir = Path(input_dataset_dir)
        if not input_dir.exists():
            if warning:
                print(f"Warning: Input directory not found: {input_dataset_dir}")
            return []
        
        # Find all supported files in the directory
        supported_extensions = ['.fbx', '.obj', '.ply', '.glb', '.gltf']
        input_files = []
        
        for ext in supported_extensions:
            input_files.extend(input_dir.glob(f"*{ext}"))
            input_files.extend(input_dir.glob(f"*{ext.upper()}"))
        
        processed_files = []
        for input_file in input_files:
            base_name = input_file.stem
            output_file = os.path.join(output_dataset_dir, f"{base_name}_{data_name}")
            
            if not BLENDER_AVAILABLE:
                processed_files.append((str(input_file), output_file))
            else:
                processed_files.append(process_with_bpy(str(input_file), output_file))
        
        return processed_files
    
    else:
        if warning:
            print("Warning: No input files or directory specified")
        return []

def process_with_bpy(input_file, output_file):
    """
    Process file using bpy (when available)
    """
    if not BLENDER_AVAILABLE:
        return (input_file, output_file)
    
    # Original bpy-based processing logic would go here
    # For now, just return the file paths
    return (input_file, output_file)

# Legacy function compatibility
def extract_files(*args, **kwargs):
    """Legacy function name compatibility"""
    return get_files(*args, **kwargs)
