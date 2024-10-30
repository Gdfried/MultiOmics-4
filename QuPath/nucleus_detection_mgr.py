import os
import subprocess
import pandas as pd
import argparse
import re
import logging
import sys


def run_qupath_image_extraction(image_dir, output_dir=None, image_type='svs', groovy_script="qupath_script.groovy", config_file='qupath_parameters.json', program_path="QuPath-0.5.1 (console).exe"):
    if output_dir is None:
        output_dir = os.path.join(image_dir, "qupath_output/")
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Set up logging
    logging.basicConfig(filename=os.path.join(output_dir, 'qupath_image_extraction.log'), level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    logging.info(f"Starting QuPath image extraction with the following parameters: image_dir={image_dir}, output_dir={output_dir}, image_type={image_type}, groovy_script={groovy_script}, config_file={config_file}, program_path={program_path}")

    qupath_parameters = ""
    with open(config_file) as fs:
        for line in fs:
            qupath_parameters += line.strip()
    # qupath_parameters = qupath_parameters.replace(" ", "____")
    
    # Run the subprocess with real-time output
    process = subprocess.Popen([program_path, "script", groovy_script, "-a", image_dir, "-a", output_dir, "-a", qupath_parameters, "-a", image_type], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.STDOUT,
                               universal_newlines=True,
                               bufsize=1)

    # Print and log output in real-time
    for line in iter(process.stdout.readline, ''):
        print(line, end='')  # Print to console
        logging.info(line.strip())  # Log to file
        sys.stdout.flush()  # Ensure output is flushed immediately

    process.stdout.close()
    return_code = process.wait()

    if return_code:
        logging.error(f"Subprocess returned non-zero exit code: {return_code}")
        raise subprocess.CalledProcessError(return_code, process.args)

    logging.info("QuPath subprocess completed.")

    average_all = pd.DataFrame([])
    for file in os.listdir(os.path.join(output_dir, "QPProject")):
        if file.endswith('.tsv'):
            print(f"Processing image: {file}")
            df = pd.read_csv(os.path.join(output_dir, "QPProject", file), sep='\t')
            # transform headers to original format
            df.columns = [re.sub(r' ', '', col) for col in df.columns]
            df.columns = [re.sub(r'[\(\)\:\.]', '_', col) for col in df.columns]

            image = df.iloc[0, 0]
            num_of_cells_detected = len(df) - 1
            numbers = df.iloc[:, 7:]
            average = numbers.mean(axis=0, skipna=False)
            df_average = pd.DataFrame([average])
            df_average.insert(0, 'Image', image)
            df_average['num_of_cells_detected'] = num_of_cells_detected
            average_all = pd.concat([average_all, df_average])
            print(f"Finished processing image: {file}")

    summary_table_path = os.path.join(output_dir, "Summary_Table.csv")
    average_all.to_csv(summary_table_path)

    logging.info(f"QuPath image extraction completed successfully. Output directory: {output_dir}")
    logging.info(f"Summary table saved to: {summary_table_path}")
    print(f"QuPath image extraction completed successfully. Output directory: {output_dir}")
    print(f"Summary table saved to: {summary_table_path}")


#                 print("run completed results are in:", exp_outdir)
def run_exp_short(args, cfg_template):
    requestedPixelSizeMicrons = [0, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
    threshold = [0, 0.0025, 0.005, 0.01 ,0.025, 0.05, 0.075, 0.1, 0.125, 0.15]
    backgroundRadiusMicrons = [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
    
    with open(cfg_template, "r") as tmplate:
        tmp = tmplate.read()

    for rpsm in requestedPixelSizeMicrons:
        th = 0.1
        brm = 4.0
        exp_outdir = os.path.join(args.outdir, f"short_exp_rpsm_{rpsm}_threshold_{th}_brm_{brm}")
        os.makedirs(exp_outdir, exist_ok=True)

        exp_json = os.path.join(exp_outdir, "cfg.json")
        with open(exp_json, "w") as exp_cfg:
            to_write = re.sub(r"<requestedPixelSizeMicrons>", str(rpsm), tmp)
            to_write = re.sub(r"<threshold>", str(th), to_write)
            to_write = re.sub(r"<backgroundRadiusMicrons>", str(brm), to_write)
            exp_cfg.write(to_write)

        # Set up a separate log file for each experiment
        log_file = os.path.join(exp_outdir, 'experiment.log')
        logging.basicConfig(
            filename=log_file, 
            level=logging.INFO, 
            format='%(asctime)s %(levelname)s: %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S',
            force=True  # Ensures that the logging configuration is updated
        )

        logging.info(f"Starting experiment with parameters: rpsm={rpsm}, threshold={th}, brm={brm}")
        logging.info(f"Running with the following configuration:\n{to_write}")
        
        try:
            run_qupath_image_extraction(
                args.input_image_dir, exp_outdir, args.image_type, 
                args.nucleus_detection_automation, exp_json, args.qupath_console_path
            )
            logging.info("Experiment completed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Experiment failed with error: {e}")
        
        # Ensure the log is closed properly before starting the next experiment
        logging.shutdown()

        print(f"Run completed for rpsm={rpsm}, threshold={th}, brm={brm}. Results are in: {exp_outdir}")
    for th in threshold:
        rspm = 0.5
        brm = 4.0
        exp_outdir = os.path.join(args.outdir, f"short_exp_rpsm_{rpsm}_threshold_{th}_brm_{brm}")
        os.makedirs(exp_outdir, exist_ok=True)

        exp_json = os.path.join(exp_outdir, "cfg.json")
        with open(exp_json, "w") as exp_cfg:
            to_write = re.sub(r"<requestedPixelSizeMicrons>", str(rpsm), tmp)
            to_write = re.sub(r"<threshold>", str(th), to_write)
            to_write = re.sub(r"<backgroundRadiusMicrons>", str(brm), to_write)
            exp_cfg.write(to_write)

        # Set up a separate log file for each experiment
        log_file = os.path.join(exp_outdir, 'experiment.log')
        logging.basicConfig(
            filename=log_file, 
            level=logging.INFO, 
            format='%(asctime)s %(levelname)s: %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S',
            force=True  # Ensures that the logging configuration is updated
        )

        logging.info(f"Starting experiment with parameters: rpsm={rpsm}, threshold={th}, brm={brm}")
        logging.info(f"Running with the following configuration:\n{to_write}")
        
        try:
            run_qupath_image_extraction(
                args.input_image_dir, exp_outdir, args.image_type, 
                args.nucleus_detection_automation, exp_json, args.qupath_console_path
            )
            logging.info("Experiment completed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Experiment failed with error: {e}")
        
        # Ensure the log is closed properly before starting the next experiment
        logging.shutdown()

        print(f"Run completed for rpsm={rpsm}, threshold={th}, brm={brm}. Results are in: {exp_outdir}")
    for brm in backgroundRadiusMicrons:
        rspm = 0.5
        th = 0.1
        exp_outdir = os.path.join(args.outdir, f"short_exp_rpsm_{rpsm}_threshold_{th}_brm_{brm}")
        os.makedirs(exp_outdir, exist_ok=True)

        exp_json = os.path.join(exp_outdir, "cfg.json")
        with open(exp_json, "w") as exp_cfg:
            to_write = re.sub(r"<requestedPixelSizeMicrons>", str(rpsm), tmp)
            to_write = re.sub(r"<threshold>", str(th), to_write)
            to_write = re.sub(r"<backgroundRadiusMicrons>", str(brm), to_write)
            exp_cfg.write(to_write)

        # Set up a separate log file for each experiment
        log_file = os.path.join(exp_outdir, 'experiment.log')
        logging.basicConfig(
            filename=log_file, 
            level=logging.INFO, 
            format='%(asctime)s %(levelname)s: %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S',
            force=True  # Ensures that the logging configuration is updated
        )

        logging.info(f"Starting experiment with parameters: rpsm={rpsm}, threshold={th}, brm={brm}")
        logging.info(f"Running with the following configuration:\n{to_write}")
        
        try:
            run_qupath_image_extraction(
                args.input_image_dir, exp_outdir, args.image_type, 
                args.nucleus_detection_automation, exp_json, args.qupath_console_path
            )
            logging.info("Experiment completed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Experiment failed with error: {e}")
        
        # Ensure the log is closed properly before starting the next experiment
        logging.shutdown()

        print(f"Run completed for rpsm={rpsm}, threshold={th}, brm={brm}. Results are in: {exp_outdir}")


def main():
    args = parser.parse_args()
    print("Starting QuPath image extraction...")
    # run_exp(args, args.qupath_parameters_config)
    # run_exp_short(args, args.qupath_parameters_config)
    run_qupath_image_extraction(args.input_image_dir, args.outdir, args.image_type, args.nucleus_detection_automation, args.qupath_parameters_config, args.qupath_console_path)
    print("QuPath image extraction completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=str, default=".", help="Path to output directory")
    parser.add_argument("--qupath_console_path", type=str, default=r"/home/ilants/Documents/QuPath-v0.5.1-Linux/QuPath/bin/QuPath", help="Path to the qupath console application")
    parser.add_argument("--input_image_dir", type=str, default=r"/home/ilants/Documents/example_image_dir", help="path to directory containing all images (one format of images for example .svs)")
    parser.add_argument("--image_type", type=str, default="svs", help="image type (for example .svs|.png|.tiff|.SCN)")
    parser.add_argument("--nucleus_detection_automation", type=str, default=r"/home/ilants/Documents/utls/nucleus_detection_wargs.groovy", help="path to the groovy script that performs the nucleus detection automation in qupath")
    parser.add_argument("--qupath_parameters_config", type=str, default=r"/home/ilants/Documents/utls/qupath_parameters.json", help="path to the parameters json file")
    parser.add_argument("--qupath_parameters_config", type=str, default=r"/home/ilants/Documents/utls/qupath_parameters.json", help="path to the parameters json file")

    main()