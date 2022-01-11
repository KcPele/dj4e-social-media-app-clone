const modelBtns = [...document.getElementsByClassName("model-button")];
const modelBody = document.getElementById("model-body-confirm");
const startBtn = document.getElementById("start-button");
const url = window.location.href;
modelBtns.forEach(modelBtn =>
  modelBtn.addEventListener("click", () => {
    const pk = modelBtn.getAttribute("data-pk");
    const name = modelBtn.getAttribute("data-quiz");
    const numQuestions = modelBtn.getAttribute("data-questions");
    const time = modelBtn.getAttribute("data-time");
    const scoreToPass = modelBtn.getAttribute("data-pass");
    const difficulty = modelBtn.getAttribute("data-difficulty");

    modelBody.innerHTML = `
        <div class="h5 mb-3">Are you sure you want to begin "<b>${name}</b>"?</div>
        <div class="text-muted">
            <ul>
                <li>difficulty: <b>${difficulty} </b></li>
                <li>number of questions: <b>${numQuestions} </b></li>
                <li>score to pass: <b>${scoreToPass}%</b></li>
                <li>time: <b>${time} min</b></li>

            </ul>

        </div>

    `;

    startBtn.addEventListener("click", () => {
      window.location.href = url + pk;
    });
  })
);
