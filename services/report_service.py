import pandas as pd
import logging
import os
from datetime import datetime
from typing import List, Dict, Any
from core.config import settings

logger = logging.getLogger(__name__)

class ReportService:
    """
    Skill for generating reports (CSV, Excel) from agent data.
    """
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or str(settings.reports_path)

    def export_to_csv(self, data: List[Dict[str, Any]], filename_prefix: str) -> str:
        """
        Exports a list of dictionaries to a CSV file.
        Returns the path to the generated file.
        """
        if not data:
            logger.warning("No data provided for export.")
            return ""

        df = pd.DataFrame(data)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.csv"
        file_path = os.path.join(self.output_dir, filename)
        
        try:
            df.to_csv(file_path, index=False)
            logger.info(f"Report exported successfully: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            return ""

    def export_to_excel(self, data: List[Dict[str, Any]], filename_prefix: str) -> str:
        """
        Exports data to an Excel file.
        """
        if not data:
            return ""

        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.xlsx"
        file_path = os.path.join(self.output_dir, filename)

        try:
            df.to_excel(file_path, index=False)
            logger.info(f"Excel report exported: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to export Excel: {e}")
            return ""
