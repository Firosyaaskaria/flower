"""fastai_example: A Flower / Fastai app."""

from typing import List, Tuple

from flwr.common import Metrics
from flwr.server import ServerApp, ServerConfig
from flwr.server.strategy import FedAvg


# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


# Define strategy
strategy = FedAvg(evaluate_metrics_aggregation_fn=weighted_average)

config = ServerConfig(num_rounds=1)

app = ServerApp(
    config=config,
    strategy=strategy,
)


# import flwr as fl
# from flwr.common import Metrics
#
#
#
#
# # Define strategy
# strategy = fl.server.strategy.FedAvg(evaluate_metrics_aggregation_fn=weighted_average)
#
# # Start Flower server
# fl.server.start_server(
#     server_address="0.0.0.0:8080",
#     config=fl.server.ServerConfig(num_rounds=3),
#     strategy=strategy,
# )
