import os
import sys
import shutil

# Add the current directory to the path to ensure modules can be found
sys.path.append(os.path.dirname(__file__))

import config
from splitter_old import SplitPDF as SplitPDF_old
from splitter import SplitPDF as SplitPDF_new

def run_test():
    # --- Test Parameters ---
    input_file = r"C:\Users\lilia\billboard-splitter\input\billboard3.pdf"
    ref_output_dir = r"C:\Users\lilia\billboard-splitter\REF"
    test_output_dir = r"C:\Users\lilia\billboard-splitter\TEST"

    # Clean up previous runs
    if os.path.exists(ref_output_dir):
        shutil.rmtree(ref_output_dir)
    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)
    os.makedirs(ref_output_dir)
    # The panels are not created in a subdirectory in the latest version
    # os.makedirs(os.path.join(ref_output_dir, 'panels'))
    os.makedirs(test_output_dir)
    # os.makedirs(os.path.join(test_output_dir, 'panels'))


    # --- Base Billboard Settings ---
    billboard_params = {
        "product_mode": "billboard",
        "rows": 2,
        "cols": 5,
        "overlap": 20.0,
        "white_stripe": 10.0,
        "add_white_to_overlap": True,
        "output_type": "output_both",
        "layout": "layout_vertical",
        "enable_reg_marks": True,
        "registration_mark_type": "reg_mark_cross",
        "enable_barcode": True,
        "barcode_type": "code_qr",
        "bryt_order": "bryt_order_1",
        "enable_separation_lines": True,
        "add_line_at_start": False,
        "add_line_at_end": False,
        "slice_rotation": 180, # This was in settings.json, and seems important
        "draw_slice_border": True, # This was in settings.json
    }

    # --- Step 1: Generate Reference Output (Old Splitter) ---
    print("Running splitter_old.py...")
    cfg_ref = config.load_settings()
    cfg_ref.update(billboard_params)
    if 'output_dir' in cfg_ref:
        del cfg_ref['output_dir']
    splitter_ref = SplitPDF_old(config)
    splitter_ref.split(input_file, ref_output_dir, **cfg_ref)
    print("Reference output generated in REF/")

    # --- Step 2: Generate Test Output (New Splitter) ---
    print("\nRunning splitter.py with scale 1:1...")
    cfg_test = config.load_settings()
    cfg_test.update(billboard_params)
    # Correctly update the nested scaling_settings dictionary
    cfg_test.update({
        "scaling_settings": {
            "scale_non_uniform": False,
            "scale_den": 1.0,
            "scale_den_x": 1.0,
            "scale_den_y": 1.0,
        }
    })
    
    if 'output_dir' in cfg_test:
        del cfg_test['output_dir']
    
    splitter_test = SplitPDF_new(config)
    splitter_test.split(input_file, test_output_dir, **cfg_test)
    print("Test output generated in TEST/")

if __name__ == "__main__":
    run_test()