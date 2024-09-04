What is Protomix?
=================

Protomix is a comprehensive Python package designed for preprocessing Nuclear Magnetic Resonance (NMR) data. It is an essential tool for academic researchers, students, and industry professionals who need to prepare 1H-NMR metabolomics data for analysis. Protomix automates and standardizes the preprocessing steps, ensuring high-quality, reliable data for further analysis.

Protomix offers a wide range of functionalities tailored to the specific needs of NMR spectroscopy. These tools help remove artifacts, enhance data quality, and prepare datasets for various forms of qualitative and quantitative analysis.

Capabilities at a Glance
------------------------

The main features of Protomix include:

- *Group Delay Removal:* Automatically removes group delay artifacts from your NMR data, ensuring cleaner spectra.
- *Solvent Residuals Removal:* Identifies and removes residual solvent peaks that can interfere with analysis.
- *Apodization:* Applies various apodization functions to your data to enhance signal-to-noise ratio.
- *Zero Filling:* Increases the number of data points through zero filling, which improves the resolution of the Fourier Transform.
- *Fourier Transform:* Converts time-domain NMR data into frequency-domain spectra, a key step in NMR data processing.
- *Phase Correction:* Corrects phase errors in the spectra to align peaks properly.
- *Internal Referencing:* Aligns chemical shifts in your spectra to a known reference peak, ensuring consistency across samples.
- *Baseline Correction:* Removes baseline drifts and inconsistencies in NMR spectra, providing a smoother baseline.
- *Negative Values Zeroing:* Sets negative intensities in spectra to zero, which is particularly useful for clean peak detection.
- *Region Removal:* Excludes specific spectral regions that are not of interest or may contain artifacts.
- *Window Selection:* Focuses analysis on selected regions of the spectra, enhancing targeted data analysis.
- *Peak Alignment:* Aligns peaks across multiple spectra for comparative analysis, crucial in metabolomics studies.
- *Binning:* Segments spectra into bins for statistical analysis, a common step in metabolomics data processing.
- *Normalization:* Normalizes spectra to account for concentration differences, ensuring comparability across samples.

Further Information
-------------------

Further information is provided on the Protomix main website, where you can find detailed tutorials, examples, and additional resources for using Protomix effectively. The Protomix code is available for download on GitHub.

Authors
-------

Protomix was developed by:

- *Mohammed Zniber* (Åbo Akademi University)
- *Tan Phat Huynh* (Åbo Akademi University)
- *Youssef Fatihi* (Ibn Tofail University)

The Protomix Python package is under continuous development at Åbo Akademi University and Ibn Tofail University, with ongoing contributions from an international team of researchers.

.. toctree::
   :maxdepth: 2

   section1
   section2
   section3