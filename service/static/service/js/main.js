
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
    cardItem.addEventListener('click', () => {
        cardContent = cardItem.querySelector('.card-content');

        if (cardContent.style.display != 'flex') {
            cardContent.style.display = 'flex';
        } else {
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
}


