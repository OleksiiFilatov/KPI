
class chat_control {
    constructor() {
        this.msg_list = $('.msg-group');
    }


    receive_msg(name, msg) {
        this.msg_list.append(this.get_msg_html(name, msg, 'left'));
        this.scroll_to_bottom(); 
    }

    receive_msg_link(name, src, dst, counter) {
        this.msg_list.append(this.get_msg_link_html(name, src, dst, counter));
        this.scroll_to_bottom(); 
    }

    get_msg_html(name, msg, side) {
        var msg_temple = `
            <div class="alert-dark" style="margin-top:2px">
                <div class="card-body">
                    <h6 class="card-subtitle mb-2 text-muted text-${side}">${name}</h6>
                        <p class="card-text float-${side}">${msg}</p>
                </div>
            </div>
            `;
        return msg_temple;
    }


    get_msg_link_html(name, src, dst, counter) {
        src = "http://" + window.location.host + "/" + src
        var msg_temple = `
                <div class="card-body alert alert-light" style=" margin: 2px 0px 1px 0px;; background-color: seashell;">
                    <h6 class="card-subtitle mb-2 text-muted ">${name}</h6>
                        <p class="card-text"> 
                        Source: <a href="${src}" target="_blank" rel="nofollow noopener">${src}</a> <br>
                        Destination <a href="${dst}" target="_blank" rel="nofollow noopener">${dst}</a> <br>
                        Counter ${counter} </p>
                </div>
            </div>
            `;
        return msg_temple;
    }
        scroll_to_bottom() {
            this.msg_list.scrollTop(this.msg_list[0].scrollHeight);
            }
        }

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/chat/ws/')

        var chat = new chat_control();
    
        send_button = $('#send') 
        share_button = $('#share') 
        input_box = $('#input-box') // get jquery element from div id
        
        function handle_msg(msg) {
            msg = msg.trim()
            msg = msg.replace(/(?:\r\n|\r|\n)/g, '<br>')
            return msg
        }

    
       

        
        send_button.on('click', send_msg.bind());

        chatSocket.onopen = function(e) {
            chat.receive_msg("Info", "Server online")
        }
        chatSocket.onerror = function(e) {
            chat.receive_msg("Server", "Сonnection error occurred. Please try again later")
            send_button.prop('disabled', true)    
        }
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.type == "chat_link")
                chat.receive_msg_link(data.name, data.src, data.dst, data.counter)
            else
                chat.receive_msg(data.name, data.message)
        }

        function send_msg() {
            msg = handle_msg(input_box.val());
            if (msg != '') {
                chatSocket.send(JSON.stringify({
                    'message': msg
                }))
            }
        }
        function link_list() {  
            jQuery('#listmodal').modal('toggle')
        }
        

        function get_links_and_render(link) {
            fetch(link)
            .then((response) => {
                return response.json();
             })
            .then((data) => {
                for (obj of data.results) {
                list.append(
                    `
                    <button type="button" class="list-group-item list-group-item-action dont-break-out" 
                    onclick=
                    "
                    handler('${obj.src}')
                    "
                    >
                    Link to ${obj.dst}
                    </button>
                    `)   
                }
                if (data.next)
                    get_links_and_render(data.next) 
            });
        }

        $('document').ready(function() {
            share_button.on('click', link_list);
            $("#closeb").on('click', link_list)
            $('#listmodal').on('show.bs.modal', function(e) {
                list = $("#modal-body")
                list.empty()
                list.append('<div class="list-group">')
                api_url = "http://" + window.location.host + "/api/urls/"
                get_links_and_render(api_url)
                list.append('</div>')
            })
        })
        
        function handler(url){
            fetch( "http://" + window.location.host + '/' + url + "/send/");
            link_list();
        }