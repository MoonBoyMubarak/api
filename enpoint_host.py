from flask import Flask, request, jsonify
from datetime import datetime
import pytz


app = Flask(__name__)

# ensures json responses are in order of arrangement (JSON originally unorders responses) 
app.json.sort_keys = False

#utc time format
def get_current_utc_time():
  return datetime.now(pytz.utc)

#validating utc time difference btw client request time and server received time
def validate_utc_time(current_time):
  request_received_time = get_current_utc_time()
  time_difference = abs((current_time - request_received_time).total_seconds())
  return time_difference <= 120


@app.route('/api', methods=['GET'])

#queries 
def get_info():
  slack_name = request.args.get('slack_name')
  track = request.args.get('track')

  #handling errors  
  if not slack_name or not track:
    return jsonify({'error': 'Both slack_name and track are required'}), 400


  current_utc_time = get_current_utc_time()

  if not validate_utc_time(current_utc_time):
    return jsonify({'error': 'UTC time validation failed'}), 400

  # respones 
  current_day = current_utc_time.strftime('%A')
  github_repo_url = "https://github.com/MoonBoyMubarak/api.git"
  github_file_url = "https://github.com/MoonBoyMubarak/api/blob/main/enpoint_host.py"

  response = {
      'slack_name': slack_name,
      'current_day': current_day,
      'utc_time': current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
      'track': track,
      'github_file_url': github_file_url,
      'github_repo_url': github_repo_url,
      'status_code': 200
  }

  return jsonify(response)


if __name__ == '__main__':
  app.run(debug=True)
