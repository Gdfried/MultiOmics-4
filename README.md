# Multi-Omics 4

**Project Number**: 2541  
**Contributors**: Dor Fried, Lior Segal  
**Mentor**: Prof. Ilan Tsarfaty, Faculty of Medical and Health Sciences, Tel Aviv University  

## Project Overview
The Multi-Omics 4 project aims to develop a robust, integrated pipeline for multi-omics cancer research. Building a solution capable of processing diverse biological data types effectively. This pipeline addresses challenges in data integration, image processing, and genetic analysis for cancer research, particularly focusing on breast cancer prognosis.

## Objectives
- **Develop a Genomics-Phatomics Integrated Pipeline**: Create a system for multiomics cancer research.
- **Pathological Image Data Management**: Implement a secure, efficient, and scalable data management solution.
- **Enhanced Image Analysis**: Improve histopathological image processing.
- **Modernize Genetic Analysis**: Transition to the R/qtl2 framework for QTL analysis.

## Key Components
### 1. **Smart Data Management Tool (SDMT)**
   - **Functionality**: Manages data downloads, preprocessing, and transfers.
   - **Hardware**: Combines a high-capacity AI server for heavy computational tasks with local management for preprocessing and storage.
   - **Impact**: Increases download speeds, storage capacity, and enables seamless large-scale data handling.

### 2. **Computational Image Processing (CIP)**
   - **Framework**: Automates image processing using QuPath and Groovy scripting.
   - **Processes**: Includes image standardization, segmentation, and Delaunay triangulation.
   - **Optimization**: Utilizes parameter tuning for improved nucleus detection accuracy.

### 3. **Quantitative Trait Locus (QTL) Analysis**
   - **Enhancement**: Transition from the HAPPY framework to R/qtl2 for advanced genetic data analysis.
   - **Data Integration**: Aligns phenotypic and genetic information, leveraging outputs from the CIP component.
   - **Analysis**: Uses permutation testing to evaluate the significance of cross-information in genetic analysis.

## Results
- **CIP Automation**: Achieved a 99.7% detection accuracy and improved throughput to 28.8 images per day.
- **QTL Analysis**: Conducted initial R/qtl2 runs, setting up future comprehensive analyses.
- **Pipeline Impact**: Demonstrated increased accuracy and efficiency, supporting a unified approach to data management, genetic analysis, and image processing.

## Future Work
- **Enhance QuPath Versatility**: Further automate parameter management.
- **Full Pipeline Integration**: Extend the pipeline to cover the complete flow from data ingestion to cancer prognosis prediction.
- **Reevaluate MultiSurv**: Apply new data and insights to improve and potentially reproduce original model findings.

## Getting Started
1. **Prerequisites**:
   - Python, Bash scripting capabilities.
   - QuPath and R/qtl2 installed.
   
2. **Installation**:
   - Clone this repository.
   - Follow the installation guide for setting up QuPath and R/qtl2 dependencies.

3. **Usage**:
   - Run the data management script to download and preprocess data.
   - Use the CIP tool for automated image processing.
   - Execute the QTL analysis script to analyze genetic data with the latest framework.

## Contributors
- **Dor Fried**
- **Lior Segal**
- **Mentor**: Prof. Ilan Tsarfaty

## License
This project is licensed under the MIT License.

--- 

Let me know if you'd like to refine any part or add specific sections like setup commands or more detailed instructions.
