const questions = document.querySelectorAll('.question');
const answers = document.querySelectorAll('.answer');



function wait(time) {
    return new Promise((resovle, reject) => setTimeout(resovle, time))
}

const size = async () => {
    await wait(40)
    answers.forEach((ans) => {
        ans.setAttribute('data-height', ans.clientHeight);
        ans.style.maxHeight = 0;
    })
}

size();

window.onresize = () => {
    size();
}


questions.forEach((question) => {
    question.onclick = () => {
        if (question.classList.contains('active')) {
    
            question.classList.remove('active');

            let ans = question.querySelector('.answer');
            ans.style.maxHeight = 0

        } else {

            questions.forEach((q) => {
                q.classList.remove('active');
                let a = q.querySelector('.answer');
                a.style.maxHeight = 0;
            })
    
            question.classList.add('active');
            let ans = question.querySelector('.answer');
            ans.style.maxHeight = ans.dataset.height + "px";
        }
    }
})