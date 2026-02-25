import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    OrderBy
)
from core.config import settings

logger = logging.getLogger(__name__)

class AnalyticsSkill:
    """
    Skill for fetching data from Google Analytics 4 (GA4).
    """
    def __init__(self, property_id: str = None, credentials_path: str = None):
        self.property_id = property_id or settings.GA4_PROPERTY_ID
        self.credentials_path = credentials_path or settings.GA4_CREDENTIALS_PATH
        self._client = None

    @property
    def client(self):
        if self._client is None:
            if not self.credentials_path:
                raise ValueError("GA4_CREDENTIALS_PATH not set in configuration.")
            self._client = BetaAnalyticsDataClient.from_service_account_json(self.credentials_path)
        return self._client

    async def get_basic_report(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Fetches basic traffic metrics (sessions, active users, page views) for the last N days.
        """
        if not self.property_id:
            logger.error("GA4_PROPERTY_ID is not configured.")
            return []

        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[Dimension(name="date")],
                metrics=[
                    Metric(name="activeUsers"),
                    Metric(name="sessions"),
                    Metric(name="screenPageViews"),
                    Metric(name="bounceRate")
                ],
                date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="yesterday")],
                order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))]
            )

            # Note: The GA4 client is synchronous, but we wrap it in a simple way.
            # In a high-concurrency app we'd use run_in_executor, but for CLI this is fine.
            response = self.client.run_report(request)
            
            report_data = []
            for row in response.rows:
                report_data.append({
                    "date": row.dimension_values[0].value,
                    "active_users": row.metric_values[0].value,
                    "sessions": row.metric_values[1].value,
                    "page_views": row.metric_values[2].value,
                    "bounce_rate": f"{float(row.metric_values[3].value) * 100:.2f}%" if row.metric_values[3].value else "0%"
                })
            
            return report_data
        except Exception as e:
            logger.error(f"Error fetching GA4 report: {e}")
            return []

    async def get_top_pages(self, days: int = 30, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetches top performing pages by views.
        """
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[Dimension(name="pagePath")],
                metrics=[Metric(name="screenPageViews"), Metric(name="activeUsers")],
                date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="yesterday")],
                limit=limit
            )
            
            response = self.client.run_report(request)
            pages = []
            for row in response.rows:
                pages.append({
                    "page_path": row.dimension_values[0].value,
                    "views": row.metric_values[0].value,
                    "users": row.metric_values[1].value
                })
            return pages
        except Exception as e:
            logger.error(f"Error fetching top pages: {e}")
            return []
