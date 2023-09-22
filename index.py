#!/usr/local/bin/python3

import os
import time
from kubernetes import client, config

def list_ingresses(namespace='default', interval_seconds=30, output_file='/data/index.html'):
    header = """
<!doctype html>
<html>
  <head>
    <title>Ingresses index</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
  </head>
  <body>
    <h2>Ingresses index</h2>
    <table>
    """

    footer = """
    </table>
  </body>
</html>
    """
    try:
        # Load Kubernetes configuration from the pod's service account
        config.load_incluster_config()

        # Create a Kubernetes API client
        api_client = client.ApiClient()

        # Create a NetworkingV1Api instance for working with Ingress resources
        v1 = client.NetworkingV1Api(api_client)

        while True:
            # List Ingress resources in the specified namespace
            ingresses = v1.list_namespaced_ingress(namespace=namespace)

            with open(output_file + '.tmp', 'w') as file:
                file.write(header)
                for ingress in ingresses.items:
                    for rule in ingress.spec.rules:
                        for path in rule.http.paths:
                            file.write(f"<tr><td>{ingress.metadata.namespace}/{ingress.metadata.name}</td><td><a href=\"http://{rule.host}{path.path}\">{rule.host}{path.path}</a></td></tr>\n")
                file.write(footer)
            os.replace(output_file + '.tmp', output_file)
            time.sleep(interval_seconds)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_ingresses()
