import subprocess


def start_minikube():
    try:
        subprocess.run(["minikube", "start", "--cpus=4", "--memory=8192"], check=True)
        print("Started Minikube successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to start Minikube:", e)


def is_minikube_running() -> bool:
    """Check if Minikube is running."""
    result = subprocess.run(
        ["minikube", "status", "--format", "{{.Host}}"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() == "Running"


def stop_minikube():
    subprocess.run(["minikube", "stop"], check=True)


def delete_minikube():
    subprocess.run(["minikube", "delete"], check=True)
