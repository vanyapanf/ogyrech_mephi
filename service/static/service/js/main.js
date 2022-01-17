
const modal = document.querySelector('.modal');
const addBtn = document.querySelector('.add-btn');
const close = modal.querySelector('.close');
const cards= document.querySelectorAll('.card');

addBtn.addEventListener('click', () => {
    modal.classList.add('is-open')
})

close.addEventListener('click', () => {
    location.reload()
    modal.classList.remove('is-open')
})

for (let cardItem of cards) {
    cardItem.addEventListener('click', (event) => {
        cardContent = cardItem.querySelector('.card-content');

        if (!cardContent.contains(event.target) && cardContent.style.display != 'flex') {
            cardContent.style.display = 'flex';
        }
        else if (!cardContent.contains(event.target) && cardContent.style.display == 'flex') {
            cardContent.style.display = 'none';
        }
    })
}

function CreateProject() {
    // const name = $('#name').val();
	const name2 = document.getElementById('name').value
    const description = document.getElementById('description').value
    console.log(description)
	console.log(name2)
	$.ajax({
		url:    	'add_project',
		method:		'POST',
		cache: 		false,
		data:   	JSON.stringify({'name': name2, 'description':description}),
		contentType: 'application/json; charset=utf-8',
        dataType:	'html',
		success: function(data) {
			$('body').html(data);
		}
	});
	modal.classList.remove('is-open');
	location.reload()
}

function CreateRelease() {
    // const name = $('#name').val();
	const name2 = document.getElementById('name').value
    const description = document.getElementById('description').value
	const project_id = document.getElementById('project_id').value
    console.log(description)
	console.log(name2)
	$.ajax({
		url:    	'add_release',
		method:		'POST',
		cache: 		false,
		data:   	JSON.stringify({'name': name2, 'description':description, 'project_id': project_id}),
		contentType: 'application/json; charset=utf-8',
        dataType:	'html',
		success: function(data) {
			$('body').html(data);
		}
	});
	modal.classList.remove('is-open');
	location.reload()
}

function CreateTestRun() {
    const test_runner = document.getElementById('test_runner').value
	const release_id = document.getElementById('release_id').value

	$.ajax({
		url:    	release_id+'/add_testrun',
		method:		'POST',
		cache: 		false,
		data:   	JSON.stringify({'test_runner': test_runner, 'release_id':release_id}),
		contentType: 'application/json; charset=utf-8',
        dataType:	'html',
		success: function(data) {
			$('body').html(data);
		}
	});
	modal.classList.remove('is-open');
	location.reload()
}

function CreateTestCase() {
    // const name = $('#name').val();
	const expected_result = document.getElementById('expected-result').value
    const description = document.getElementById('description').value

    console.log(description)
	console.log(expected_result)
	$.ajax({
		url:    	'add_test_case',
		method:		'POST',
		cache: 		false,
		data:   	JSON.stringify({'description':description, 'expected_result': expected_result}),
		contentType: 'application/json; charset=utf-8',
        dataType:	'html',
		success: function(data) {
			$('body').html(data);
		}
	});
	modal.classList.remove('is-open');
	location.reload()
}

function AddToTestRun() {
	var checked = document.getElementsByClassName('checkbox-row');
	var values = [];
	for(var i = 0; i < checked.length; i++){
		if(checked[i].checked){
			 var case_id = checked[i].getAttribute("value");
			 values.push(case_id);
		}
	}
	console.log(values)
	const json_values = JSON.stringify(values);

	$.ajax({
		url:    	'add_test_case',
		method:		'POST',
		cache: 		false,
		data:   	JSON.stringify({'case_ids': json_values}),
		contentType: 'application/json; charset=utf-8',
        dataType:	'html',
		success: function(data) {
			$('body').html(data);
		}
	});
	modal.classList.remove('is-open');
	location.reload()
}

function SuccessfulCase() {
	var real_result = document.getSelection().focusNode.childNodes.item(3).firstChild.toString()
	var test_case_id = document.getSelection().focusNode.childNodes.item(9).firstChild.toString()
	const test_run_id = document.getElementById('test_run_id').value

	console.log(test_run_id)
	console.log(test_case_id)
	console.log(real_result)

	var status = 'True'
	$.ajax({
		url:    	test_run_id+'/finish_test_case',
		method:		'POST',
		cache: 		false,
		data:   	JSON.stringify({'real_result': real_result, 'test_case_id': test_case_id, 'status': status, 'test_run_id': test_run_id}),
		contentType: 'application/json; charset=utf-8',
        dataType:	'html',
		success: function(data) {
			$('body').html(data);
		}
	});
}

function FailedCase() {
	var real_result = document.getSelection().focusNode.childNodes.item(8).firstChild
	var test_case_id = document.getSelection().focusNode.childNodes.item(9).firstChild
	const test_run_id = document.getElementById('test_run_id').value

	console.log(test_run_id)
	console.log(test_case_id)
	console.log(real_result)

	var status = 'False'
	$.ajax({
		url:    	test_run_id+'/finish_test_case',
		method:		'POST',
		cache: 		false,
		data:   	JSON.stringify({'real_result': real_result, 'test_case_id': test_case_id, 'status': status, 'test_run_id': test_run_id}),
		contentType: 'application/json; charset=utf-8',
        dataType:	'html',
		success: function(data) {
			$('body').html(data);
		}
	});
}

