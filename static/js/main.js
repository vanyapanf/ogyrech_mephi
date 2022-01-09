
const modal = document.querySelector('.modal');
const addBtn = document.querySelector('.add-btn');
const close = modal.querySelector('.close');
const cards= document.querySelectorAll('.card');

addBtn.addEventListener('click', () => {
    modal.classList.add('is-open')
})   

close.addEventListener('click', () => {
    modal.classList.remove('is-open')
})

for (let cardItem of cards) {
    cardItem.addEventListener('click', () => {
        cardContent = cardItem.querySelector('.card-content');

        if (cardContent.style.display != 'block') { 
            cardContent.style.display = 'block';
        } else { 
            cardContent.style.display = 'none'; 
        }
    })
}