import argparse
import re
from openai import OpenAI


def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyze and optimize Nginx configurations using OpenAI GPT.")
    parser.add_argument(
        '--config-file',
        required=True,
        type=str,
        help="Path to the Nginx configuration file to be analyzed"
    )
    return parser.parse_args()


def read_config_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    except Exception as e:
        raise IOError(f"Error reading the configuration file: {str(e)}")


def parse_recommendations_and_status(response_content):
    recommendation_match = re.search(r"Recommendation:\s*(.*)", response_content)
    status_match = re.search(r"Recommendation Status:\s*(\w+)", response_content)

    if recommendation_match and status_match:
        recommendation = recommendation_match.group(1).strip()
        status = status_match.group(1).lower().strip()

        if status not in {'warning', 'high', 'critical'}:
            raise ValueError(f"Invalid status: {status}")

        return recommendation, status
    else:
        raise ValueError("Failed to parse recommendation and status from the response.")


def main():

    args = parse_arguments()
    config_file = args.config_file

    try:
        nginx_config = read_config_file(config_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        return

    client = OpenAI()

    try:
        completion = client.chat.completions.create(
            model='gpt-4o-mini',  # Убедитесь, что модель доступна
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'You are an expert in configuring and optimizing Nginx servers. '
                        'Review the given configuration and provide one overall recommendation and its corresponding status. '
                        'Your response should follow this structure: '
                        '1. Recommendation: [The overall recommendation here]. '
                        '2. Recommendation Status: [One of: "warning", "high", "critical"]. '
                        'The response must only contain these two fields and be formatted exactly as shown.'
                    )
                },
                {
                    'role': 'user',
                    'content': f"Here's my Nginx configuration. Please review it and provide recommendations:\n\n{nginx_config}"
                },
            ],
        )

        response_content = completion.choices[0].message.content
    except Exception as e:
        print(f"Error during OpenAI API call: {str(e)}")
        return

    try:
        recommendation, status = parse_recommendations_and_status(response_content)
        print(f"Configuration analyzed successfully.")
        print(f"Recommendation: {recommendation}")
        print(f"Status: {status}")

    except ValueError as e:
        print(f"Error determining status: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == '__main__':
    main()
