import threading

from daplacer.k8s.controller import controller_loop
from swiplserver import PrologMQI
from daplacer.k8s.scheduler import scheduler_loop
from daplacer.utils import (
    NUM_NODES,
    RETRACT,
    SEED,
    USE_DOCKER,
    timed_query,
)

if __name__ == "__main__":

    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog:
            timed_query(prolog, RETRACT.format("deployment(_,_,_,_)"))
            t1 = threading.Thread(target=scheduler_loop, args=(prolog, NUM_NODES, SEED))
            t2 = threading.Thread(
                target=controller_loop, args=(prolog, SEED, USE_DOCKER)
            )

            t1.start()
            t2.start()

            t1.join()
            t2.join()
