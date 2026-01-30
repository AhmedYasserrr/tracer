from typing import Optional, List, Dict, Any, Type
from datetime import datetime
from tracer.db.models import NetworkLog
from tracer.db.connection import SessionLocal


class NetCRUD:
    """CRUD operations for NetworkLog (network table)"""

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @property
    def model_class(self) -> Type[NetworkLog]:
        return NetworkLog

    def add(self, metric_details: Dict[str, Any]) -> NetworkLog:
        """
        Add a new network metric entry to the database

        Args:
            metric_details: Dictionary containing:
                - download: float - Download speed in Mbps
                - upload: float - Upload speed in Mbps
                - ping_ms: float - Ping latency in milliseconds
                - packet_loss: float - Packet loss percentage
                - bytes_sent: int - Total bytes sent
                - bytes_recv: int - Total bytes received
                - public_ip: str - Public IP address
                - timestamp: datetime (optional) - Metric timestamp

        Returns:
            NetworkLog: The created network log entry
        """
        try:
            # Add timestamp if not provided
            if "timestamp" not in metric_details:
                metric_details["timestamp"] = datetime.utcnow()

            network_log = NetworkLog(**metric_details)
            self.session.add(network_log)
            self.session.commit()
            self.session.refresh(network_log)
            return network_log

        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, log_id: int) -> Optional[NetworkLog]:
        """
        Get a network log entry by ID

        Args:
            log_id: The ID of the log entry

        Returns:
            NetworkLog or None if not found
        """
        return self.session.query(NetworkLog).filter(NetworkLog.id == log_id).first()

    def get_latest(self, limit: int = 1) -> List[NetworkLog]:
        """
        Get the latest network log entries

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of NetworkLog entries
        """
        return (
            self.session.query(NetworkLog)
            .order_by(NetworkLog.timestamp.desc())
            .limit(limit)
            .all()
        )

    def get_by_ip(self, public_ip: str) -> List[NetworkLog]:
        """
        Get all network log entries for a specific public IP

        Args:
            public_ip: The public IP address to search for

        Returns:
            List of NetworkLog entries
        """
        return (
            self.session.query(NetworkLog)
            .filter(NetworkLog.public_ip == public_ip)
            .all()
        )

    def get_entries_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[NetworkLog]:
        """
        Get network log entries within a date range

        Args:
            start_date: Start of the date range
            end_date: End of the date range

        Returns:
            List of NetworkLog entries within the date range
        """
        return (
            self.session.query(NetworkLog)
            .filter(NetworkLog.timestamp >= start_date)
            .filter(NetworkLog.timestamp <= end_date)
            .order_by(NetworkLog.timestamp.desc())
            .all()
        )

    def get_average_metrics(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> Dict[str, float]:
        """
        Get average network metrics over a time period

        Args:
            start_date: Start of the date range (optional)
            end_date: End of the date range (optional)

        Returns:
            Dictionary with average values for download, upload, ping_ms, packet_loss
        """
        from sqlalchemy import func

        query = self.session.query(
            func.avg(NetworkLog.download).label("avg_download"),
            func.avg(NetworkLog.upload).label("avg_upload"),
            func.avg(NetworkLog.ping_ms).label("avg_ping_ms"),
            func.avg(NetworkLog.packet_loss).label("avg_packet_loss"),
        )

        if start_date:
            query = query.filter(NetworkLog.timestamp >= start_date)
        if end_date:
            query = query.filter(NetworkLog.timestamp <= end_date)

        result = query.first()

        return {
            "avg_download": result.avg_download,
            "avg_upload": result.avg_upload,
            "avg_ping_ms": result.avg_ping_ms,
            "avg_packet_loss": result.avg_packet_loss,
        }

    def update(self, log_id: int, update_data: Dict[str, Any]) -> Optional[NetworkLog]:
        """
        Update a network log entry

        Args:
            log_id: The ID of the log entry to update
            update_data: Dictionary containing fields to update

        Returns:
            Updated NetworkLog entry or None if not found
        """
        try:
            network_log = (
                self.session.query(NetworkLog).filter(NetworkLog.id == log_id).first()
            )
            if not network_log:
                return None

            # Update only provided fields
            for key, value in update_data.items():
                if hasattr(network_log, key):
                    setattr(network_log, key, value)

            self.session.commit()
            self.session.refresh(network_log)
            return network_log

        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, log_id: int) -> bool:
        """
        Delete a network log entry

        Args:
            log_id: The ID of the log entry to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            network_log = (
                self.session.query(NetworkLog).filter(NetworkLog.id == log_id).first()
            )
            if not network_log:
                return False

            self.session.delete(network_log)
            self.session.commit()
            return True

        except Exception as e:
            self.session.rollback()
            raise e

    def delete_by_date_range(self, start_date: datetime, end_date: datetime) -> int:
        """
        Delete all network log entries within a date range

        Args:
            start_date: Start of the date range
            end_date: End of the date range

        Returns:
            Number of deleted entries
        """
        try:
            count = (
                self.session.query(NetworkLog)
                .filter(NetworkLog.timestamp >= start_date)
                .filter(NetworkLog.timestamp <= end_date)
                .count()
            )
            self.session.query(NetworkLog).filter(
                NetworkLog.timestamp >= start_date
            ).filter(NetworkLog.timestamp <= end_date).delete()
            self.session.commit()
            return count

        except Exception as e:
            self.session.rollback()
            raise e
