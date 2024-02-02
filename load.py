import click
from locust import HttpUser, between, task

class LoadTest(HttpUser):
    wait_time = between(1, 5)  # Time between requests in seconds

    @task
    def navugate_to_url(self):
        self.client.get("/")

@click.command()
@click.option('--url', prompt='Enter the target URL', help='Target URL for load testing')
def run_locust(url):
    LoadTest.host = url
    click.launch(f"locust -f {__file__} --headless --users 10 --spawn-rate 2")

if __name__ == '__main__':
    run_locust()
