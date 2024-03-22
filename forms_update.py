import requests
from gforms import Form
from gforms.elements import Short, Value

form_url = "https://docs.google.com/forms/d/1aasFUOOYthqspJuXRs9zaAl9IoS4PFE-dvV3fQT65Fc/viewform"
beano_url = "https://beano-data.herokuapp.com/api/v1/poll_votes/results"
beano_qid = "1709814981761"
beano_auth = "379cd32c8c21c0c472a80dedd2e14673"
candidate_keys = ["1709815700398", "1709815679894", "1709815687824"]

current_data = [0.3, 0.2, 0.2]
def callback(element, page_index, element_index):
	if page_index != 0:
		return

	if element_index == 3:
		return Value.DEFAULT

	return str(current_data[element_index])

def submit_data():
	global current_data

	response = requests.get(beano_url, {"question_id": beano_qid}, headers={"Authorization": beano_auth})
	votes = response.json()["pollVotes"][beano_qid]

	current_data = [votes[candidate]["percentage"] for candidate in candidate_keys]

	form = Form()

	form.load(form_url)
	form.fill(callback)
	form.submit()

schedule.every(20).minutes.do(submit_data)