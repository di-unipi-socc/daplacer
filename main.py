from daplacer.k8s import start_minikube, is_minikube_running, generate_pods

if __name__ == "__main__":
    start_minikube()
    if not is_minikube_running():
        print("Minikube is not running. Please start it first.")
    else:
        print("Minikube is running. Generating pods...")

    # generate_pods(apply=False)
