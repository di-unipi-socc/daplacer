import threading
from random import Random

from daplacer.k8s import minikube as mkb
from daplacer.k8s.builder import write_infrastructure_kb
from daplacer.utils import (
    INFR_NAME,
    INFRS_DIR,
    NUM_NODES,
    SEED,
    SLEEP_TIME,
    USE_DOCKER,
)

if __name__ == "__main__":

    extra_config = {
        "kubelet.node-status-update-frequency": f"{SLEEP_TIME}s",
        "controller-manager.node-monitor-grace-period": f"{SLEEP_TIME+1}s",
        "controller-manager.node-monitor-period": f"{SLEEP_TIME}s",
        # "controller-manager.pod-eviction-timeout": f"{SLEEP_TIME+1}s",
        # "kubelet.eviction-hard": "memory.available<100Mi,nodefs.available<1Gi",
        # "kubelet.eviction-pressure-transition-period": "10s",
    }

    if not mkb.is_minikube_running():
        print("Minikube is not running. Starting.")
        mkb.start_minikube(
            num_nodes=NUM_NODES + 1,  # extra_config=extra_config
        )  # +1 for the control plane node
    else:
        print("Minikube is running. Generating pods...")

    r = Random(SEED)

    output_path = INFRS_DIR / INFR_NAME.format(nodes=NUM_NODES, seed=SEED)
    write_infrastructure_kb(output_path=output_path, rand=r, use_docker=USE_DOCKER)
