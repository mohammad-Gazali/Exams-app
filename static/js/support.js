const questions = document.querySelectorAll('.question');
const answers = document.querySelectorAll('.answer');


questions.forEach((question) => {
    question.onclick = () => {
        if (question.classList.contains('active')) {
    
            question.classList.remove('active');
            question.querySelector('.answer').style.height = 0

        } else {

            questions.forEach((q) => {
                q.classList.remove('active');
                question.querySelector('.answer').style.height = 0
            })
    
            question.classList.add('active');
            const ans = question.querySelector('.answer');

            //? I don't Know why but the prefect height is scrollHeight * 2 😁
            ans.style.height = (ans.scrollHeight * 2) + "px";
        }
    }
})