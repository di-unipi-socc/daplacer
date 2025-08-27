from swiplserver import PrologMQI

from daplacer.k8s.pods import generate_pods

if __name__ == "__main__":
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog:
            # Generate and apply pods
            generate_pods(prolog, apply=True)
