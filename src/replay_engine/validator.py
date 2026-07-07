import math

from src.utils.logger import get_logger

logger = get_logger("Validator")


class EventValidator:
    """
    Validates and cleans payment events before they are
    published to Kafka.
    """

    REQUIRED_FIELDS = [
        "TransactionID",
        "TransactionAmt",
        "TransactionDT",
        "ProductCD",
    ]

    def validate(self, event: dict):
        """
        Validate and clean a payment event.
        """

        cleaned_event = {}

        # Replace NaN with None
        for key, value in event.items():

            if isinstance(value, float) and math.isnan(value):
                cleaned_event[key] = None
            else:
                cleaned_event[key] = value

        # Validate required fields
        for field in self.REQUIRED_FIELDS:

            if cleaned_event.get(field) is None:

                logger.warning(
                    f"Missing required field: {field}"
                )

                return None

        return cleaned_event