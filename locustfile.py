import click
import subprocess
from locust import HttpUser, between, task
from datetime import datetime

class LoadTest(HttpUser):
    wait_time = between(1, 5)  # Time between requests in seconds

    @task
    def navigate_to_url(self):
        self.client.get("/")

@click.command()
@click.option('--url', prompt='Enter the target URL', help='Target URL for load testing')
def run_locust(url):
    LoadTest.host = url

    # Get current date and time
    current_datetime = datetime.now().strftime('%d %B %Y, %I.%M%p')

    # Replace spaces and commas in the formatted datetime to create a suitable filename
    filename = current_datetime.replace(' ', '_').replace(',', '') + '_load_test_report.html'

    subprocess.run(['locust', '-f', __file__, '--headless', '--host', url, '--users', '10', '--spawn-rate', '2', '--html', filename])

if __name__ == '__main__':
    run_locust()
