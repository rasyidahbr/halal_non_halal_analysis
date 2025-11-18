"""
Utilities for loading and processing data.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional


def load_ingredients_data(file_path: str) -> pd.DataFrame:
    """
    Load the ingredients dataset and preprocess it.
    
    Args:
        file_path (str): Path to the CSV file containing ingredient data
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame with ingredient data
        
    Raises:
        FileNotFoundError: If the ingredients dataset file doesn't exist
    """
    # Check if file exists
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Ingredients dataset file not found: {file_path}")
        
    # Load the dataset for halal ingredients
    df = pd.read_csv(file_path)

    # Convert all string columns to lowercase and remove spaces
    for col in df.columns:
        if df[col].dtype == 'object':  # Check if the column is of string type
            df[col] = df[col].str.lower()
            
    return df


def save_analysis_results(
    result: Dict[str, Any], 
    output_dir: Optional[str] = None,
    filename: Optional[str] = None
) -> str:
    """
    Save analysis results to a CSV file.
    
    Args:
        result (Dict[str, Any]): Analysis results
        output_dir (Optional[str]): Directory to save the file (defaults to data directory)
        filename (Optional[str]): Filename (defaults to "analysis_results.csv")
        
    Returns:
        str: Path to the saved file
    """
    import pandas as pd
    from datetime import datetime
    
    # Default values
    if output_dir is None:
        output_dir = "data"
        
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_results_{timestamp}.csv"
    
    # Create directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Create DataFrame from results
    df = pd.DataFrame.from_dict({k: [v] for k, v in result.items()})
    
    # Save to CSV
    file_path = output_path / filename
    df.to_csv(file_path, index=False)
    
    return str(file_path)