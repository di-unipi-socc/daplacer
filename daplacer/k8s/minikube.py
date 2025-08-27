import subprocess
from typing import List


from subprocess import run
from typing import Optional, Dict


def start_minikube(
    num_nodes: int = 4,
    num_cpus: int = 4,
    memory: int = 8192,
    driver: str = "docker",
    extra_config: Optional[Dict[str, str]] = None,
):
    """
    Avvia un cluster Minikube con configurazioni personalizzate.

    :param num_nodes: Numero di nodi da creare
    :param num_cpus: Numero totale di CPU da distribuire
    :param memory: Quantità totale di memoria in MiB da distribuire
    :param driver: Driver di Minikube da usare (es. 'docker', 'virtualbox')
    :param extra_config: Dizionario con chiavi come "kubelet.node-status-update-frequency" e valori stringa
    """

    per_node_mem = max(memory // num_nodes, 2048)
    per_node_cpus = max(num_cpus // num_nodes, 2)

    print(f"Distributing {num_cpus} CPUs and {memory}MiB RAM across {num_nodes} nodes:")
    print(f"Each node will receive: {per_node_cpus} CPUs and {per_node_mem}MiB RAM\n")

    command = [
        "minikube",
        "start",
        f"--nodes={num_nodes}",
        f"--cpus={per_node_cpus}",
        f"--memory={per_node_mem}",
        f"--driver={driver}",
    ]

    if extra_config:
        for key, value in extra_config.items():
            command.append(f"--extra-config={key}={value}")

    try:
        run_command(command)
        print(f"Minikube cluster with {num_nodes} nodes started successfully.")
    except Exception as e:
        print(f"Error starting Minikube: {e}")


def is_minikube_running() -> bool:
    """Check if Minikube is running."""
    result = subprocess.run(
        ["minikube", "status", "--format", "{{.Host}}"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() == "Running"


def stop_minikube():
    run_command(["minikube", "stop"])


def delete_minikube():
    run_command(["minikube", "delete", "--all"])


def run_command(cmd: List[str]):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e}")
        raise
