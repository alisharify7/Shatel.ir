async function GetTicketInfo(ticketID) { // get a ticket info
    const bodyDATA = new FormData();
    bodyDATA.append("TICKET_ID", ticketID);

    let response = await fetch("/user/ticket-info/", {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("#csrftoken").value
        },
        body: bodyDATA
    })
    let data = await response.json()
    return data
}


const ModalTicket = new bootstrap.Modal(document.getElementById('modal-ticket'), {})

function ShowModalTicket(data) {
    const number = document.querySelector("#TicketNumber")
    const time = document.querySelector("#TicketTime")
    const title = document.querySelector("#TicketTitle")
    const status = document.querySelector("#TicketStatus")
    const message = document.querySelector("#TicketMessage")
    const ShowAnswerBtn = document.querySelector("#ShowAnswerBtn")
    const answerErrorText = data.answer_error

    message.textContent = data.message
    message.setAttribute("rows", data.message.length <= 150 ? "5" : "10")

    ShowAnswerBtn.setAttribute("data-answer", data.answer)
    number.textContent = `#${data.ticket_number}`;
    time.textContent = `${data.created_at}`;

    title.textContent = `${data.title.length <= 45 ? data.title : data.title.slice(45) + " ..."}`;
    title.setAttribute('data-bs-title', data.title)

    status.textContent = `${!data.answer_status ? status.dataset.waited : status.dataset.ok}`
    status.className = (!data.answer_status ? 'badge bg-warning cursor-pointer' : 'badge bg-success cursor-pointer')

    ShowAnswerBtn.addEventListener("click", event => { // if show answer clicked
        let answer = (ShowAnswerBtn.dataset.answer)
        if (answer !== 'null') {
            Swal.fire({
                icon: "success",
                title: data.title,
                text: answer
            })
        } else {
            Swal.fire({
                icon: "warning",
                title: data.title,
                text: answerErrorText
            })
        }
    })


    ModalTicket.show();
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
}

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')

async function SetUP() {

    document.querySelectorAll(".ticket-row").forEach(each => {
        each.addEventListener("click", async row => {
            let TicketID = (row.currentTarget.dataset.ticketKey)
            let response = await GetTicketInfo(TicketID);
            if (response.status.toLocaleLowerCase() == "success") {
                ShowModalTicket(response.message)
            } else {
                Swal.fire({
                    icon: "error",
                    title: response.status,
                    title: response.status,
                    text: response.message
                })
            }
        })
    })
}

SetUP()