from flask import Blueprint, request, jsonify
from crawling import task

blue_repeat = Blueprint("repeat", __name__, url_prefix="/repeat")
current_repaet = -1

# Control repeat time
## GET method
@blue_repeat.route('', methods=["GET"], strict_slashes=False)
def GET_repeat():
    global current_repaet
    if current_repaet == -1:
        from Module import default_repeat_time
        return jsonify({"messege" : "Current repeat time is " + str(default_repeat_time) + " second"}), 200
    else:
        return jsonify({"messege" : "Current repeat time is " + str(current_repaet) + " second"}), 200

## POST method
@blue_repeat.route('', methods=["POST"], strict_slashes=False)
def POST_repeat():
    from Module import schedule

    # Set repeat time 
    data = request.get_json()

    if data['repeat'] < 1:
        return jsonify({"messege" : "Repeat time must be at least 1 second. Your repeat is " + str(data['repeat'])}),  400
    else:
        global current_repaet
        current_repaet = data['repeat']

        # Check job
        # if job is exist, delete job
        if schedule.get_jobs():
            schedule.remove_job('my_job')
        
        # Set new repeat time, Create new job
        schedule.add_job(task, 'interval', seconds=current_repaet, id='my_job')
        return jsonify({"messege" : 'Apply Repeat time'}), 200
