import click
import subprocess
from locust import HttpUser, between, task
from datetime import datetime

class LoadTest(HttpUser):
    # Default wait time between requests
    wait_time = between(1, 5)  # Time between requests in seconds

    @task
    def navigate_to_url(self):
        self.client.get("/")

@click.command()
@click.option('--url', prompt='Enter the target URL', help='Target URL for load testing')
@click.option('--users', type=int, prompt='Enter the number of users', help='Number of users to simulate')
@click.option('--duration', type=int, prompt='Enter the test duration in minutes', help='Test duration in minutes')
@click.option('--wait-time', type=int, prompt='Enter time between requests in seconds', help='Time between requests in seconds')
def run_locust(url, users, duration, wait_time):
    LoadTest.host = url
    LoadTest.wait_time = between(wait_time, wait_time)  # Set wait time based on user input

    # Get current date and time
    current_datetime = datetime.now().strftime('%d %B %Y, %I.%M%p')

    # Replace spaces and commas in the formatted datetime to create a suitable filename
    filename = current_datetime.replace(' ', '_').replace(',', '') + '_load_test_report.html'

    subprocess.run(['locust', '-f', __file__, '--headless', '--host', url, '--users', str(users), '--spawn-rate', '2', '--run-time', f'{duration}m', '--html', filename])

if __name__ == '__main__':
    run_locust()
