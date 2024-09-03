import os
import pandas as pd

from Protomix.utils import get_paths

def extract_params(root_directory: str) -> pd.DataFrame:
    """
    Extract parameters from 'acqus' files located within a directory hierarchy.

    :param root_directory: Root directory where the 'acqus' files are located.
    :type root_directory: str

    :return: A dataframe with extracted parameters, indexed by sample names.
    :rtype: pd.DataFrame
    """
        
    # Check the type of root_directory
    assert isinstance(root_directory, str), "root_directory should be a string."
    
    # Check if root_directory exists and is a directory
    assert os.path.exists(root_directory) and os.path.isdir(root_directory), "root_directory should point to an existing directory."
    
    acqus_files = []
    sample_names = []
    
    paths = get_paths(root_directory, 'acqus')
    
    # Check if paths list is not empty
    assert paths, "No 'acqus' files found in the specified directory."
    
    for data_file in paths:
        sample_names.append(os.path.basename(os.path.dirname(os.path.dirname(data_file))))
        
        with open(data_file) as file:
            acqus_data = file.readlines()

        params = {}
        for line in acqus_data:
            if line.startswith('##'):
                parts = line.strip().split('=')
                assert len(parts) == 2, f"Unexpected data format in {data_file}."
                key, value = parts
                params[key[2:].strip()] = value.strip()
        
        acqus_files.append(params)
    
    return pd.DataFrame(acqus_files, index=sample_names)