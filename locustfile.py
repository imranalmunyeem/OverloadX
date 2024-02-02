import click
import subprocess
from locust import HttpUser, between, task
from datetime import datetime
import logging

class AdvancedLoadTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def navigate_to_url(self):
        self.client.get("/")

    @task
    def simulate_user_activity(self):
        # Add more realistic tasks simulating user activity
        # For example, logging in, performing actions, logging out, etc.
        pass

@click.command()
@click.option('--url', prompt='Enter the target URL', help='Target URL for load testing')
@click.option('--users', type=int, prompt='Enter the number of users', help='Number of users to simulate')
@click.option('--duration', type=int, prompt='Enter the test duration in minutes', help='Test duration in minutes')
@click.option('--wait-time', type=int, prompt='Enter time between requests in seconds', help='Time between requests in seconds')
@click.option('--spawn-rate', type=int, prompt='Enter spawn rate', help='User spawn rate per second')
@click.option('--html-report', type=click.Path(), help='Path to save HTML report')
def run_locust(url, users, duration, wait_time, spawn_rate, html_report):
    AdvancedLoadTest.host = url
    AdvancedLoadTest.wait_time = between(wait_time, wait_time)

    current_datetime = datetime.now().strftime('%d %B %Y, %I.%M%p')
    filename = current_datetime.replace(' ', '_').replace(',', '') + '_load_test_report.html'

    if html_report:
        filename = html_report

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

    try:
        logging.info('Starting the load test...')

        subprocess.run(['locust', '-f', __file__, '--headless', '--host', url, '--users', str(users),
                        '--spawn-rate', str(spawn_rate), '--run-time', f'{duration}m', '--html', filename])

        logging.info(f'Load test completed. HTML report saved at: {filename}')
    except Exception as e:
        logging.error(f'Error during load test: {str(e)}')

if __name__ == '__main__':
    run_locust()
