import time
from pathlib import Path

import pandas as pd

from src.replay_engine.producer import FraudKafkaProducer
from src.replay_engine.validator import EventValidator
from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger("ReplayEngine")

EVENT_COLUMNS = [
    "TransactionID",
    "TransactionDT",
    "TransactionAmt",
    "ProductCD",
    "card4",
    "card6",
    "addr1",
    "addr2",
    "P_emaildomain",
    "R_emaildomain",
    "isFraud",
]


class ReplayEngine:
    """
    Reads historical transaction data
    and replays it into Kafka.
    """

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.csv_path = (
            self.project_root
            / config["replay"]["csv_path"]
        )

        self.max_events = config["replay"]["max_events"]

        self.replay_speed = config["replay"]["replay_speed"]

    def load_transactions(self):

        logger.info(f"Loading dataset: {self.csv_path}")

        df = pd.read_csv(
            self.csv_path,
            usecols=EVENT_COLUMNS
        )

        logger.info(f"Loaded {len(df):,} transactions.")
        logger.info(f"Selected {len(EVENT_COLUMNS)} columns.")

        return df


def main():

    replay = ReplayEngine()

    validator = EventValidator()

    producer = FraudKafkaProducer()

    transactions = replay.load_transactions()

    logger.info("=" * 60)
    logger.info("Starting Replay Engine...")
    logger.info(f"Maximum Events : {replay.max_events}")
    logger.info(f"Replay Speed   : {replay.replay_speed} seconds")
    logger.info("=" * 60)

    published = 0

    for _, row in transactions.iterrows():

        event = row.to_dict()

        validated_event = validator.validate(event)

        if validated_event is None:
            continue

        producer.send(validated_event)

        published += 1

        # Print only the first 5 events
        if published <= 5:

            print("\n" + "=" * 60)
            print(f"EVENT {published}")
            print("=" * 60)
            print(validated_event)

        # Progress every 100 events
        if published % 100 == 0:

            logger.info(f"Published {published} events...")

        # Stop after configured limit
        if published >= replay.max_events:

            logger.info(
                f"Reached configured limit ({replay.max_events})."
            )
            break

        time.sleep(replay.replay_speed)

    producer.flush()

    producer.close()

    logger.info("=" * 60)
    logger.info(f"Replay Completed Successfully.")
    logger.info(f"Total Events Published : {published}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()