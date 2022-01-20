
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