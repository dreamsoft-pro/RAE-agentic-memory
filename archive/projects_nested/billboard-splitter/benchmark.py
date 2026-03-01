import time
import os
import shutil
import cProfile
import pstats
import io
import logging

import splitter
import config

TEST_FILES = ["billboard1.pdf", "billboard2.pdf", "billboard3.pdf"]

# --- Test Scenarios ---
SCENARIOS = {
    "separate_files": {
        "output_dir": "benchmark_output_separate",
        "settings": {
            "output_type": "output_separate_files",
            "enable_separation_lines": False, # Not applicable for separate files
            "add_line_at_start": False,
            "add_line_at_end": False,
        }
    },
    "common_sheet": {
        "output_dir": "benchmark_output_common",
        "settings": {
            "output_type": "output_common_sheet",
            "enable_separation_lines": True,
            "add_line_at_start": True,
            "add_line_at_end": True,
        }
    }
}

# --- Base settings common to all scenarios ---
BASE_SETTINGS = {
    "overlap": 20.0,
    "rows": 2,
    "cols": 5,
    "layout": "layout_vertical",
    "enable_reg_marks": True,
    "registration_mark_type": "reg_mark_cross",
    "enable_barcode": True,
    "barcode_type": "code_qr",
    "bryt_order": "bryt_order_1",
    "white_stripe": 10.0,
    "add_white_to_overlap": True,
}

def run_test_scenario(splitter_instance, scenario_name, scenario_config):
    """Runs a single test scenario and prints the results."""
    output_dir = scenario_config["output_dir"]
    test_settings = {**BASE_SETTINGS, **scenario_config["settings"]}

    print(f"--- Running Scenario: {scenario_name} ---")

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    print(f"Output directory: '{output_dir}'")
    print("-" * 50)

    total_time = 0
    for test_file in TEST_FILES:
        if not os.path.exists(test_file):
            print(f"Test file '{test_file}' not found. Skipping.")
            continue

        print(f"Processing file: {test_file}...")
        start_time = time.time()

        success = splitter_instance.split(
            input_pdf_path=test_file,
            output_dir=output_dir,
            **test_settings
        )

        end_time = time.time()
        duration = end_time - start_time
        total_time += duration

        if success:
            print(f"Completed in: {duration:.4f} seconds")
        else:
            print(f"An error occurred during processing. Time: {duration:.4f} seconds")

        print("-" * 50)

    print(f"\n--- Scenario '{scenario_name}' Summary ---")
    avg_time = total_time / len(TEST_FILES) if TEST_FILES else 0
    print(f"Total time for {len(TEST_FILES)} files: {total_time:.4f} seconds")
    print(f"Average time per file: {avg_time:.4f} seconds")
    print("-" * 50 + "\n")
    return total_time

def profiled_task():
    """The main function to be profiled, running all test scenarios."""
    print("--- Starting Comprehensive Verification Benchmark ---")

    try:
        config.load_settings()
        logging.getLogger('BillboardSplitter').setLevel(logging.WARNING)
        splitter_instance = splitter.SplitPDF(config)
    except Exception as e:
        print(f"Error during initialization: {e}")
        return

    total_benchmark_time = 0
    for name, scenario_config in SCENARIOS.items():
        total_benchmark_time += run_test_scenario(splitter_instance, name, scenario_config)

    print(f"\n=== Total Benchmark Time for All Scenarios: {total_benchmark_time:.4f} seconds ===")

def run_profiler():
    """Runs cProfile on the main task and saves the results."""
    profiler = cProfile.Profile()
    profiler.enable()

    profiled_task()

    profiler.disable()

    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(40)

    profile_results = s.getvalue()

    try:
        with open("profiling_results_final.txt", "w+") as f:
            f.write(profile_results)
        print("\nFinal profiling results saved to 'profiling_results_final.txt'")
    except Exception as e:
        print(f"\nCould not save final profiling results: {e}")

    print("\n--- Final Profiling Results (cProfile) ---")
    print(profile_results)
    print("------------------------------------------")

if __name__ == "__main__":
    run_profiler()