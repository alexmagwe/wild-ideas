var socket = io.connect(window.location.protocol == 'https:' ? 'wss://' + document.domain + '/' : 'http://' + document.domain + ':' + location.port);
// var socket = io()
socket.on('connect', () => {
    let msg = document.createElement('span')
    msg.style.position = "absolute"
    msg.style.top = '0'
    msg.style.left = '0'
    msg.style.width = '100%'
    msg.style.color = '#111'
    let body = document.querySelector('body')
    body.appendChild(msg)

    let data = { 'data': 'query_lessons' };
    socket.emit('request', data);
    $('form').submit(event => {
        event.preventDefault();
        let question = $('#question').val()
        socket.emit('request', {
            'lesson': question
        })
        $('#question').val("").focus();

    })
})

socket.on('receive', (msg) => {
    if (msg.lessons !== undefined && msg.lessons.length > 1) {
        msg.lessons.forEach(display);
    } else if (typeof msg.lesson !== undefined) {
        display(msg);
    }
})
const display = (data, index) => {
    let container = $('#lesson-container')
    let lesson = document.createElement('div');
    let date = document.createElement('span')
    date.innerHTML = data.date
    lesson.innerHTML = data.lesson;
    lesson.append(date);
    lesson.className += 'lesson';
    container.append(lesson);


}