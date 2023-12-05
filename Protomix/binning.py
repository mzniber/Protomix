import numpy as np
import pandas as pd

def binning(spectra_df: pd.DataFrame, bin_size: float, method="trapezoidal") -> pd.DataFrame:
    """
    Perform uniform binning on an NMR spectrum by integrating the area under the curve for each bin.

    Parameters:
    - spectra_df (pd.DataFrame): DataFrame containing the spectra. Rows are samples, columns are ppm values.
    - bin_size (float): Size of the bin in ppm.
    - method (str): Integration method - "trapezoidal" or "rectangular".

    Returns:
    - pd.DataFrame: Binned spectra with integrated intensities.
    """
    
    # Extract ppm values from columns
    ppm_values = spectra_df.columns.astype(float).values
    
    # Define the start and end of the ppm range
    ppm_start = ppm_values[0]
    ppm_end = ppm_values[-1]
    
    # Create new binned ppm values
    binned_ppm = np.arange(ppm_start, ppm_end, bin_size)
    
    # Create an empty DataFrame to store binned data
    binned_df = pd.DataFrame(index=spectra_df.index, columns=binned_ppm[:-1])
    
    for i in range(len(binned_ppm) - 1):
        # Mask to select values in the current bin range
        mask = (ppm_values >= binned_ppm[i]) & (ppm_values < binned_ppm[i+1])
        
        # Determine the width of each data point within the bin
        delta_ppm = ppm_values[1] - ppm_values[0]
        
        if method == "trapezoidal":
            # Average the first and last intensities in the bin for each sample
            avg_intensity = 0.5 * (spectra_df.loc[:, mask].iloc[:, 0] + spectra_df.loc[:, mask].iloc[:, -1])
            binned_df[binned_ppm[i]] = avg_intensity * delta_ppm * mask.sum()
        
        elif method == "rectangular":
            # Use the midpoint intensity for each bin (or the first intensity, depending on preference)
            binned_df[binned_ppm[i]] = spectra_df.loc[:, mask].mean(axis=1) * delta_ppm * mask.sum()
        else:
            raise ValueError("Invalid method. Choose 'trapezoidal' or 'rectangular'.")
    
    return binned_df